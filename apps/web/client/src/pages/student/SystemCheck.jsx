import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Camera, Mic, Wifi, Globe, ScreenShare, Lock, Check, X, Loader2, AlertCircle, RefreshCw } from 'lucide-react';
import InterfaceSelector from '../../components/InterfaceSelector.jsx';
import Steps from '../../components/Steps.jsx';

// `failsFirst` rows fail on the first run and pass after "Retry Failed Checks" - just for the demo.
const checks = [
  { icon: Camera,      name: 'Camera',              ok: 'Webcam HD Camera' },
  { icon: Mic,         name: 'Microphone',          ok: 'Built-in Microphone', failsFirst: true },
  { icon: Wifi,        name: 'Internet Connection', ok: '32 Mbps — Excellent' },
  { icon: Globe,       name: 'Browser',             ok: 'Chrome — Compatible', failsFirst: true },
  { icon: ScreenShare, name: 'Screen Sharing',      ok: 'Enabled' },
  { icon: Lock,        name: 'Device Security',     ok: 'No threats detected' },
];

export default function SystemCheck() {
  const navigate = useNavigate();
  const [attempt, setAttempt] = useState(1);
  const [finished, setFinished] = useState(0); // how many rows have a result

  // reveal one result at a time
  useEffect(() => {
    if (finished >= checks.length) return;
    const timer = setTimeout(() => setFinished(finished + 1), 650);
    return () => clearTimeout(timer);
  }, [finished]);

  const failed = (c) => c.failsFirst && attempt === 1;
  const done = finished >= checks.length;
  const anyFailed = done && checks.some(failed);

  function retry() {
    setAttempt(2);
    setFinished(0);
  }

  return (
    <div className="student-page">
      <InterfaceSelector />
      <div className="student-wrap wide">
        <Steps current={4} title="System Check" subtitle="Verifying your device is ready for the exam session." />

        <div className="panel compact">
          {checks.map((c, i) => {
            const Icon = c.icon;
            const hasResult = i < finished;
            return (
              <div className="check-row" key={c.name}>
                <Icon size={17} />
                <div className="check-text">
                  <strong>{c.name}</strong>
                  <small>{!hasResult ? 'Checking...' : failed(c) ? 'Check failed' : c.ok}</small>
                </div>
                {!hasResult ? (
                  <Loader2 size={17} className="spin" />
                ) : failed(c) ? (
                  <span className="result fail"><X size={13} /></span>
                ) : (
                  <span className="result pass"><Check size={13} /></span>
                )}
              </div>
            );
          })}

          {anyFailed && (
            <div className="notice bad">
              <strong><AlertCircle size={15} /> Some checks failed</strong>
              <span>One or more system requirements could not be verified. Please resolve the issues and retry.</span>
            </div>
          )}

          {anyFailed ? (
            <button className="btn btn-outline big-btn" onClick={retry}><RefreshCw size={15} /> Retry Failed Checks</button>
          ) : (
            <button className="btn btn-blue big-btn" disabled={!done} onClick={() => navigate('/student/exam')}>
              {done ? 'Start Exam' : <><Loader2 size={16} className="spin" style={{ color: '#fff' }} /> Running system checks...</>}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
