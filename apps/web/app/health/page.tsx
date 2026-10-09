"use client";

import { useEffect, useState } from "react";
import { API_URL, getHealth, type HealthResponse } from "@/lib/api";

type State =
  | { kind: "loading" }
  | { kind: "ok"; data: HealthResponse }
  | { kind: "error" };

export default function HealthPage() {
  const [state, setState] = useState<State>({ kind: "loading" });

  useEffect(() => {
    getHealth()
      .then((data) => setState({ kind: "ok", data }))
      .catch(() => setState({ kind: "error" }));
  }, []);

  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-semibold">API Health</h1>
      <p className="text-sm text-muted">
        Calling <code className="font-mono">{API_URL}/api/v1/health</code> from
        the browser.
      </p>

      {state.kind === "loading" && <p className="text-muted">Checking...</p>}

      {state.kind === "ok" && (
        <pre className="rounded-md border border-border bg-surface p-4 font-mono text-success">
          {JSON.stringify(state.data)}
        </pre>
      )}

      {state.kind === "error" && (
        <div className="rounded-md border border-border bg-surface p-4 text-danger">
          API unreachable — check <code className="font-mono">docker logs api</code>
        </div>
      )}
    </section>
  );
}