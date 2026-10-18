// Small rounded label with a coloured dot, used for risk levels and statuses.
// `tone` is one of: high, review, normal, low, live, scheduled, completed, online.
export default function Pill({ tone, children }) {
  return (
    <span className={`pill pill-${tone}`}>
      <i className="pill-dot" />
      {children}
    </span>
  );
}

export function riskTone(level) {
  return level.toLowerCase();
}
