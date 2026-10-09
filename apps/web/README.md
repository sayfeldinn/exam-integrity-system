# apps/web

Next.js (App Router, TypeScript) frontend for the student and proctor UI.

## Decisions

- **Styling:** Tailwind CSS (enabled via `create-next-app`).
- **Package manager:** npm (do not mix with pnpm/yarn).
- **Node:** 20 (see `.nvmrc`).
- **API calls:** client-side `fetch` using `NEXT_PUBLIC_API_URL`, so CORS problems show up early (see M0-24).

## Run locally

```bash
cp .env.local.example .env.local
npm ci
npm run dev
```

Open http://localhost:3000

## Environment variables

| Variable | Purpose | Local value |
| --- | --- | --- |
| `NEXT_PUBLIC_API_URL` | Base URL of the FastAPI backend, read in the browser | `http://localhost:8000` |

## Scripts

- `npm run dev`: start the dev server
- `npm run lint`: run ESLint
- `npm run build`: production build