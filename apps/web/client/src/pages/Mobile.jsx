import { useState } from 'react';
import { Home, Bell, Users, ChevronRight } from 'lucide-react';
import InterfaceSelector from '../components/InterfaceSelector.jsx';
import Avatar from '../components/Avatar.jsx';
import Pill, { riskTone } from '../components/Pill.jsx';
import { alerts, students } from '../data.js';

const borderFor = { High: '#e91437', Review: '#f39906', Low: '#1a56f0' };

export default function Mobile() {
  const [tab, setTab] = useState('home');
  const highRisk = students.filter((s) => s.level === 'High');

  const tabs = [
    { key: 'home',     label: 'Home',     icon: Home },
    { key: 'alerts',   label: 'Alerts',   icon: Bell },
    { key: 'students', label: 'Students', icon: Users },
  ];

  return (
    <div className="mobile-stage">
      <InterfaceSelector />
      <div className="phone">
        <div className="phone-screen">
          <div className="m-header">
            <h2>CS-401 Machine Learning</h2>
            <small>Midterm Exam · Ends 12:00 PM</small>
            <div className="m-counts">
              <div className="m-count white"><b>5</b><small>Online</small></div>
              <div className="m-count red"><b>2</b><small>High Risk</small></div>
              <div className="m-count amber"><b>3</b><small>Alerts</small></div>
            </div>
          </div>

          <div className="m-body">
            {tab === 'home' && (
              <>
                <h3>Urgent Alerts <button className="m-more" style={{ background: 'none', border: 0 }} onClick={() => setTab('alerts')}>View all</button></h3>
                {alerts.filter((a) => a.level === 'High').map((a) => (
                  <div className="m-card" key={a.title + a.student}>
                    <strong>{a.title}</strong>
                    <small>{a.student}</small>
                    <Pill tone="high">High</Pill>
                  </div>
                ))}
                <h3>High Risk Students</h3>
                {highRisk.map((s) => (
                  <div className="m-card plain" key={s.id}>
                    <Avatar name={s.name} color={s.color} size={34} />
                    <div style={{ flex: 1 }}><strong>{s.name}</strong><small>{s.violations} violations</small></div>
                    <ChevronRight size={16} color="#9aa3b5" />
                  </div>
                ))}
              </>
            )}

            {tab === 'alerts' && (
              <>
                <h3>Alerts</h3>
                {alerts.map((a) => (
                  <div className="m-card" key={a.title + a.student} style={{ borderLeftColor: borderFor[a.level] }}>
                    <strong>{a.title}</strong>
                    <small>{a.student} · {a.time}</small>
                    <div className="m-actions">
                      <button className="btn btn-blue">Review</button>
                      <button className="btn btn-outline">Flag</button>
                    </div>
                  </div>
                ))}
              </>
            )}

            {tab === 'students' && (
              <>
                <h3>Students</h3>
                {students.map((s) => (
                  <div className="m-card plain" key={s.id}>
                    <Avatar name={s.name} color={s.color} size={34} />
                    <div style={{ flex: 1 }}><strong>{s.name}</strong><small>{s.id}</small></div>
                    <Pill tone={riskTone(s.level)}>{s.level} · {s.score}</Pill>
                  </div>
                ))}
              </>
            )}
          </div>

          <div className="m-tabs">
            {tabs.map(({ key, label, icon: Icon }) => (
              <button key={key} className={`m-tab ${tab === key ? 'on' : ''}`} onClick={() => setTab(key)}>
                <Icon size={18} />
                {label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
