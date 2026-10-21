/**
 * Typed API client for the Exam Integrity System backend.
 *
 * M0-19/M0-23: consumes the frozen contract (docs/API_CONTRACT.md) and the
 * canonical shared types (packages/shared/types) — type-only imports, so the
 * existing JSX app needs no TypeScript migration.
 *
 * Base URL comes from VITE_API_URL (see .env.example); the browser must reach
 * this URL directly — no server proxy (M0-24 CORS verification).
 */
import type { ExamSession } from '../../../../../packages/shared/types/session';
import type { Violation } from '../../../../../packages/shared/types/violation';

export const API_URL: string = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

export interface HealthResponse {
  status: 'ok' | 'degraded';
  database: string;
}

export interface SessionsResponse {
  sessions: ExamSession[];
}

export interface ViolationsResponse {
  violations: Violation[];
}

/** The API host did not respond at all (down, wrong port, CORS block, network). */
export class ApiUnreachableError extends Error {
  constructor(url: string) {
    super(`Could not reach the API at ${url}. Is the backend running?`);
    this.name = 'ApiUnreachableError';
  }
}

async function request<T>(path: string, signal?: AbortSignal): Promise<T> {
  const url = `${API_URL}${path}`;
  let res: Response;
  try {
    res = await fetch(url, { signal, headers: { Accept: 'application/json' } });
  } catch {
    // fetch rejects on network failure AND on CORS blocks — both mean
    // "unreachable from the browser" for the caller.
    throw new ApiUnreachableError(url);
  }
  if (!res.ok) {
    throw new Error(`API ${url} responded with ${res.status} ${res.statusText}`);
  }
  return (await res.json()) as T;
}

/** GET /api/v1/health — public, no auth (contract: docs/API_CONTRACT.md). */
export function getHealth(signal?: AbortSignal): Promise<HealthResponse> {
  return request<HealthResponse>('/api/v1/health', signal);
}

/** GET /api/v1/students/{student_id}/sessions */
export async function getStudentSessions(
  studentId: string,
  signal?: AbortSignal,
): Promise<ExamSession[]> {
  const data = await request<SessionsResponse>(
    `/api/v1/students/${encodeURIComponent(studentId)}/sessions`,
    signal,
  );
  return data.sessions;
}

/** GET /api/v1/sessions/{session_id}/violations */
export async function getSessionViolations(
  sessionId: string,
  signal?: AbortSignal,
): Promise<Violation[]> {
  const data = await request<ViolationsResponse>(
    `/api/v1/sessions/${encodeURIComponent(sessionId)}/violations`,
    signal,
  );
  return data.violations;
}
