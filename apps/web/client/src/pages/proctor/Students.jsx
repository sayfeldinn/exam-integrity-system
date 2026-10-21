import { useState } from 'react';
import { Search } from 'lucide-react';
import { students } from '../../data.js';
import Avatar from '../../components/Avatar.jsx';
import Pill, { riskTone } from '../../components/Pill.jsx';

export default function Students() {
  const [query, setQuery] = useState('');
  const matches = students.filter((s) =>
    `${s.name} ${s.id}`.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="page">
      <div className="toolbar">
        <div className="search-box">
          <Search size={15} />
          <input
            aria-label="Search students"
            placeholder="Search students, exams..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>
      </div>

      <div className="card table-wrap">
        <table className="table">
          <thead>
            <tr><th>Student</th><th>Risk</th><th>Violations</th><th>Last Event</th></tr>
          </thead>
          <tbody>
            {matches.map((s) => (
              <tr key={s.id}>
                <td>
                  <div className="cell-person">
                    <Avatar name={s.name} color={s.color} />
                    <div><strong style={{ maxWidth: 'none' }}>{s.name}</strong><span className="sub-id">{s.id}</span></div>
                  </div>
                </td>
                <td><Pill tone={riskTone(s.level)}>{s.level} · {s.score}</Pill></td>
                <td className="mono">{s.violations}</td>
                <td className="cell-muted">{s.lastEvent}<span className="stamp">{s.time}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
        {matches.length === 0 && <p className="empty-note">No students match "{query}".</p>}
      </div>
    </div>
  );
}
