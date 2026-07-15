<div align="center">

# 🌐 Web Intelligence Ingestion Engine

### 🚀 Production-Grade Brand Intelligence Data Foundation

**Fetches ➜ Crawls ➜ Cleans ➜ AI Scores ➜ Structures ➜ Stores**

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

</p>

---

### ⚡ Architecture

```text
              🔍 Search Query
                     │
                     ▼
          🌍 Search Engine APIs
                     │
                     ▼
              📄 URL Discovery
                     │
                     ▼
          ⚡ Redis Crawl Queue
                     │
      ┌──────────────┴──────────────┐
      ▼                             ▼
 🚀 Crawl Worker               🚀 Crawl Worker
      ▼                             ▼
      └──────────────┬──────────────┘
                     ▼
         📰 HTML Content Extraction
                     ▼
          🧹 Cleaning & Processing
                     ▼
         🤖 AI Relevance Scoring
                     ▼
          📑 Structured Documents
                     ▼
      PostgreSQL • MongoDB • Redis
```

</div>

---

# ✨ Features

- 🌍 Intelligent Web Search
- 🚀 Multi-threaded Crawling
- 📄 HTML Content Extraction
- 🧹 Automatic Text Cleaning
- 🤖 AI-based Relevance Scoring
- 📊 Sentiment Analysis
- 📝 Content Summarization
- ⭐ Source Credibility Analysis
- 🔎 Full-text Search
- 📈 Analytics Dashboard
- 💾 MongoDB + PostgreSQL Storage
- ⚡ Redis Queue Processing

---

# 📦 Tech Stack

| Layer | Technology |
|--------|------------|
| Backend | FastAPI |
| Language | Python 3.11+ |
| Queue | Redis |
| Database | PostgreSQL |
| Document Store | MongoDB |
| Containers | Docker |
| AI | Anthropic Claude |
| Search | SerpAPI / DuckDuckGo |

---

# 🚀 Quick Start

## 📋 Prerequisites

Install the following:

- 🐍 Python 3.11+
- 🐳 Docker Desktop
- 🌱 Git (Optional)

### Verify Installation

```bash
python --version
```

Expected:

```
Python 3.11+
```

---

# 📂 Clone / Extract Project

```bash
unzip web-intelligence-engine.zip

cd web-intelligence-engine
```

---

# 🐳 Start Infrastructure

```bash
docker-compose up -d
```

Check status

```bash
docker-compose ps
```

Expected Services

| Service | Status |
|---------|---------|
| PostgreSQL | ✅ Healthy |
| MongoDB | ✅ Healthy |
| Redis | ✅ Healthy |

---

# 🐍 Create Virtual Environment

```bash
python -m venv venv
```

### Activate

**Windows**

```powershell
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

---

# 📥 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ⚙ Configure Environment

```bash
cp .env.example .env
```

### Anthropic

```env
ANTHROPIC_API_KEY=YOUR_API_KEY
```

### Search API

```env
SERPAPI_KEY=YOUR_API_KEY
```

or leave blank

```env
SERPAPI_KEY=
```

to use

✅ DuckDuckGo

---

# ▶ Run Server

```bash
python main.py
```

Expected Output

```
INFO: Starting Web Intelligence Engine...

✅ Redis Queue Ready

🚀 20 Workers Started

INFO: Running on http://localhost:8000
```

---

# 📖 Swagger Documentation

```
http://localhost:8000/docs
```

Interactive API documentation.

---

# 🔍 Submit Search

```bash
curl -X POST http://localhost:8000/api/v1/search/ \
-H "Content-Type: application/json" \
-d '{
  "query":"Nike brand reputation 2024",
  "max_results":30
}'
```

Response

```json
{
  "job_id":"abc123",
  "queued":28
}
```

---

# 📊 Check Progress

```bash
curl http://localhost:8000/api/v1/search/status/JOB_ID
```

Response

```json
{
  "progress_pct":57.1,
  "completed":14,
  "pending":12
}
```

---

# 📄 Retrieve Results

```bash
curl "http://localhost:8000/api/v1/content/?query=Nike+brand+reputation+2024"
```

Every document includes

- 🌍 URL
- 📰 Title
- 📄 Clean Content
- 🤖 AI Summary
- ⭐ Relevance Score
- 😊 Sentiment
- 📊 Confidence Score
- 🌐 Source Domain
- 📅 Timestamp

---

# 🐍 Python Example

```python
import httpx
import time

