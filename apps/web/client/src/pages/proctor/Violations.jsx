import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Smartphone, Download, Flag } from 'lucide-react';
import { alerts } from '../../data.js';
import Pill, { riskTone } from '../../components/Pill.jsx';

const filters = ['All', 'High Risk', 'Medium', 'Low', 'Unread'];

// icon tile colours for each severity
const tiles = {
  High:   { background: '#fbdde1', color: '#d3000d' },
  Review: { background: '#fdf0c0', color: '#d9820b' },
  Low:    { background: '#dbe6fb', color: '#1a56f0' },
};

export default function Violations() {
  const [filter, setFilter] = useState('All');
  const [flagged, setFlagged] = useState([]);

  const visible = alerts.filter((a) => {
    if (filter === 'High Risk') return a.level === 'High';
    if (filter === 'Medium') return a.level === 'Review';
    if (filter === 'Low') return a.level === 'Low';
    if (filter === 'Unread') return a.level !== 'Low';
    return true;
  });

  function toggleFlag(key) {
    setFlagged(flagged.includes(key) ? flagged.filter((k) => k !== key) : [...flagged, key]);
  }

  return (
    <div className="page">
      <div className="toolbar">
        <div className="tabs">
          {filters.map((f) => (
            <button key={f} className={`tab ${filter === f ? 'on' : ''}`} onClick={() => setFilter(f)}>{f}</button>
          ))}
        </div>
        <button className="btn btn-outline btn-small"><Download size={14} /> Export</button>
      </div>

      {visible.map((a) => {
        const key = a.title + a.student;
        return (
          <div className="card alert-card" key={key}>
            <span className="alert-icon" style={tiles[a.level]}><Smartphone size={18} /></span>
            <div className="alert-body">
              <div className="alert-title">
                <strong>{a.title}</strong>
                <Pill tone={riskTone(a.level)}>{a.level}</Pill>
              </div>
              <div className="alert-name">{a.student}</div>
              <div className="alert-text">{a.text}</div>
            </div>
            <div className="alert-side">
              <div className="alert-time">{a.time}</div>
              <div className="alert-conf">{a.confidence}% confidence</div>
              <div className="alert-buttons">
                <Link to="/proctor/reports" className="btn btn-outline btn-small">Review</Link>
                <button className="btn btn-blue btn-small" onClick={() => toggleFlag(key)}>
                  <Flag size={13} /> {flagged.includes(key) ? 'Flagged' : 'Flag'}
                </button>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
