export const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

// When "true", getHealth() returns a fake response and never calls the API.
const USE_MOCK = process.env.NEXT_PUBLIC_USE_MOCK === "true";

export type HealthResponse = { status: string };

export async function getHealth(): Promise<HealthResponse> {
  if (USE_MOCK) {
    return { status: "ok" };
  }

  const res = await fetch(`${API_URL}/api/v1/health`);
  if (!res.ok) throw new Error(`Health check failed: ${res.status}`);
  return res.json();
}