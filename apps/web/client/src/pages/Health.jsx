import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Activity, AlertTriangle, CheckCircle2, RefreshCw, XCircle } from 'lucide-react';

import { getHealth, API_URL } from '../lib/api';

// Module-scope helper so the mount effect never calls setState synchronously
// (react-hooks/set-state-in-effect). Returns null on abort.
async function fetchHealth(signal) {
  try {
    return { data: await getHealth(signal) };
  } catch (err) {
    if (err.name === 'AbortError') return null;
    return { error: err };
  }
}

// M0-23: client-side health check against the real backend.
// Three rendered states: ok (green), degraded (amber, API up but DB down),
// unreachable (red — "API unreachable" with a hint).
export default function Health() {
  const [state, setState] = useState('loading'); // loading | ok | degraded | unreachable
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  function apply(res) {
    if (!res) return; // aborted
    if (res.error) {
      setError(res.error.message);
      setState('unreachable');
    } else {
      setResult(res.data);
      setState(res.data.status === 'ok' ? 'ok' : 'degraded');
    }
  }

  async function check() {
    setState('loading');
    setError(null);
    apply(await fetchHealth());
  }

  useEffect(() => {
    const controller = new AbortController();
    (async () => apply(await fetchHealth(controller.signal)))();
    return () => controller.abort();
  }, []);

  return (
    <div className="container health-page">
      <header className="page-intro">
        <h1>System status</h1>
        <p>Live health check of the Exam Integrity API ({API_URL}).</p>
      </header>

      <section className={`tile health-card health-${state}`} role="status" aria-live="polite">
        {state === 'loading' && (
          <p className="health-loading">
            <RefreshCw size={20} className="spin" /> Contacting the API…
          </p>
        )}

        {state === 'ok' && (
          <>
            <div className="health-icon ok">
              <CheckCircle2 size={30} strokeWidth={2.5} />
            </div>
            <h2>API is healthy</h2>
            <p>Database: {result?.database}</p>
          </>
        )}

        {state === 'degraded' && (
          <>
            <div className="health-icon warn">
              <AlertTriangle size={30} strokeWidth={2.5} />
            </div>
            <h2>API is up — database degraded</h2>
            <p>{result?.database}</p>
          </>
        )}

        {state === 'unreachable' && (
          <>
            <div className="health-icon err">
              <XCircle size={30} strokeWidth={2.5} />
            </div>
            <h2>API unreachable — check `docker logs api`</h2>
            <p>{error}</p>
            <p className="health-hint">
              Start the backend:{' '}
              <code>cd services/api && uv run uvicorn main:app --reload --port 8000</code>
            </p>
          </>
        )}

        <div className="health-actions">
          <button className="btn btn-teal" type="button" onClick={check} disabled={state === 'loading'}>
            <Activity size={16} /> Re-check
          </button>
          <Link to="/" className="btn btn-dark">
            Back home
          </Link>
        </div>
      </section>
    </div>
  );
}
