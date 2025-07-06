# 🐛 Issues & Insights Tracker

A full-stack issue tracking platform with real-time updates, role-based access, and background analytics. Built using **SvelteKit**, **FastAPI**, and **PostgreSQL**.

---

## ✨ Features

### 🔐 Authentication & Authorization
- Email/password authentication (JWT-based)
- Roles: `ADMIN`, `MAINTAINER`, `REPORTER`
- RBAC:
  - `REPORTER`: Create/view only own issues
  - `MAINTAINER`: View all, triage/update status/tags
  - `ADMIN`: Full CRUD access

### 📝 Issue Management
- Create, edit, delete issues
- Markdown-supported description
- Optional file path
- Severity levels: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`
- Status workflow: `OPEN → TRIAGED → IN_PROGRESS → DONE`

### 📡 Real-Time Updates
- Implemented using **Server-Sent Events (SSE)**
- Admins see real-time issue creation & status changes without refreshing

### 📊 Dashboard
- Displays chart of open issues grouped by severity
- Dynamically updates as issues change

### ⏲️ Background Job
- Every 30 min, a job aggregates issue counts by status into a `daily_stats` table
- Uses **APScheduler**

### 📚 API Docs
- Auto-generated using **FastAPI’s** OpenAPI schema
- Available at `/api/docs`

---

## 🛠️ Tech Stack

| Layer       | Technology                    |
|-------------|-------------------------------|
| Frontend    | SvelteKit (JavaScript)        |
| Backend     | FastAPI (Python)              |
| Database    | PostgreSQL                    |
| Auth        | OAuth2 (JWT)                  |
| Realtime    | Server-Sent Events (SSE)      |
| Scheduler   | APScheduler                   |
| Deployment  | Vercel (frontend), Render (backend/db) |

---

## 📦 Setup Instructions

### 🧩 1. Backend (FastAPI)

#### 📁 Navigate to `/backend` folder

```bash
cd backend

📥 Install dependencies

pip install -r requirements.txt
⚙️ Setup .env file

DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<dbname>
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
🔄 Apply migrations

alembic upgrade head
🚀 Start the backend

uvicorn app.main:app --reload
🖥️ 2. Frontend (SvelteKit)
📁 Navigate to /my-app

cd my-app
📥 Install dependencies

npm install
🚀 Start the frontend

npm run dev
Frontend runs at: http://localhost:5173
Backend runs at: http://localhost:8000

🧪 Demo Instructions
To test real-time updates:

Open 2 browser tabs

Login as different users (e.g. REPORTER and ADMIN)

Create or update an issue as reporter

Observe auto-update in admin view (no refresh)

📊    Sample Daily Stats Table
Date        OPEN	   TRIAGED	    IN_PROGRESS	  DONE
2025-07-04    3	         2	              1	       5
2025-07-03    5	         1	              2	       3

🔒 Roles and Permissions
Role     Create  View     All       EditDelete
REPORTER   ✅    ❌      ❌	      ❌
MAINTAINER ❌	✅	   ✅       	  ❌
ADMIN      ✅    ✅      ✅          ✅

🔍 API Endpoints
Visit: http://localhost:8000/api/docs
Interactive docs powered by Swagger UI.

🎥 Loom/Video Walkthrough
A short 5-min demo showing:

Registration/Login flow

Role-based access

Issue creation/edit

Real-time dashboard sync (SSE)

API docs preview

Loom video link: https://www.loom.com/share/3963d5131607420aa1f206262d80b8c5?sid=c5658c82-0341-463a-99ef-ee5f361e171c

🧑‍💻 Developer Notes
🔁 Run background scheduler manually (optional)

# Already started by app, but to run manually:
python app/jobs/scheduler.py
🐳 Docker Support (Optional)
Can be dockerized using:

Dockerfile for backend

docker-compose.yml to combine backend, db, and optionally frontend

📌 Known Limitations
File path is not actually uploaded, just stored as string

Basic form validation; no client-side markdown preview

🙏 Acknowledgements
SvelteKit

FastAPI

PostgreSQL

APScheduler

Swagger U
