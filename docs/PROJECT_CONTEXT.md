# AI-Based Online Exam Integrity System

> Context file for LLM-assisted development (Claude Code, Cursor, Copilot, etc.).
> Keep this file up to date as decisions change — paste it into a new chat or
> reference it directly to give an assistant full project context.

## 1. Project Summary

A real-time, AI-powered proctoring platform for remote/online exams. It monitors
students via webcam, microphone, and screen activity during an exam session,
flags suspicious behavior, computes a live cheating-risk score, and gives
instructors/proctors a dashboard with alerts, recordings, and post-exam reports.

- **Type:** Graduation project (Faculty of Computers and Data Science, Alexandria University)
- **Team size:** 8 people
- **Team members:** Seif Eldeen Nasser, Jana Mostafa, Adel Serag, Hana Marwan Negm,
  Rodaina Gomaa, Moatasem Mohamed, Ahmed Refaat, Huda Mohamed Hasson (see Section 6)
- **Repo name:** `exam-integrity-system` — https://github.com/sayfeldinn/exam-integrity-system
- **Platform decision:** Web app only for now (Next.js). A Flutter proctor-only
  companion app is documented as future work, not built in the current phase.

## 2. Why Web, Not Mobile

Core features (screen monitoring, Alt+Tab / tab-switch detection, copy-paste
logging, screenshot detection) only make sense in a browser/desktop context —
there's no meaningful mobile equivalent for "leaving the exam page." Students
take exams on laptops in practice. A Flutter app for the **proctor** (alerts,
live risk scores, push notifications) is a reasonable future extension, but
was deliberately excluded from the current build to avoid splitting the
8-person team across two frontend stacks.

## 3. Feature Set (20 features across 6 categories)

### Presence & Identity Detection
1. **Face Detection** — verify student is present; alert if face disappears.
2. **Face Recognition** — match live face against university ID / registered photo.
3. **Eye Tracking** — detect prolonged looking away from the screen.
4. **Head Pose Estimation** — detect left/right/up/down looks; count repeated head-turns.
5. **Multiple Person Detection** — flag a second person in frame.

### Object & Audio Cheating Detection
6. **Phone Detection** — detect a mobile phone in frame (YOLO-based).
7. **Screenshot Detection** — record screen-capture attempts where supported.
8. **Voice Detection** — detect speech; alert if more than one voice is heard.
9. **Background Noise Detection** — measure ambient noise; alert above threshold.

### System & Screen Monitoring
10. **Screen Monitoring** — detect leaving the exam page, log/prevent Alt+Tab, log copy-paste.
11. **Session Recording** — record full session video; store key events to save storage.
12. **Live Monitoring** — live stream of students to the proctor with real-time alerts.

### AI Analysis & Risk Scoring
13. **Suspicious Behavior Detection** — combine head-turning, face loss, phone,
    extra people, and speech into a risk signal.
14. **AI Risk Score** — cheating-risk percentage, not just raw alerts.
    Example bands: `10% = normal`, `40% = requires review`, `90% = high probability of cheating`.
15. **Proctor AI Assistant** — chatbot for natural-language queries, e.g.
    "Which student has the most violations?" / "Show students who used a phone."

### Dashboard & Reporting
16. **Proctor Dashboard** — connected students, real-time alerts, risk scores,
    violation history, recorded video access.
17. **Incident Report** — auto-generated PDF per exam: face-disappearance count,
    head-turn count, phone/person detections, final assessment.
18. **Analytics** — most common violation types, average risk score, per-exam stats.

### System & Access Management
19. **Authentication** — separate student/proctor login, role-based admin permissions.
20. **Notifications** — immediate proctor alerts on violations; in-exam warnings to students.

## 4. MVP Scope (current graduation deliverable)

Full 20-feature vision is the long-term product. The MVP focuses on five pillars:

1. **Enrollment** — register student identity before the exam window opens.
2. **Liveness Detection** — confirm a real, live student (not a photo/replay).
3. **Continuous Identity Re-verification** — re-check identity throughout the session.
4. **Suspicious Activity Detection** — flag cheating-indicative behavior in real time.
5. **Instructor Dashboard** — working view for instructors to monitor/review sessions.

