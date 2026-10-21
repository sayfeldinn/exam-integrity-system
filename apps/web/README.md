# ExamGuard AI — Graduation Project Starter

A responsive React + Vite frontend with an Express API starter for the ExamGuard AI interface.

## Requirements
- Node.js 20+ recommended
- npm

## Run locally

### 1. Start the API
```bash
cd server
npm install
npm run dev
```
API runs on http://localhost:4000

### 2. Start the frontend
In another terminal:
```bash
cd client
cp .env.example .env.local   # sets VITE_API_URL=http://localhost:8000
npm install
npm run dev
```
Frontend runs on http://localhost:5173

### 3. Check the live health page
Open http://localhost:5173/health — it fetches `GET /api/v1/health` from the
FastAPI backend (M0-23/M0-24). Three states: **ok** (green), **degraded**
(API up, database down — amber), **API unreachable** (red).

> The Express starter in `server/` (port 4000) is optional legacy scaffolding.
> The real backend is `services/api` (FastAPI, port 8000).

## Lint & format
```bash
npm run lint     # eslint (js/jsx)
npm run format   # prettier --write
```

## Included
- Dark marketing site matching the ExamGuard website design (home with the interface picker, product page, contact page)
- Student flow: sign in, identity verification, permissions, system check, timed exam with submit dialog
- Proctor dashboard: live monitoring, exams, students, violations, reports, analytics, AI assistant, settings
- Proctor mobile app preview at /mobile
- Responsive mobile navigation
- Live API health page at /health (first real browser → FastAPI integration)
- Typed API client (`src/lib/api.ts`) consuming the frozen contract + `packages/shared` types
- Express sample API endpoints and mock data

## Project structure (client/src)
- `pages/Home.jsx`, `pages/Product.jsx`, `pages/Contact.jsx` - marketing site (shared nav and footer live in `components/SiteLayout.jsx`)
- `pages/Health.jsx` - live API health check against `VITE_API_URL` (M0-23)
- `pages/student/` - login, identity verification, permissions, system check, exam
- `pages/proctor/` - dashboard shell plus one file per sidebar page
- `pages/Mobile.jsx` - proctor mobile app preview
- `components/` - small shared pieces (pills, avatars, interface selector)
- `lib/api.ts` - typed fetch client for the FastAPI backend (health, sessions, violations)
- `styles/` - one stylesheet per area; colours and fonts live in `styles/base.css`
- `data.js` - demo data used by the screens (only /health talks to the real API so far)

## Important
This is a frontend starter with demo/mock data. Camera checks and exam monitoring are UI demonstrations, not a secure proctoring implementation. Before real deployment, implement server-side authentication, authorization, persistent database storage, audit logs, rate limiting, input validation, secure session/token handling, and consent/privacy controls. Never use the demo login as real authentication.

## Demo
On the student sign-in page, any non-empty ID and password continues the demo. The proctor dashboard and mobile app open straight from the landing page ("Choose your interface").
