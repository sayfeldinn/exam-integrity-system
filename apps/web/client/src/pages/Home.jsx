import { useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { GraduationCap, Monitor, Smartphone, ArrowRight } from 'lucide-react';
import scrollToPicker from '../components/scrollToPicker.js';

const interfaces = [
  { to: '/student/login',     icon: GraduationCap, title: 'Student Web App',    text: 'Take exams securely from any browser.' },
  { to: '/proctor/dashboard', icon: Monitor,       title: 'Proctor Dashboard',  text: 'Monitor sessions and review AI alerts.' },
  { to: '/mobile',            icon: Smartphone,    title: 'Proctor Mobile App', text: 'Get live alerts and act on the go.' },
];

export default function Home() {
  const { hash } = useLocation();

  // coming back from a demo screen via "Interface Selector" lands on the picker
  useEffect(() => {
    if (hash === '#interfaces') scrollToPicker(false);
  }, [hash]);

  return (
    <>
      <section className="hero">
        <span className="hero-badge">AI-Powered Exam Integrity</span>
        <h1>Fair and Secure <br></br> Online Exams,<em>Powered <br></br> by AI</em></h1>
        <p>ExamGuard AI monitors exams in real time, so students can focus on their answers and proctors can focus on real risks.</p>
        <div className="hero-buttons">
          <a href="#interfaces" className="btn btn-teal btn-lg" onClick={(e) => { e.preventDefault(); scrollToPicker(); }}>Get Started</a>
          <Link to="/product" className="btn btn-dark btn-lg">Learn More</Link>
        </div>
      </section>

      <section className="interfaces" id="interfaces">
        <div className="container">
          <h2 className="section-title">Choose your interface</h2>
          <div className="interface-grid">
            {interfaces.map(({ to, icon: Icon, title, text }) => (
              <Link to={to} className="tile interface-tile" key={title}>
                <span className="tile-icon"><Icon size={22} /></span>
                <h3>{title}</h3>
                <p>{text}</p>
                <ArrowRight size={16} className="tile-arrow" />
              </Link>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