Remaining 15 features (object/audio detection, session recording, full
analytics, AI assistant, etc.) are planned as post-MVP extensions.

## 5. Tech Stack

### Frontend
- **Next.js (React)** — student exam interface + proctor dashboard
- **WebRTC / `getUserMedia`** — in-browser webcam & mic capture
- **TensorFlow.js / MediaPipe (client-side)** — lightweight face/eye tracking to cut server load before flagging to backend

### Backend
- **FastAPI** — async API, matches team's existing stack experience
- **WebSockets** — live video/alert streaming to the proctor dashboard
- **Celery + Redis** — background job queue for CV inference and PDF report generation (post-MVP)

### Computer Vision / ML
- **YOLOv8 (Ultralytics)** — phone detection, multiple-person detection
- **MediaPipe Face Mesh / dlib** — face detection, eye tracking, head pose estimation
- **FaceNet / ArcFace** (via `face_recognition` or `deepface`) — face recognition / liveness
- Rules-based or small-CNN scorer — suspicious-behavior risk fusion

### Audio
- WebRTC audio stream → server-side VAD (`webrtcvad` or `pyannote.audio` for multi-speaker detection)
- `librosa` — background noise level measurement

### Data & Storage
- **PostgreSQL** — students, sessions, violations, risk scores
- **S3-compatible storage** (AWS S3 or self-hosted MinIO) — session recordings (flagged clips only, post-MVP)
- **Redis** — session state, live risk scores

### AI Assistant
- **Gemini API** — natural-language querying over the structured violations DB (Proctor AI Assistant)

### Auth & Infra
- JWT-based auth, role-based access (student/proctor/admin)
- Docker Compose for local dev; Render/Railway or university server for deployment

### Future / Not in MVP
- Flutter proctor companion app (push notifications, live alerts, risk score view) — calls the same FastAPI backend.

## 6. Team Roles (8 people)

| Name | Specialization |
|---|---|
| Seif Eldeen Nasser | AI / ML / Computer Vision |
| Jana Mostafa | AI / ML / Computer Vision |
| Adel Serag | ML / Frontend |
| Hana Marwan Negm | Full Stack |
| Rodaina Gomaa | Full Stack |
| Moatasem Mohamed | AI / Flutter |
| Ahmed Refaat | AI / Flutter |
| Huda Mohamed Hasson | UI/UX / ML |

Formal version presented to the instructor: `Team_Roles.docx`.

### Suggested functional mapping

A rough mapping from specialization to the functional areas the project
needs — useful for sprint planning, not a fixed assignment:

- **CV Engineers (Identity + Objects/Behavior):** Seif Eldeen Nasser, Jana Mostafa
- **Frontend (student + proctor dashboard):** Adel Serag, plus frontend
  work split from the full-stack pair below
- **Full Stack (API + frontend integration):** Hana Marwan Negm, Rodaina Gomaa
- **Flutter (future proctor companion app) + AI support:** Moatasem Mohamed, Ahmed Refaat
- **UI/UX + ML:** Huda Mohamed Hasson — design system, dashboard UX, and
  supporting model work

Since Moatasem and Ahmed's Flutter skills map to work that's currently
future scope (Section 5), they can be applied to AI/risk-engine work or
backend support until the mobile companion app is prioritized.

## 7. Repo Structure

Monorepo layout, one repo for the whole team:

```
exam-integrity-system/
├── apps/
│   ├── web/                 # Next.js — student + proctor frontend
│   └── mobile-proctor/      # Flutter proctor app (future work — empty for now)
├── services/
│   ├── api/                 # FastAPI — auth, sessions, DB, WebSockets
│   ├── cv-identity/         # Face detection/recognition, eye tracking, head pose
│   ├── cv-objects/          # YOLO phone/person detection, screenshot detection
│   ├── audio/               # Voice detection, background noise
│   └── risk-engine/         # Risk scoring fusion, Gemini assistant, reports
├── packages/
│   └── shared/              # Shared types/schemas used by web + api
├── infra/
│   ├── docker-compose.yml
│   └── .env.example
├── docs/
│   ├── PROJECT_CONTEXT.md   # this file
│   ├── STARTING_PLAN.md     # 10-min orientation (thin pointer → milestones/M0)
│   ├── milestones/          # per-milestone execution specs — verifiable DoD
│   │   ├── M0_IMPLEMENTATION_PLAN.md  # M0: repo & scaffolding (canonical)
│   │   └── README.md        # index of M0–M6
│   ├── ARCHITECTURE.md      # service diagram, repo tree, DB tables v0
│   ├── API_CONTRACT.md      # freeze of students/sessions/violations JSON
│   ├── ONBOARDING.md        # OS matrix, verify scripts, troubleshooting
│   ├── PROGRESS_LOG.md      # dated sprint-by-sprint status entries
│   └── supervisor-log.md    # supervisor summary template
├── .github/
│   ├── workflows/           # CI — added later, not on day one
│   └── ISSUE_TEMPLATE.md    # standard task write-up template
├── .gitignore
├── README.md
└── LICENSE
```

