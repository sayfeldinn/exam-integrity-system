# Onboarding — exam-integrity-system

> M0-4 skeleton + M0-28 verification `M0:110,167`.
> Run `scripts/verify-setup.sh` first; then `cp infra/.env.example infra/.env && docker compose -f infra/docker-compose.yml up --build`.

## 1. Prerequisites — OS Matrix

| OS | Setup | Notes |
|---|---|---|
| **Windows 10/11** | Enable WSL2 + install Docker Desktop (Hyper-V enabled, BIOS virtualization on). **Clone inside WSL** (`\\wsl$\...` is slow on Windows FS). `git config core.autocrlf input`. First `docker compose up --build` downloads 5-10 min. | Port `5432` often taken by local Postgres — compose maps to `5433` if conflict (see `infra/.env.example`). `node_modules` volume perf: use WSL FS. |
| **macOS (Intel/M1)** | Install Docker Desktop (enable Rosetta on M1), Xcode CLI `xcode-select --install`. Fix Postgres volume perms: `chmod 700 infra/pgdata` if `permission denied`. | Rosetta for `node:20-alpine` parity; `.env` perms `chmod 600`. |
| **Linux** | `sudo usermod -aG docker $USER && newgrp docker`, `docker compose version` ≥20. | `ports free` check in script. |

**Versions (pinned `M0-3` `M0:109`):** `node >=20` (`.nvmrc` 20), `python >=3.11` (`.python-version` 3.11.8), `docker >=20`, `git >=2.40`.

## 2. One-Command Setup

```bash
# 0. Verify toolchain
./scripts/verify-setup.sh              # Linux/macOS/WSL
# or Windows PowerShell:
powershell -ExecutionPolicy Bypass -File scripts\verify-setup.ps1

# 1. Env (never commit .env)
cp infra/.env.example infra/.env

# 2. Validate compose (no secrets needed)
docker compose -f infra/docker-compose.yml config

# 3. Build & start api+web+postgres (one command)
docker compose -f infra/docker-compose.yml up --build

# 4. Verify in browser + curl
curl http://localhost:8000/api/v1/health          # → {"status":"ok"}
curl http://localhost:8000/health                 # → 302 → /api/v1/health
# open http://localhost:3000 — page shows health result or "API unreachable"

# 5. DB check (in another terminal)
docker compose -f infra/docker-compose.yml exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB -c "\dt"  # 3 tables
docker compose -f infra/docker-compose.yml exec api alembic current  # == head
```

Fresh clone reproduction: `docker compose -f infra/docker-compose.yml down -v && up --build` passes on 2 OSes (DoD `M0:45`, Exit `M0:352`).

## 3. Standalone Dev (without Docker)

```bash
# api
cd services/api && uv sync  # or pip install -e .
uvicorn main:app --reload --port 8000

# web
cd apps/web && npm ci && npm run dev  # http://localhost:3000, needs NEXT_PUBLIC_API_URL=http://localhost:8000
```

CORS: `web` must **client-side `fetch(NEXT_PUBLIC_API_URL/api/v1/health)`** not server via Route Handler (hides CORS). CORS is backend `CORSMiddleware` allow `http://localhost:3000` `M0-16` `M0:133` — see `M0-24` `M0:152`.

## 4. Verify Scripts (M0-28)

`scripts/verify-setup.sh` checks: `node>=20`, `python>=3.11`, `docker>=20`, `git`, ports `3000/8000/5432` free, `.env` exists. Same for `.ps1` on Windows.

## 5. Branch Workflow (pointer)

Branch naming `<type>/<member-name>/<desc>` — see `CONTRIBUTING.md:1`

```
feat/seif/agent-tool-calling
```

Allowed `feat/ fix/ docs/ refactor/ test/ chore/` all with `<member-name>/`. Never push directly to `main` after Ruleset active.

## 6. Troubleshooting (updated from M0-33)

| Symptom | Fix |
|---|---|
| `port is already allocated 5432` | Change `POSTGRES_PORT=5433` in `infra/.env` or stop local Postgres. |
| `docker: permission denied` (Linux) | `sudo usermod -aG docker $USER && newgrp docker`, re-login. |
| `CRLF` vs `LF` in `.sh` fails on Linux | `git config core.autocrlf input`, re-checkout inside WSL. |
| `API unreachable` in web | Check `docker logs api`, `NEXT_PUBLIC_API_URL=http://localhost:8000` locally vs `http://api:8000` in compose network `M0-24`. |
| `alembic current` not head | `docker compose exec api alembic upgrade head`, check `psql \dt`. |
| Slow `node_modules` on Windows | Move clone inside WSL FS, not `C:\` mounted. |

Log fixes here + `docs/PROGRESS_LOG.md` (retro `M0:181`).

## 7. For Late Joiners

Same steps as §2. Ask sayfeldinn for `.env` values (never committed). See `docs/STARTING_PLAN.md:10-30` orientation and `docs/milestones/M0_IMPLEMENTATION_PLAN.md:30` placeholders.
