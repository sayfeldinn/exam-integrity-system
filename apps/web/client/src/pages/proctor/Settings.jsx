import { useState } from 'react';

const options = [
  { key: 'email', title: 'Email alerts',      note: 'Get an email when a High risk event is detected' },
  { key: 'sound', title: 'Sound alerts',      note: 'Play a sound for new violations' },
  { key: 'auto',  title: 'Auto-flag events',  note: 'Flag events above 90% confidence automatically' },
];

export default function Settings() {
  const [on, setOn] = useState({ email: true, sound: false, auto: true });

  return (
    <div className="page">
      <div className="card settings-card">
        {options.map((o) => (
          <label className="setting" key={o.key}>
            <span>
              <strong>{o.title}</strong>
              <small>{o.note}</small>
            </span>
            <span className="switch">
              <input
                type="checkbox"
                checked={on[o.key]}
                onChange={() => setOn({ ...on, [o.key]: !on[o.key] })}
              />
              <span />
            </span>
          </label>
        ))}
      </div>
    </div>
  );
}
