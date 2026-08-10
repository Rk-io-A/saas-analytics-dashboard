# SaaS Analytics Dashboard 📊

**Full Stack SaaS Subscription Analytics Dashboard**

Track MRR, Churn, Revenue, Active Users and more. Perfect portfolio project for Full Stack Developers.

## 📁 Structure

```
saas-analytics-dashboard/
├── frontend/          # Next.js 14 + Tailwind CSS + TypeScript
├── backend/           # FastAPI + SQLAlchemy
├── .gitignore
└── README.md
```

## ✨ Features

- 📈 MRR (Monthly Recurring Revenue) tracking
- 📉 Churn rate calculation
- 👥 Active subscribers count
- 💰 Revenue overview
- 🔐 JWT Authentication
- 🎨 Modern dark/light dashboard UI
- 📡 Ready for Stripe webhook integration

## 🛠️ Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Frontend  | Next.js 14, TypeScript, Tailwind  |
| Backend   | FastAPI, SQLAlchemy, Pydantic     |
| Database  | SQLite (local) / PostgreSQL       |
| Auth      | JWT                               |

## 🚀 How to Run

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
→ http://localhost:8000  |  Docs: http://localhost:8000/docs

### Frontend
```bash
cd frontend
npm install
npm run dev
```
→ http://localhost:3000

## 👨‍💻 Author

**Rajiv Kapur**  
Software Architect & Full Stack Developer  
[Portfolio](https://rajivkapur.in.net) · [GitHub](https://github.com/Rk-io-A)

---
⭐ Star this repo if you find it useful!
