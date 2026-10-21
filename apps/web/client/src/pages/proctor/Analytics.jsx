import { Users, AlertCircle, TrendingUp, ClipboardList, ArrowUp, ArrowDown } from 'lucide-react';
import { violationTypes, riskDistribution, riskTrend } from '../../data.js';

const stats = [
  { label: 'Students Monitored', value: '1,284', icon: Users,         tone: 'blue',  trend: '+8%', up: true },
  { label: 'Total Violations',   value: '342',   icon: AlertCircle,   tone: 'red',   note: 'Last 30 days' },
  { label: 'Avg Risk Score',     value: '31.4',  icon: TrendingUp,    tone: 'amber', trend: '−5%', up: false },
  { label: 'Exams Conducted',    value: '47',    icon: ClipboardList, tone: 'green', note: 'This semester' },
];

// builds the line + shaded area for the risk trend chart
function TrendChart({ values }) {
  const width = 400, height = 110, pad = 12;
  const min = 25, max = 50;
  const points = values.map((v, i) => [
    pad + (i / (values.length - 1)) * (width - pad * 2),
    height - pad - ((v - min) / (max - min)) * (height - pad * 2),
  ]);
  const line = points.map(([x, y]) => `${x},${y}`).join(' ');
  const area = `${pad},${height} ${line} ${width - pad},${height}`;

  return (
    <svg viewBox={`0 0 ${width} ${height}`} style={{ width: '100%', maxWidth: 420, display: 'block', margin: '8px auto 0' }} role="img" aria-label="Average risk score over the last 12 exam sessions">
      <defs>
        <linearGradient id="trendFill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#3b82f6" stopOpacity="0.22" />
          <stop offset="1" stopColor="#3b82f6" stopOpacity="0" />
        </linearGradient>
      </defs>
      <polygon points={area} fill="url(#trendFill)" />
      <polyline points={line} fill="none" stroke="#3b82f6" strokeWidth="2.5" strokeLinejoin="round" />
      {points.map(([x, y], i) => <circle key={i} cx={x} cy={y} r="3.6" fill="#3b82f6" />)}
    </svg>
  );
}

export default function Analytics() {
  const tallest = Math.max(...violationTypes.map(([, n]) => n));

  return (
    <div className="page">
      <div className="stat-grid">
        {stats.map(({ label, value, icon: Icon, tone, trend, up, note }) => (
          <div className="card stat" key={label} style={{ minHeight: 170 }}>
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

      <div className="chart-grid">
        <section className="card chart-card">
          <h3>Violation Types — Last 30 Days</h3>
          <div className="bar-chart">
            {violationTypes.map(([label, count]) => (
              <div className="bar-col" key={label}>
                <div className="bar-value">{count}</div>
                <div className="bar" style={{ height: (count / tallest) * 124 }} />
                <div className="bar-label">{label}</div>
              </div>
            ))}
          </div>
        </section>

        <section className="card chart-card">
          <h3>Risk Distribution</h3>
          {riskDistribution.map((row) => (
            <div className="dist-row" key={row.label}>
              <div className="dist-top"><span>{row.label}</span><span>{row.value}%</span></div>
              <div className="dist-track"><div className="dist-fill" style={{ width: `${row.value}%`, background: row.color }} /></div>
            </div>
          ))}
        </section>
      </div>

      <section className="card chart-card">
        <h3>Average Risk Score Trend</h3>
        <p>Last 12 exam sessions</p>
        <TrendChart values={riskTrend} />
      </section>
    </div>
  );
}
