import { Download } from 'lucide-react';
import { timeline } from '../../data.js';
import Avatar from '../../components/Avatar.jsx';
import Pill, { riskTone } from '../../components/Pill.jsx';

// half-circle gauge: the arc fills in proportion to the score
function Gauge({ score }) {
  const r = 38;
  const half = Math.PI * r;
  return (
    <div className="gauge">
      <svg width="104" height="72" viewBox="0 0 104 72" aria-hidden="true">
        <path d="M 14 56 A 38 38 0 0 1 90 56" fill="none" stroke="#eceff4" strokeWidth="10" strokeLinecap="round" />
        <path
          d="M 14 56 A 38 38 0 0 1 90 56"
          fill="none" stroke="#dc3545" strokeWidth="10" strokeLinecap="round"
          strokeDasharray={`${(score / 100) * half} ${half}`}
        />
        <text x="52" y="62" textAnchor="middle" fontSize="24" fontWeight="700" fill="#dc3545" fontFamily="Manrope, sans-serif">{score}</text>
      </svg>
      Risk Score
    </div>
  );
}

export default function Reports() {
  return (
    <div className="page">
      <div className="report">
        <div className="report-head">
          <div>
            <h2>Incident Report</h2>
            <p>Report ID: IR-20260929-001 · Generated: 10:52:14</p>
          </div>
          <button className="btn btn-outline" onClick={() => window.print()}>
            <Download size={16} /> Export PDF
          </button>
        </div>

        <section className="card report-card">
          <h3 className="report-title">Exam Information</h3>
          <div className="info-grid">
            <div><small>Exam</small><b>CS-401 · Machine Learning Midterm</b></div>
            <div><small>Date</small><b>September 29, 2026</b></div>
            <div><small>Time</small><b>09:30 AM – 12:00 PM</b></div>
            <div><small>Course</small><b>Introduction to Machine Learning</b></div>
            <div><small>Department</small><b>Computer Science</b></div>
            <div><small>Session ID</small><b>#EX-20260929-4821</b></div>
          </div>
        </section>

        <div className="report-pair">
          <section className="card report-card">
            <h3 className="report-title">Student Information</h3>
            <div className="student-line">
              <Avatar name="Ahmed Ali Hassan" size={46} />
              <div>
                <strong>Ahmed Ali Hassan</strong>
                <span className="sub-id">STU-2026-001</span>
              </div>
            </div>
            <div className="info-grid two">
              <div><small>Faculty</small><b>CS</b></div>
              <div><small>Year</small><b>3rd Year</b></div>
              <div><small>GPA</small><b>3.2</b></div>
              <div><small>Session</small><b>1h 17m</b></div>
            </div>
          </section>

          <section className="card report-card">
            <div className="assessment">
              <Gauge score={82} />
              <div>
                <h3 className="report-title" style={{ marginBottom: 10 }}>Final Assessment</h3>
                <Pill tone="high">High · 82</Pill>
                <p>4 violations detected.<br />High probability of academic misconduct.</p>
              </div>
            </div>
          </section>
        </div>

        <section className="card report-card">
          <h3 className="report-title">Violation Timeline</h3>
          <div className="table-wrap">
            <table className="table timeline-table">
              <thead>
                <tr><th>Time</th><th>Event Type</th><th>Severity</th><th>Confidence</th><th>Description</th></tr>
              </thead>
              <tbody>
                {timeline.map((row) => (
                  <tr key={row.time}>
                    <td className="stamp-cell">{row.time}</td>
                    <td>{row.event}</td>
                    <td><Pill tone={riskTone(row.level)}>{row.level}</Pill></td>
                    <td className="mono">{row.confidence}</td>
                    <td className="cell-muted">{row.text}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  );
}
