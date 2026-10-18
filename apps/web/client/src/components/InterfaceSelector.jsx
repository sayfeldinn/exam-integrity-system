import { Link } from 'react-router-dom';

// Floating button that takes you back to the "Choose your interface" section.
export default function InterfaceSelector() {
  return (
    <Link to="/#interfaces" className="selector-btn">
      ← Interface Selector
    </Link>
  );
}
