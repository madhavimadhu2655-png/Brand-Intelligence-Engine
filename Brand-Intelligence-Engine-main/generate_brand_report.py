import argparse
import asyncio
import glob
import json
import os
from datetime import datetime, timezone

import httpx


async def _run_search(base_url: str, brand: str, max_results: int, search_engine: str):
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(
            f"{base_url}/api/v1/search/",
            json={"query": brand, "max_results": max_results, "search_engine": search_engine},
        )
        r.raise_for_status()
        return r.json()["job_id"]


async def _poll_status(base_url: str, job_id: str, sleep_s: int = 4):
    async with httpx.AsyncClient(timeout=60) as client:
        while True:
            r = await client.get(f"{base_url}/api/v1/search/status/{job_id}")
            # if the backend isn't ready for this job_id yet, keep polling
            if r.status_code != 200:
                await asyncio.sleep(sleep_s)
                continue
            data = r.json()
            if data.get("progress_pct", 0) >= 100:
                return data
            await asyncio.sleep(sleep_s)


def _load_latest_json_docs(json_dir: str, limit: int | None = None):
    paths = sorted(glob.glob(os.path.join(json_dir, "*.json")), key=os.path.getmtime, reverse=True)
    if limit is not None:
        paths = paths[:limit]
    docs = []
    for p in paths:
        try:
            with open(p, "r", encoding="utf-8") as f:
                docs.append(json.load(f))
        except Exception:
            continue
    return docs, paths


def _build_report(brand: str, docs: list[dict], top_k: int = 8):
    # docs are per-URL extracted docs; we build a simple aggregated report from them.
    # (If ANTHROPIC aggregation is desired, it can be added later.)
    ranked = sorted(docs, key=lambda d: float(d.get("relevance_score", 0)), reverse=True)
    top = ranked[:top_k]

    report = {
        "brand": brand,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "documents_used": len(top),
        "highlights": {
            "key_points": [],
            "sentiments": {},
            "credibility": {},
        },
        "sources": [
            {
                "url": d.get("url", ""),
                "title": d.get("title", ""),
                "source_domain": d.get("source_domain", ""),
                "relevance_score": d.get("relevance_score", 0),
                "content_summary": d.get("content_summary", ""),
            }
            for d in top
        ],
        "notes": "This report is an aggregated JSON output from per-URL extracted documents produced by the backend. Add Anthropic summarization/formatting if needed.",
    }

    # aggregate highlights
    key_points = []
    sentiments = {}
    credibility = {}
    seen_kp = set()

    for d in top:
        for kp in d.get("key_points", []) or []:
            if kp and kp not in seen_kp:
                seen_kp.add(kp)
                key_points.append(kp)
                if len(key_points) >= 12:
                    break
        s = (d.get("sentiment") or "neutral").lower()
        sentiments[s] = sentiments.get(s, 0) + 1
        c = (d.get("source_credibility") or "medium").lower()
        credibility[c] = credibility.get(c, 0) + 1

    report["highlights"]["key_points"] = key_points
    report["highlights"]["sentiments"] = sentiments
    report["highlights"]["credibility"] = credibility

    return report


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="http://localhost:8000")
    ap.add_argument("--brand", required=True, help="Brand/company name. Example: Antropic (or Google, Amazon)")
    ap.add_argument("--max-results", type=int, default=30)
    ap.add_argument("--search-engine", default="auto")
    ap.add_argument("--json-output-dir", default="./json_output")
    ap.add_argument("--docs-limit", type=int, default=20, help="How many latest per-URL docs to use")
    ap.add_argument("--top-k", type=int, default=8)
    ap.add_argument("--report-out", default="./brand_report.json")
    args = ap.parse_args()

    job_id = await _run_search(args.base_url, args.brand, args.max_results, args.search_engine)
    await _poll_status(args.base_url, job_id)

    docs, paths = _load_latest_json_docs(args.json_output_dir, limit=args.docs_limit)
    report = _build_report(args.brand, docs, top_k=args.top_k)

    with open(args.report_out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"Wrote report: {os.path.abspath(args.report_out)}")
    print(f"Used {len(docs)} latest per-URL docs from {args.json_output_dir}")


if __name__ == "__main__":
    asyncio.run(main())

