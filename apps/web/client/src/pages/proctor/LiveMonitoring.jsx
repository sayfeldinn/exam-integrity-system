import { useState } from 'react';
import { LayoutGrid, List, User, Video, Eye, Flag } from 'lucide-react';
import { students } from '../../data.js';
import Avatar from '../../components/Avatar.jsx';
import Pill, { riskTone } from '../../components/Pill.jsx';

const filters = ['All', 'High Risk', 'Online'];

function scoreClass(level) {
  if (level === 'High') return 'cam-score-high';
  if (level === 'Review') return 'cam-score-review';
  return 'cam-score-ok';
}

function barColor(score) {
  if (score >= 80) return '#e11d48';
  if (score >= 60) return '#f5b800';
  return '#22c88a';
}

export default function LiveMonitoring() {
  const [filter, setFilter] = useState('All');
  const [view, setView] = useState('grid');

  const visible = students.filter((s) => {
    if (filter === 'High Risk') return s.level === 'High';
    if (filter === 'Online') return !s.offline;
    return true;
  });

  return (
    <div className="page">
      <div className="toolbar">
        <div className="tabs">
          {filters.map((f) => (
            <button key={f} className={`tab ${filter === f ? 'on' : ''}`} onClick={() => setFilter(f)}>{f}</button>
          ))}
        </div>
        <div className="view-toggle">
          <button className={`toggle-btn ${view === 'grid' ? 'on' : ''}`} aria-label="Grid view" onClick={() => setView('grid')}><LayoutGrid size={17} /></button>
          <button className={`toggle-btn ${view === 'list' ? 'on' : ''}`} aria-label="List view" onClick={() => setView('list')}><List size={17} /></button>
        </div>
      </div>

      {view === 'grid' ? (
        <div className="cam-grid">
          {visible.map((s) => (
            <div className="cam-card" key={s.id}>
              <div className={`cam-view is-${s.level === 'High' ? 'high' : s.level === 'Review' ? 'review' : 'ok'}`}>
                {s.offline ? (
                  <div className="cam-offline"><Video size={22} />Camera Offline</div>
                ) : (
                  <>
                    <span className="cam-live"><i />LIVE</span>
                    <span className="cam-person"><User size={22} /></span>
                  </>
                )}
                <div className="cam-footer">
                  <span>{s.first}</span>
                  <span className={scoreClass(s.level)}>{s.score}</span>
                </div>
              </div>
              <div className="cam-info">
                <strong>{s.name}</strong>
                <span className="sub-id">{s.id}</span>
                <div className="cam-info-row">
                  <Pill tone={riskTone(s.level)}>{s.level} · {s.score}</Pill>
                  <span>{s.violations} violations</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card table-wrap">
          <table className="table">
            <thead>
              <tr><th>Student</th><th>Risk Score</th><th>Level</th><th>Violations</th><th>Status</th><th>Last Event</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {visible.map((s) => (
                <tr key={s.id}>
                  <td>
                    <div className="cell-person">
                      <Avatar name={s.name} color={s.color} size={30} />
                      <div><strong style={{ maxWidth: 'none' }}>{s.name}</strong><span className="sub-id">{s.id}</span></div>
                    </div>
                  </td>
                  <td>
                    <div className="score-bar">
                      <span className="score-track"><span className="score-fill" style={{ width: `${s.score}%`, background: barColor(s.score) }} /></span>
                      <span style={{ fontSize: 13 }}>{s.score}</span>
                    </div>
                  </td>
                  <td><Pill tone={riskTone(s.level)}>{s.level}</Pill></td>
                  <td>{s.violations}</td>
                  <td><Pill tone="online">{s.offline ? 'Offline' : 'Online'}</Pill></td>
                  <td className="cell-muted">{s.lastEvent}<span className="sub-id" style={{ marginLeft: 0 }}>{s.time}</span></td>
                  <td>
                    <div className="row-actions">
                      <button className="btn btn-ghost btn-small"><Eye size={14} /> Investigate</button>
                      <button className="btn btn-ghost btn-small"><Flag size={14} /> Flag</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
