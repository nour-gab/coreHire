# CoreHire

CoreHire is a full-stack AI internship/job matching platform with three roles:
- Candidate
- Company
- Admin

This MVP includes a Django REST backend and a React + Tailwind frontend.

## Tech Stack
- Backend: Django, DRF, SimpleJWT
- Frontend: React (Vite), TailwindCSS, Framer Motion
- Database: PostgreSQL (Dockerized via docker-compose)
- AI features:
  - Resume analysis from text/PDF
  - ATS scoring with KeyBERT (with lightweight fallback keyword extraction)
  - AI job generation from rough descriptions
  - Job recommendations and micro-suggestions
  - Candidate/Employer chatbot endpoint backed by Hugging Face inference (fallback-safe)

## Project Structure
- `backend/` API server
- `frontend/` web app
- `docker-compose.yml` local PostgreSQL container

## Prerequisites
- Python 3.11+ (or compatible virtual environment)
- Node.js 18+
- Docker Desktop

## 1) Start PostgreSQL With Docker
From project root:

```bash
docker compose up -d postgres
docker compose ps
```

The API expects these DB defaults (already in `backend/.env.example`):
- DB host: `127.0.0.1`
- DB port: `5432`
- DB name/user/password: `corehire/postgres/postgres`

## Backend Setup
1. Create and activate a Python virtual environment.
2. Install dependencies:
   - `pip install -r backend/requirements.txt`
3. Create env file:
   - Copy `backend/.env.example` to `backend/.env`
4. Add your Hugging Face API token in `backend/.env`:
   - `HUGGINGFACE_API_TOKEN=your_token_here`
5. Run migrations:
   - `cd backend`
   - `python manage.py makemigrations`
   - `python manage.py migrate`
6. Seed demo data:
   - `python manage.py seed_demo_data`
7. Create admin user (optional):
   - `python manage.py createsuperuser`
8. Start backend:
   - `python manage.py runserver`

API base URL: `http://127.0.0.1:8000`

### Demo Seed Credentials
- Users:
  - `admin@corehire.dev` (admin)
  - `hiring@novalabs.dev` (company)
  - `jobs@atlasworks.dev` (company)
  - `maya.candidate@corehire.dev` (candidate)
  - `sam.candidate@corehire.dev` (candidate)
- Default password: `DemoPass123!`

### Main Endpoints
- `POST /auth/register/`
- `POST /auth/login/`
- `POST /auth/refresh/`
- `GET /auth/me/`
- `GET|POST /jobs/`
- `GET|POST /applications/`
- `POST /ai/analyze-resume/`
- `POST /ai/ats-score/`
- `POST /ai/generate-job/`
- `GET /ai/recommend-jobs/`
- `POST /ai/micro-suggestions/`
- `POST /ai/chat/`
- `POST /ai/import-profile-data/`

## Backend Tests
From `backend/`:

```bash
python manage.py test apps.ai_services.tests apps.applications.tests
```

Included tests cover:
- ATS scoring computation behavior
- Candidate apply flow and role restrictions

## Frontend Setup
1. Install dependencies:
   - `cd frontend`
   - `npm install`
2. Configure frontend env:
   - Copy `frontend/.env.example` to `frontend/.env`
3. Run frontend:
   - `npm run dev`

Frontend URL: `http://127.0.0.1:5173`

Frontend now includes route protection by role using `/auth/me/` for:
- `/dashboard/candidate` -> candidate only
- `/dashboard/company` -> company only
- `/dashboard/admin` -> admin only

## Role Dashboards
- Candidate dashboard:
  - Resume suggestions
  - ATS-based recommended jobs
   - Resume builder with live preview + PDF export
   - Candidate AI chat coach
- Company dashboard:
  - AI job generator
   - Employer AI assistant
- Admin dashboard:
  - Analytics snapshot cards and moderation panel shell

## Notes
- Hugging Face inference is integrated for chatbot and resume suggestion generation, with deterministic fallback responses when token/model access is unavailable.
- GitHub integration is available for public repo/language extraction via `/ai/import-profile-data/`; LinkedIn import is implemented as parsing simulation from provided profile text.
- Resume builder export to PDF is not yet fully implemented in this MVP shell, but candidate profile and AI suggestion workflows are ready.
