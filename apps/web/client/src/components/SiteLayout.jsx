import { Link, NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { Shield, Menu, X } from 'lucide-react';
import scrollToPicker from './scrollToPicker.js';

// Nav bar and footer shared by the home, product and contact pages.
export default function SiteLayout() {
  const [menuOpen, setMenuOpen] = useState(false);
  const { pathname } = useLocation();
  const navigate = useNavigate();

  // "Get Started" - "Try Demo" both lead to the interface picker on the home page
  function goToInterfaces(e) {
    e.preventDefault();
    setMenuOpen(false);
    if (pathname === '/') {
      scrollToPicker();
    } else {
      navigate('/#interfaces');
    }
  }
  const linkClass = ({ isActive }) => (isActive ? 'current' : '');

  return (
    <div className="site">
      <header className="site-nav">
        <div className="nav-inner">
          <Link to="/" className="site-logo" onClick={() => setMenuOpen(false)}>
            <span className="logo-mark"><Shield size={18} /></span>
            ExamGuard AI
          </Link>

          <nav className={`site-links ${menuOpen ? 'open' : ''}`}>
            <NavLink to="/product" className={linkClass} onClick={() => setMenuOpen(false)}>Our Product</NavLink>
            <a href="/#interfaces" onClick={goToInterfaces}>Try Demo</a>
            <NavLink to="/contact" className={linkClass} onClick={() => setMenuOpen(false)}>Contact</NavLink>
            <a href="/#interfaces" className="btn btn-teal nav-cta" onClick={goToInterfaces}>Get Started</a>
          </nav>

          <button className="nav-burger" aria-label="Toggle menu" onClick={() => setMenuOpen(!menuOpen)}>
            {menuOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>
      </header>

      <main className="site-main">
        <Outlet />
      </main>

      <footer className="site-footer">
        Faculty of Computers and Data Science, Alexandria University · Graduation Project 2026
      </footer>
    </div>
  );
}
