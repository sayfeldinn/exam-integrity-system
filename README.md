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
npm install
npm run dev
```
Frontend runs on http://localhost:5173

## Included
- Dark marketing site matching the ExamGuard website design (home with the interface picker, product page, contact page)
- Student flow: sign in, identity verification, permissions, system check, timed exam with submit dialog
- Proctor dashboard: live monitoring, exams, students, violations, reports, analytics, AI assistant, settings
- Proctor mobile app preview at /mobile
- Responsive mobile navigation
- Express sample API endpoints and mock data

## Project structure (client/src)
- `pages/Home.jsx`, `pages/Product.jsx`, `pages/Contact.jsx` - marketing site (shared nav and footer live in `components/SiteLayout.jsx`)
- `pages/student/` - login, identity verification, permissions, system check, exam
- `pages/proctor/` - dashboard shell plus one file per sidebar page
- `pages/Mobile.jsx` - proctor mobile app preview
- `components/` - small shared pieces (pills, avatars, interface selector)
- `styles/` - one stylesheet per area; colours and fonts live in `styles/base.css`
- `data.js` - all demo data used by the screens (the frontend does not call the API yet)

## Important
This is a frontend starter with demo/mock data. Camera checks and exam monitoring are UI demonstrations, not a secure proctoring implementation. Before real deployment, implement server-side authentication, authorization, persistent database storage, audit logs, rate limiting, input validation, secure session/token handling, and consent/privacy controls. Never use the demo login as real authentication.

## Demo
On the student sign-in page, any non-empty ID and password continues the demo. The proctor dashboard and mobile app open straight from the landing page ("Choose your interface").