BASE = "http://localhost:8000"

response = httpx.post(
    f"{BASE}/api/v1/search/",
    json={
        "query":"Tesla electric vehicle market share",
        "max_results":30
    }
)

job = response.json()["job_id"]

while True:

    status = httpx.get(
        f"{BASE}/api/v1/search/status/{job}"
    ).json()

    print(status["progress_pct"])

    if status["progress_pct"] >= 100:
        break

    time.sleep(3)

results = httpx.get(
    f"{BASE}/api/v1/content/",
    params={
        "query":"Tesla electric vehicle market share"
    }
)

print(results.json())
```

Run

```bash
pip install httpx

python test_query.py
```

---

# 📡 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/v1/search/` | 🔍 Submit Query |
| GET | `/api/v1/search/status/{job_id}` | 📊 Job Status |
| GET | `/api/v1/content/` | 📄 Documents |
| GET | `/api/v1/content/search` | 🔎 Full-text Search |
| GET | `/api/v1/content/{hash}` | 📃 Single Document |
| GET | `/api/v1/content/domain/{domain}` | 🌐 Domain Results |
| GET | `/api/v1/analytics/summary` | 📈 Analytics |
| GET | `/api/v1/analytics/domains` | 🌍 Domain Stats |
| GET | `/api/v1/analytics/quality` | ⭐ Quality Distribution |
| GET | `/api/v1/crawl/queue` | ⚡ Queue Status |
| GET | `/health/` | ❤️ Health |
| GET | `/docs` | 📘 Swagger |

---

# 📊 Data Flow

```text
Search Query
      │
      ▼
🔍 Discover URLs
      │
      ▼
⚡ Queue URLs
      │
      ▼
🌍 Crawl Websites
      │
      ▼
🧹 Clean HTML
      │
      ▼
🤖 AI Processing
      │
      ▼
📄 Structured Documents
      │
      ▼
💾 MongoDB + PostgreSQL
      │
      ▼
📈 Analytics APIs
```

---

# 🛑 Stop Services

Stop server

```
CTRL + C
```

Stop Docker

```bash
docker-compose down
```

Delete all data

```bash
docker-compose down -v
```

---

# 🩺 Troubleshooting

| Problem | Solution |
|----------|----------|
| Connection Refused | Restart Docker Services |
| No Search Results | Configure SerpAPI or Use DuckDuckGo |
| Low Relevance Score | Add Anthropic API Key |
| Port Already in Use | Change Docker Port |

Restart

```bash
docker-compose restart
```

---

# 💾 View Stored Data

## MongoDB

```bash
docker exec -it wi_mongodb mongosh
```

```javascript
use web_intelligence

db.processed_content.find().limit(5)

db.processed_content.countDocuments()
```

---

## PostgreSQL

```bash
docker exec -it wi_postgres psql -U postgres -d web_intelligence
```

```sql
SELECT status,COUNT(*)

FROM search_results

GROUP BY status;
```

---

## Redis

```bash
docker exec -it wi_redis redis-cli
```

Queue

```redis
ZCARD wi:queue
```

Jobs

```redis
KEYS wi:job:*:stats
```

---

# 🎯 Project Highlights

✅ Production Ready

✅ AI-powered Content Intelligence

✅ Scalable Queue Architecture

✅ Asynchronous Crawling

✅ Structured Knowledge Storage

✅ Enterprise-grade APIs

---

<div align="center">

## ⭐ If you found this project useful, please give it a Star!

Made with ❤️ using **Python • FastAPI • Docker • MongoDB • PostgreSQL • Redis**

</div>
