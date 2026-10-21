import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Camera, User, Loader2, Check, CheckCircle2 } from 'lucide-react';
import InterfaceSelector from '../../components/InterfaceSelector.jsx';
import Steps from '../../components/Steps.jsx';

export default function Verify() {
  const navigate = useNavigate();
  const [state, setState] = useState('idle'); // idle -> scanning -> verified

  // fake the face scan: takes a couple of seconds, then succeeds
  useEffect(() => {
    if (state !== 'scanning') return;
    const timer = setTimeout(() => setState('verified'), 2200);
    return () => clearTimeout(timer);
  }, [state]);

  const scanning = state === 'scanning';
  const verified = state === 'verified';

  return (
    <div className="student-page">
      <InterfaceSelector />
      <div className="student-wrap wide">
        <Steps current={2} title="Identity Verification" subtitle="We need to confirm your identity before starting the exam." />

        <div className="panel compact">
          <div className={`camera ${state === 'idle' ? '' : state}`}>
            {state === 'idle' && (
              <div className="camera-inner">
                <div className="face-circle"><User size={24} /></div>
                Camera preview will appear here
              </div>
            )}
            {state !== 'idle' && <div className="face-circle" style={{ margin: 0 }}><User size={24} /></div>}
            {scanning && <span className="camera-badge"><Loader2 size={13} className="spin" style={{ color: '#fff' }} /> Detecting face...</span>}
            {verified && <span className="camera-badge"><Check size={13} /> Face Detected &amp; Verified</span>}
          </div>

          <div className="check-chips">
            <div className={`check-chip ${verified ? 'ok' : scanning ? 'active' : ''}`}>
              {verified ? <CheckCircle2 size={14} /> : scanning ? <Loader2 size={14} className="spin" /> : <span className="chip-ring" />} Face Detection
            </div>
            <div className={`check-chip ${verified ? 'ok' : ''}`}>
              {verified ? <CheckCircle2 size={14} /> : <span className="chip-ring" />} ID Verification
            </div>
          </div>

          <div className="instructions">
            <h4>Instructions</h4>
            • Position your face in the center of the frame<br />
            • Ensure good lighting — avoid backlighting<br />
            • Remove hats, sunglasses, or face coverings<br />
            • Look directly at the camera
          </div>

          {verified && <div className="notice good"><CheckCircle2 size={15} /> Identity Confirmed</div>}

          {verified ? (
            <button className="btn btn-blue big-btn" onClick={() => navigate('/student/permissions')}>Continue</button>
          ) : (
            <button className="btn btn-blue big-btn" disabled={scanning} onClick={() => setState('scanning')}>
              {scanning ? <><Loader2 size={16} className="spin" style={{ color: '#fff' }} /> Verifying Identity...</> : <><Camera size={17} /> Start Verification</>}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
