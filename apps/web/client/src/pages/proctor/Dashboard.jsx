import { Link } from 'react-router-dom';
import { Users, AlertCircle, Bell, TrendingUp, Monitor, Eye, Plus, ArrowUp, ArrowDown } from 'lucide-react';
import { students, alerts, exams } from '../../data.js';
import Avatar from '../../components/Avatar.jsx';
import Pill, { riskTone } from '../../components/Pill.jsx';

const stats = [
  { label: 'Students Online', value: 240, note: '',                    icon: Users,       tone: 'blue',  trend: '+12', up: true },
  { label: 'High Risk',       value: 8,   note: 'Requires attention',  icon: AlertCircle, tone: 'red' },
  { label: 'Active Alerts',   value: 5,   note: 'In the last 10 min',  icon: Bell,        tone: 'amber' },
  { label: 'Avg Risk Score',  value: 31,  note: 'Across all students', icon: TrendingUp,  tone: 'green', trend: '−4', up: false },
];

export default function Dashboard() {
  const todayExams = exams.slice(0, 3);

  return (
    <div className="page">
      <div className="exam-banner">
        <div>
          <div className="banner-tag"><i /> 2 ACTIVE EXAMS</div>
          <h2>CS-401 Machine Learning Midterm</h2>
          <p>142 students · Ends at 12:00 PM · 1h 13m remaining</p>
        </div>
        <div className="banner-actions">
          <Link to="/proctor/live-monitoring" className="btn banner-white"><Monitor size={16} /> Monitor</Link>
          <Link to="/proctor/exams" className="btn banner-glass">View Details</Link>
        </div>
      </div>

      <div className="stat-grid">
        {stats.map(({ label, value, note, icon: Icon, tone, trend, up }) => (
          <div className="card stat" key={label}>
            <div className="stat-top">
              <span className={`stat-icon tone-${tone}`}><Icon size={19} /></span>
              {trend && (
                <span className={`trend ${up ? 'trend-up' : 'trend-down'}`}>
                  {up ? <ArrowUp size={13} /> : <ArrowDown size={13} />} {trend}
                </span>
              )}
            </div>
            <div className="stat-number">{value}</div>
            <div className="stat-label">{label}</div>
            {note && <div className="stat-note">{note}</div>}
          </div>
        ))}
      </div>

      <div className="dash-grid">
        <section className="card">
          <div className="card-head">
            <div>
              <h3>Live Students</h3>
              <p>CS-401 Midterm · Real-time monitoring</p>
            </div>
            <Link to="/proctor/live-monitoring" className="btn btn-outline btn-small"><Monitor size={14} /> Full View</Link>
          </div>
          <div className="table-wrap">
            <table className="table">
              <thead>
                <tr>
                  <th>Student</th><th>Risk</th><th>Violations</th><th>Status</th><th>Last Event</th><th />
                </tr>
              </thead>
              <tbody>
                {students.slice(0, 5).map((s) => (
                  <tr key={s.id}>
                    <td>
                      <div className="cell-person">
                        <Avatar name={s.name} color={s.color} />
                        <div><strong>{s.name}</strong><span className="sub-id">{s.id}</span></div>
                      </div>
                    </td>
                    <td><Pill tone={riskTone(s.level)}>{s.level} · {s.score}</Pill></td>
                    <td className="mono">{s.violations}</td>
                    <td><Pill tone="online">Online</Pill></td>
                    <td className="cell-muted">{s.lastEvent}<span className="stamp">{s.time}</span></td>
                    <td>
                      <Link to="/proctor/live-monitoring" className="row-actions btn-ghost btn" style={{ color: '#4b5565', fontSize: 13 }}>
                        <Eye size={15} /> View
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="card">
          <div className="card-head">
            <h3>Recent Alerts</h3>
            <Link to="/proctor/violations" className="link-btn">View all</Link>
          </div>
          {alerts.map((a) => (
            <div className="alert-row" key={a.title + a.student}>
              <div className="alert-row-top">
                <strong>{a.title}</strong>
                <Pill tone={riskTone(a.level)}>{a.level}</Pill>
              </div>
              <p>{a.student}</p>
              <span className="alert-meta">{a.time} · {a.confidence}% conf.</span>
            </div>
          ))}
        </section>
      </div>

      <section className="card" style={{ marginTop: 24 }}>
        <div className="card-head">
          <h3>Active Exams Today</h3>
          <Link to="/proctor/exams" className="btn btn-outline btn-small"><Plus size={14} /> Manage Exams</Link>
        </div>
        <div className="today-list">
          {todayExams.map((e) => (
            <div className="today-card" key={e.id}>
              <div className="today-top">
                <Pill tone={e.status.toLowerCase()}>{e.status}</Pill>
                <span className="mono" style={{ fontSize: 12, color: '#9aa3b5' }}>{e.id}</span>
              </div>
              <strong>{e.name}</strong>
              <p>{e.students} students · {e.schedule.replace(' – ', '–')}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
