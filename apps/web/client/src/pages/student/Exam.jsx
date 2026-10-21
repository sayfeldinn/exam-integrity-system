import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Check, Camera, Mic, Activity, ChevronRight, ChevronLeft } from 'lucide-react';
import InterfaceSelector from '../../components/InterfaceSelector.jsx';
import { questions } from '../../data.js';

const LETTERS = ['A', 'B', 'C', 'D'];
const EXAM_SECONDS = 90 * 60;

function formatTime(total) {
  const h = Math.floor(total / 3600);
  const m = Math.floor((total % 3600) / 60);
  const s = total % 60;
  return [h, m, s].map((n) => String(n).padStart(2, '0')).join(':');
}

export default function Exam() {
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState({}); // question index -> option index
  const [secondsLeft, setSecondsLeft] = useState(EXAM_SECONDS);
  const [confirming, setConfirming] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    if (submitted) return;
    const timer = setInterval(() => setSecondsLeft((s) => Math.max(0, s - 1)), 1000);
    return () => clearInterval(timer);
  }, [submitted]);

  const answeredCount = Object.keys(answers).length;
  const unanswered = questions.length - answeredCount;
  const q = questions[current];

  if (submitted) {
    return (
      <div className="student-page">
        <InterfaceSelector />
        <div className="student-wrap">
          <div className="logo-tile" style={{ background: '#12a35f', color: '#fff' }}><Check size={26} /></div>
          <h1>Exam submitted</h1>
          <p className="student-tag">Your {answeredCount} answers were recorded. Your proctor will review the session.</p>
          <Link to="/" className="btn btn-blue">Back to home</Link>
        </div>
      </div>
    );
  }

  return (
    <div style={{ background: 'var(--page)', minHeight: '100vh' }}>
      <InterfaceSelector />

      <header className="exam-bar">
        <div>
          <strong>Machine Learning</strong>
          <small>CS-401 · Spring 2026</small>
        </div>
        <div className="exam-right">
          <span className="monitoring">Monitoring Active</span>
          <span className="timer">{formatTime(secondsLeft)}</span>
          <button className="btn btn-red btn-small" onClick={() => setConfirming(true)}>Submit Exam</button>
        </div>
      </header>

      <div className="exam-body">
        <main className="exam-main">
          <div className="exam-meta">
            <span>Question {current + 1} of {questions.length}</span>
            <span>{answeredCount} answered · {unanswered} remaining</span>
          </div>
          <div className="progress"><i style={{ width: `${((current + 1) / questions.length) * 100}%` }} /></div>

          <span className="q-tag">QUESTION {current + 1}</span>
          <h2>{q.text}</h2>

          {q.options.map((text, i) => (
            <button
              key={text}
              className={`option ${answers[current] === i ? 'picked' : ''}`}
              onClick={() => setAnswers({ ...answers, [current]: i })}
            >
              <b>{LETTERS[i]}</b>
              {text}
            </button>
          ))}

          <div className="exam-nav">
            <button className="btn btn-outline" disabled={current === 0} onClick={() => setCurrent(current - 1)}>
              <ChevronLeft size={15} /> Previous
            </button>
            <button className="btn btn-blue" disabled={current === questions.length - 1} onClick={() => setCurrent(current + 1)}>
              Next Question <ChevronRight size={15} />
            </button>
          </div>
        </main>

        <aside className="exam-side">
          <p className="side-title">MONITORING</p>
          <div className="monitor-row"><span><Camera size={14} /> Camera</span><b>Active</b></div>
          <div className="monitor-row"><span><Mic size={14} /> Microphone</span><b>Active</b></div>
          <div className="monitor-row"><span><Activity size={14} /> AI Proctoring</span><b>Active</b></div>

          <p className="side-title" style={{ marginTop: 26 }}>QUESTIONS</p>
          <div className="q-grid">
            {questions.map((_, i) => (
              <button
                key={i}
                aria-label={`Question ${i + 1}`}
                className={i === current ? 'current' : answers[i] !== undefined ? 'answered' : ''}
                onClick={() => setCurrent(i)}
              >
                {i + 1}
              </button>
            ))}
          </div>
          <div className="legend">
            <span><i /> Current</span>
            <span><i className="green" /> Answered</span>
          </div>
        </aside>
      </div>

      {confirming && (
        <div className="confirm-overlay" role="dialog" aria-modal="true">
          <div className="confirm-box">
            <h3>Submit Exam?</h3>
            <p>Please review your progress before submitting.</p>
            <div className="count-pair">
              <div className="answered-box"><b>{answeredCount}</b>Answered</div>
              <div className="left-box"><b>{unanswered}</b>Unanswered</div>
            </div>
            <p>Time remaining: <span className="mono">{formatTime(secondsLeft)}</span></p>
            <div className="confirm-actions">
              <button className="btn btn-outline" onClick={() => setConfirming(false)}>Cancel</button>
              <button className="btn btn-red" onClick={() => setSubmitted(true)}>Submit Exam</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
