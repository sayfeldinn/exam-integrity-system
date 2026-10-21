import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, User, Lock, Eye, EyeOff } from 'lucide-react';
import InterfaceSelector from '../../components/InterfaceSelector.jsx';

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  function signIn(e) {
    e.preventDefault();
    if (email.trim() && password.trim()) navigate('/student/verify');
  }

  return (
    <div className="student-page">
      <InterfaceSelector />
      <div className="student-wrap">
        <div className="logo-tile"><Shield size={26} /></div>
        <h1>ExamGuard AI</h1>
        <p className="student-tag">Online Proctoring Platform</p>

        <form className="panel" onSubmit={signIn}>
          <h2>Student Sign In</h2>

          <label className="field-label">Student ID / Email
            <div className="input-box">
              <User size={15} />
              <input
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="s.ahmed@university.edu"
                autoComplete="username"
              />
            </div>
          </label>

          <label className="field-label">Password
            <div className="input-box">
              <Lock size={15} />
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                autoComplete="current-password"
              />
              <button type="button" className="eye-btn" aria-label="Show or hide password" onClick={() => setShowPassword(!showPassword)}>
                {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </label>

          <div className="login-extras">
            <label><input type="checkbox" /> Remember me</label>
            <a href="#" onClick={(e) => e.preventDefault()}>Forgot password?</a>
          </div>

          <button className="btn btn-blue big-btn" disabled={!email.trim() || !password.trim()}>
            Sign In to Exam Portal
          </button>
        </form>

        <p className="student-foot">Al-Azhar University · Exam Management System v3.2</p>
      </div>
    </div>
  );
}
