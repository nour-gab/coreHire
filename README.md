# CoreHire

CoreHire is a full-stack AI internship/job matching platform with three roles:
- Candidate
- Company
- Admin

This MVP includes a Django REST backend and a React + Tailwind frontend.

## Tech Stack
- Backend: Django, DRF, SimpleJWT
- Frontend: React (Vite), TailwindCSS, Framer Motion
- Database: PostgreSQL (with SQLite fallback if DB env vars are omitted)
- AI features:
  - Resume analysis from text/PDF
  - ATS scoring with KeyBERT fallback keyword extraction
  - AI job generation from rough descriptions
  - Job recommendations and micro-suggestions
  - Candidate/Employer chatbot endpoint

## Project Structure
- `backend/` API server
- `frontend/` web app

## Backend Setup
1. Create and activate a Python virtual environment.
2. Install dependencies:
   - `pip install -r backend/requirements.txt`
3. Create env file:
   - Copy `backend/.env.example` to `backend/.env`
4. Make sure PostgreSQL is running and DB credentials match `.env`.
5. Run migrations:
   - `cd backend`
   - `python manage.py makemigrations`
   - `python manage.py migrate`
6. Create admin user (optional):
   - `python manage.py createsuperuser`
7. Start backend:
   - `python manage.py runserver`

API base URL: `http://127.0.0.1:8000`

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

## Frontend Setup
1. Install dependencies:
   - `cd frontend`
   - `npm install`
2. Configure frontend env:
   - Copy `frontend/.env.example` to `frontend/.env`
3. Run frontend:
   - `npm run dev`

Frontend URL: `http://127.0.0.1:5173`

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
- AI chatbot is currently implemented as a practical rule-based assistant endpoint that can later be switched to Hugging Face inference.
- GitHub integration is available for public repo/language extraction via `/ai/import-profile-data/`; LinkedIn import is implemented as parsing simulation from provided profile text.
- Resume builder export to PDF is not yet fully implemented in this MVP shell, but candidate profile and AI suggestion workflows are ready.