Full step-by-step initialization order (what to push first, Ruleset
setup, backend-before-frontend sequencing, etc.) is documented in
`docs/STARTING_PLAN.md` (branch naming: `CONTRIBUTING.md`). Per-milestone
execution (DoD, phases, gates) lives in `docs/milestones/M0_IMPLEMENTATION_PLAN.md`
(index: `docs/milestones/README.md`).

**Where things get tracked, to avoid confusion:**
- **Milestones (M0–M6) and live task status** → GitHub's native Milestones +
  Issues, not a doc — this auto-updates as PRs merge.
- **Decisions that rarely change** (stack choices, repo name, structure) →
  `PROJECT_CONTEXT.md` Section 9, append-only.
- **Sprint-by-sprint progress** (what shipped, what slipped, why) →
  `docs/PROGRESS_LOG.md`, updated weekly at the Sunday retro.

## 8. Project Management Framework

**Approach: Scrumban** (Scrum + Kanban hybrid) — chosen over pure Scrum
(too much ceremony overhead for research-heavy CV/ML tasks that don't
estimate cleanly into sprints) and pure Kanban (no deadline structure,
and the project has a fixed graduation defense date).

### How it works
- **2-week sprints** for planning/check-ins, but tasks flow through a
  continuous Kanban board rather than being rigidly locked to sprint
  boundaries — a CV task that runs long just stays "In Progress" instead
  of "failing" the sprint.
- **One milestone per MVP pillar** (Section 4), due-dated against the
  defense timeline.
- **Weekly 15-minute sync** instead of daily standups, with async updates
  in a team chat (Slack/Discord) the rest of the week.

### Tooling
- **GitHub Projects** (free, built into the repo) as the board — avoids
  adding a separate tool like Jira/Trello for 8 people to check.
- Board columns: `Backlog → This Sprint → In Progress → In Review (PR open) → Done`
- Issues tagged by service area (`cv-identity`, `api`, `web`, etc.) matching
  the repo structure (Section 7), so each person's queue is filterable.

### Milestone timeline (template — adjust dates to actual defense date)

| Milestone | Target | Scope |
|---|---|---|
| M0 — Repo & Scaffolding | Week 1–2 | Skeleton pushed, `services/api` + `apps/web` scaffolded, Ruleset active targeting `main` (see `docs/STARTING_PLAN.md` Step 2 + `CONTRIBUTING.md`) |
| M1 — Enrollment | Week 3–4 | Student registration flow, ID/photo capture, DB schema for students |
| M2 — Liveness Detection | Week 5–6 | Live face verification working end-to-end (client capture → CV service → API) |
| M3 — Continuous Re-verification | Week 7–8 | Periodic identity re-checks during an active session |
| M4 — Suspicious Activity Detection | Week 9–10 | Risk signal fusion (head pose, face loss, etc.) feeding a basic risk score |
| M5 — Instructor Dashboard | Week 11–12 | Working dashboard: live sessions, alerts, risk scores |
| M6 — Integration, Polish & Defense Prep | Week 13+ | End-to-end testing, demo rehearsal, report/slides finalized |

This assumes a ~12–14 week runway; compress or stretch each milestone
proportionally once the actual defense date is confirmed.

### Weekly leadership cadence

