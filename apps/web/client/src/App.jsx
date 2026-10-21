import { useEffect } from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';

import SiteLayout from './components/SiteLayout.jsx';
import Home from './pages/Home.jsx';
import Product from './pages/Product.jsx';
import Contact from './pages/Contact.jsx';
import Mobile from './pages/Mobile.jsx';
import Health from './pages/Health.jsx';
import Login from './pages/student/Login.jsx';
import Verify from './pages/student/Verify.jsx';
import Permissions from './pages/student/Permissions.jsx';
import SystemCheck from './pages/student/SystemCheck.jsx';
import Exam from './pages/student/Exam.jsx';
import ProctorLayout from './pages/proctor/ProctorLayout.jsx';
import Dashboard from './pages/proctor/Dashboard.jsx';
import LiveMonitoring from './pages/proctor/LiveMonitoring.jsx';
import Exams from './pages/proctor/Exams.jsx';
import Students from './pages/proctor/Students.jsx';
import Violations from './pages/proctor/Violations.jsx';
import Reports from './pages/proctor/Reports.jsx';
import Analytics from './pages/proctor/Analytics.jsx';
import Assistant from './pages/proctor/Assistant.jsx';
import Settings from './pages/proctor/Settings.jsx';

export default function App() {
  const { pathname, hash } = useLocation();

  // jump back to the top on page change, unless we're heading to a #section
  useEffect(() => {
    if (!hash) window.scrollTo(0, 0);
  }, [pathname, hash]);

  return (
    <Routes>
      <Route element={<SiteLayout />}>
        <Route path="/" element={<Home />} />
        <Route path="/product" element={<Product />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/health" element={<Health />} />
      </Route>

      <Route path="/mobile" element={<Mobile />} />

      <Route path="/student/login" element={<Login />} />
      <Route path="/student/verify" element={<Verify />} />
      <Route path="/student/permissions" element={<Permissions />} />
      <Route path="/student/system-check" element={<SystemCheck />} />
      <Route path="/student/exam" element={<Exam />} />

      <Route path="/proctor" element={<ProctorLayout />}>
        <Route index element={<Navigate to="dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="live-monitoring" element={<LiveMonitoring />} />
        <Route path="exams" element={<Exams />} />
        <Route path="students" element={<Students />} />
        <Route path="violations" element={<Violations />} />
        <Route path="reports" element={<Reports />} />
        <Route path="analytics" element={<Analytics />} />
        <Route path="assistant" element={<Assistant />} />
        <Route path="settings" element={<Settings />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
