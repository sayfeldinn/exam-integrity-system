import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Camera, Mic, ScreenShare, Check, AlertCircle } from 'lucide-react';
import InterfaceSelector from '../../components/InterfaceSelector.jsx';
import Steps from '../../components/Steps.jsx';

const items = [
  { key: 'camera', icon: Camera,      title: 'Camera Access',     text: 'Used to verify your identity and monitor for suspicious activity during the exam.' },
  { key: 'mic',    icon: Mic,         title: 'Microphone Access', text: 'Used to detect unauthorized voice communication or external audio sources.' },
  { key: 'screen', icon: ScreenShare, title: 'Screen Sharing',    text: 'Allows proctors to detect if you switch tabs or open unauthorized applications.' },
];

export default function Permissions() {
  const navigate = useNavigate();
  const [status, setStatus] = useState({ camera: 'unset', mic: 'unset', screen: 'unset' });
  const set = (key, value) => setStatus({ ...status, [key]: value });
  const allGranted = Object.values(status).every((s) => s === 'allowed');

  return (
    <div className="student-page">
      <InterfaceSelector />
      <div className="student-wrap wide">
        <Steps current={3} title="Permission Setup" subtitle="ExamGuard requires access to the following to monitor your exam session." />

        <div className="panel compact">
          {items.map(({ key, icon: Icon, title, text }) => (
            <div className={`perm ${status[key] === 'allowed' ? 'granted' : ''}`} key={key}>
              <span className="perm-icon"><Icon size={17} /></span>
              <div className="perm-text"><strong>{title}</strong><small>{text}</small></div>
              <div className="perm-state">
                {status[key] === 'allowed' ? (
                  <span className="tag-small good"><Check size={11} style={{ verticalAlign: -1 }} /> Allowed</span>
                ) : (
                  <>
                    <span className="tag-small">{status[key] === 'denied' ? 'Denied' : 'Not Set'}</span>
                    <div className="perm-buttons">
                      <button className="btn btn-blue" onClick={() => set(key, 'allowed')}>Allow</button>
                      <button className="btn btn-outline" onClick={() => set(key, 'denied')}>Deny</button>
                    </div>
                  </>
                )}
              </div>
            </div>
          ))}

          {!allGranted && (
            <div className="notice warn">
              <AlertCircle size={15} />
              <span>All permissions are required to proceed with the exam. Click "Allow" for each item above.</span>
            </div>
          )}

          <button className="btn btn-blue big-btn" disabled={!allGranted} onClick={() => navigate('/student/system-check')}>
            Continue to System Check
          </button>
        </div>
      </div>
    </div>
  );
}
