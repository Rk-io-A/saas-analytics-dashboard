# SaaS Analytics Dashboard

Full-stack portfolio project demonstrating subscription analytics UI and backend patterns.

> **Status:** engineering demo. MRR, churn, revenue, subscriber counts and other metrics are illustrative until connected to verified billing/customer events.

## Stack

```text
Frontend   Next.js 14 + TypeScript + Tailwind CSS
Backend    FastAPI + SQLAlchemy + Pydantic
Database   SQLite locally / PostgreSQL-ready
Auth       JWT
```

## Demonstrated metrics

- monthly recurring revenue;
- churn-rate calculation patterns;
- active subscriber counts;
- revenue overview;
- dashboard/authentication flows;
- billing-webhook integration direction.

## Local setup

Backend:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Production requirements

For real financial/subscription analytics, ingest verified provider webhooks server-side, verify signatures, deduplicate events, store immutable source events, use correct currency/timezone rules and distinguish estimates from recognized revenue. Never accept revenue or subscription state directly from the browser.

## Author

Rajiv Kapur — Software Architect & Full-Stack Developer

Portfolio: `https://rajivkapur.in.net`
