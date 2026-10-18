import { initials } from '../data.js';

export default function Avatar({ name, color = '#3b82f6', size = 32 }) {
  return (
    <span
      className="avatar"
      style={{ background: color, width: size, height: size, fontSize: size * 0.34 }}
    >
      {initials(name)}
    </span>
  );
}
