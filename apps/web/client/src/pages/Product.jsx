import { Link } from 'react-router-dom';
import { GraduationCap, Monitor, Building2, UserCheck, Eye, BarChart3, Bell } from 'lucide-react';

const features = [
  { icon: UserCheck, title: 'Identity Verification', text: 'Face detection confirms the student before the exam starts.' },
  { icon: Eye,       title: 'Real-Time Monitoring',  text: 'AI watches camera and screen activity during the exam.' },
  { icon: BarChart3, title: 'Smart Risk Scoring',    text: 'Suspicious events are ranked as Normal, Review, or High Risk.' },
  { icon: Bell,      title: 'Live Proctor Alerts',   text: 'Proctors are notified instantly on dashboard and mobile.' },
];

const steps = [
  { n: '01', title: 'Verify Identity',          text: 'The student logs in and confirms their identity via face detection before the exam begins.' },
  { n: '02', title: 'Take the exam',            text: 'The student answers questions in a clean, distraction-free browser interface.' },
  { n: '03', title: 'AI flags integrity risks', text: 'Suspicious behavior is detected and scored in real time; proctors receive instant alerts.' },
];

const audiences = [
  { icon: GraduationCap, title: 'Students',     text: 'A simple, guided exam flow with clear instructions at every step.' },
  { icon: Monitor,       title: 'Proctors',     text: 'A powerful dashboard to monitor, investigate, and act on AI alerts.' },
  { icon: Building2,     title: 'Institutions', text: 'Reports and analytics to maintain academic integrity at scale.' },
];

export default function Product() {
  return (
    <div className="container product">
      <header className="page-intro">
        <h1>Meet ExamGuard AI</h1>
        <p>One platform to verify, monitor, and report — from login to submission.</p>
      </header>

      <h2 className="bar-heading">Key Features</h2>
      <div className="feature-grid">
        {features.map(({ icon: Icon, title, text }) => (
          <div className="tile feature-tile" key={title}>
            <span className="tile-icon"><Icon size={22} /></span>
            <div>
              <h3>{title}</h3>
              <p>{text}</p>
            </div>
          </div>
        ))}
      </div>

      <h2 className="bar-heading">How It Works</h2>
      <div className="how-steps">
        {steps.map((s) => (
          <div className="how-step" key={s.n}>
            <b>{s.n}</b>
            <h3>{s.title}</h3>
            <p>{s.text}</p>
          </div>
        ))}
      </div>

      <h2 className="bar-heading">Who It's For</h2>
      <div className="audience-grid">
        {audiences.map(({ icon: Icon, title, text }) => (
          <div className="tile audience-tile" key={title}>
            <span className="tile-icon"><Icon size={24} /></span>
            <h3>{title}</h3>
            <p>{text}</p>
          </div>
        ))}
      </div>

      <div className="demo-cta">
        <Link to="/#interfaces" className="btn btn-teal btn-lg">Try the Demo</Link>
      </div>
    </div>
  );
}