- **Workflow:** `git checkout -b <type>/<member-name>/<short-description>` → `git push` → open PR to `main` → resolve conversations → obtain 1 approval from leader (stale dismissed on push) → squash-merge. Never push directly to `main` after Ruleset active. See `CONTRIBUTING.md` for full spec and branch types (`feat/ fix/ docs/ refactor/ test/ chore/`).
- **Monday — sprint planning** (every 2 weeks, 30 min) or quick sync (off
  weeks): review the current milestone, pull the next chunk of work from
  Backlog into "This Sprint," let people claim 1–2 issues in their track
  rather than being assigned top-down.
- **Daily — async one-line updates** in a #standup channel: what moved
  yesterday, what's happening today, any blocker. Replaces a daily meeting.
- **Wednesday/Thursday — 15-min live sync**: unblock anyone stuck more than
  a day; keep it short if async updates already cover the ground.
- **As PRs open — review within 24 hours, leader is final approver**: every PR to `main` requires **1 approval from the leader** (only `Admin`/bypass holder; stale approvals dismissed on new pushes, conversations must be resolved). Peers may review/comment for context, but cannot approve alone. For stronger enforcement, use a GitHub Organization + team containing only the leader.
- **Sunday — 15-min retro + board cleanup**: what went well, what slowed
  things down, what changes next sprint. Anything stuck "In Progress" for
  3+ sprints gets broken down or re-scoped, not left to linger.

### Leader's specific responsibilities (distinct from contributing code)

- Own the board's health — check weekly why any card hasn't moved.
- Break down each milestone into concrete issues *before* sprint planning,
  so planning is "pick from a ready list," not "figure out what to build."
- Protect the `services/api` contract — any schema change gets a heads-up
  before merging, since multiple services depend on it.
- Call scope cuts early. If a milestone is running late at a check-in,
  decide what drops to post-MVP rather than letting the whole timeline slip.

### Apps required

| Purpose | Tool |
|---|---|
| Board / issue tracking | GitHub Projects |
| Async daily updates | Discord or Slack |
| Weekly video sync | Google Meet / Zoom / Discord voice |
| Design handoff (UI/UX) | Figma |
| Documentation | `docs/` folder in this repo |

Issue template for consistent task write-ups: `.github/ISSUE_TEMPLATE.md`.

## 9. Key Decisions Log

- Web-based platform (Next.js), not mobile-first — screen/tab monitoring
  features don't translate to mobile OSes.
- Flutter proctor companion app: documented as future work, not built now.
- Repo name: `exam-integrity-system` — https://github.com/sayfeldinn/exam-integrity-system
- MVP narrows 20 features down to 5 core pillars (see Section 4) for the
  graduation deliverable; full feature set is the long-term roadmap.
- Monorepo structure adopted (Section 7); `services/api` and `apps/web`
  scaffolded first, other service folders added only once work starts there.
- Project management approach: Scrumban with GitHub Projects, 2-week
  sprints, milestone-per-MVP-pillar, weekly leadership cadence (Section 8).
- Sprint progress tracked separately from decisions: see `docs/PROGRESS_LOG.md`
  for weekly status, this section for durable decisions only.
- Branch workflow & protection (2026-09-02): Ruleset is active targeting `main` — restrict direct pushes/updates ✓, restrict deletions ✓, block force pushes ✓, require PR ✓, require 1 approval from leader (dismiss stale on push) ✓, require conversation resolution ✓. Bypass: only `Admin` (team leader) can bypass, mode **For pull requests only**; members have `Write` not `Admin` and cannot bypass/modify the Ruleset. Leader is the final reviewer/approver for every PR to `main`. Stronger enforcement via GitHub Organization + team containing only the leader was recommended.
- Branch naming convention (2026-09-02): `<type>/<member-name>/<short-description>` where `type` ∈ `{feat, fix, docs, refactor, test, chore}`. Examples: `feat/seif/agent-tool-calling`, `feat/ahmed/frontend`, `fix/sara/api-error-handling`, `docs/mohamed/project-documentation`. Documented as source of truth in `CONTRIBUTING.md`.
- Permissions model (2026-09-02): leader remains the only repository `Admin`; all other members are `Write`. Only the `Admin` can modify Rulesets. Workflow: `create branch <type>/<member-name>/<desc>` → `push` → `open PR to main` → `resolve conversations` → `leader approves` → `squash-merge`. Never push directly to `main` (initial `git push -u origin main` before Ruleset is the sole exception).
