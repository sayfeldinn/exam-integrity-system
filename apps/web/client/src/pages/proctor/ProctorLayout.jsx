import { useState } from 'react';
import { NavLink, Outlet, useLocation } from 'react-router-dom';
import {
  Home, Monitor, ClipboardList, Users, AlertCircle, FileText, BarChart3,
  Brain, Settings, Bell, Menu, Shield,
} from 'lucide-react';
import InterfaceSelector from '../../components/InterfaceSelector.jsx';
import Avatar from '../../components/Avatar.jsx';

const navItems = [
  { to: 'dashboard',       label: 'Dashboard',       icon: Home },
  { to: 'live-monitoring', label: 'Live Monitoring', icon: Monitor, badge: 2 },
  { to: 'exams',           label: 'Exams',           icon: ClipboardList },
  { to: 'students',        label: 'Students',        icon: Users },
  { to: 'violations',      label: 'Violations',      icon: AlertCircle, badge: 5 },
  { to: 'reports',         label: 'Reports',         icon: FileText },
  { to: 'analytics',       label: 'Analytics',       icon: BarChart3 },
  { to: 'assistant',       label: 'AI Assistant',    icon: Brain },
  { to: 'settings',        label: 'Settings',        icon: Settings },
];

// what the top bar shows for each page
const headings = {
  dashboard:         ['Dashboard', 'September 29, 2026 · 2 active exams'],
  'live-monitoring': ['Live Monitoring', 'CS-401 Machine Learning Midterm · 240 students'],
  exams:             ['Exam Management'],
  students:          ['Students', '240 students across active exams'],
  violations:        ['Violations & Alerts', '5 new alerts in the last 10 minutes'],
  reports:           ['Incident Reports'],
  analytics:         ['Analytics', 'Current semester overview'],
  assistant:         ['AI Assistant', 'Powered by ExamGuard Intelligence'],
  settings:          ['Settings', 'Manage your proctor preferences'],
};

export default function ProctorLayout() {
  const [menuOpen, setMenuOpen] = useState(false);
  const section = useLocation().pathname.split('/')[2] || 'dashboard';
  const [title, subtitle] = headings[section] || headings.dashboard;

  return (
    <div className="proctor">
      <InterfaceSelector />

      <aside className={`sidebar ${menuOpen ? 'open' : ''}`}>
        <div className="side-brand">
          <span className="brand-mark"><Shield size={18} /></span>
          <div>
            <strong>ExamGuard AI</strong>
            <small>Proctor Dashboard</small>
          </div>
        </div>

        <div className="side-label">MAIN</div>
        <nav className="side-nav">
          {navItems.map(({ to, label, icon: Icon, badge }) => (
            <NavLink
              key={to}
              to={`/proctor/${to}`}
              className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
              onClick={() => setMenuOpen(false)}
            >
              <Icon size={18} />
              {label}
              {badge && <span className="nav-badge">{badge}</span>}
            </NavLink>
          ))}
        </nav>

        <div className="side-user">
          <Avatar name="Dr Mona" color="#f39906" size={36} />
          <div>
            <strong>Dr. Mona Al-Said</strong>
            <small>Senior Proctor</small>
          </div>
        </div>
      </aside>

      <div className="proctor-main">
        <header className={`topbar ${subtitle ? 'with-sub' : ''}`}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <button className="menu-toggle" aria-label="Open menu" onClick={() => setMenuOpen(!menuOpen)}>
              <Menu size={22} />
            </button>
            <div>
              <h1>{title}</h1>
              {subtitle && <p>{subtitle}</p>}
            </div>
          </div>
          <div className="topbar-right">
            <span className="bell"><Bell size={19} /></span>
            <Avatar name="Dr Mona" color="#f39906" size={36} />
          </div>
        </header>

        <Outlet />
      </div>
    </div>
  );
}
