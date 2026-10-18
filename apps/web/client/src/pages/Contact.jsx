import { useState } from 'react';
import { Mail, MapPin, Check } from 'lucide-react';

export default function Contact() {
  const [sent, setSent] = useState(false);

  function submit(e) {
    e.preventDefault();
    setSent(true);
  }

  function sendAnother() {
    setSent(false);
  }

  return (
    <div className="container contact">
      <header className="page-intro">
        <h1>Get in touch</h1>
        <p>Questions about the project? We'd love to hear from you.</p>
      </header>

      <div className="contact-grid">
        {sent ? (
          <section className="tile contact-success" role="status" aria-live="polite">
            <div className="success-icon"><Check size={30} strokeWidth={2.5} /></div>
            <h2>Message sent!</h2>
            <p>Thanks! We'll get back to you soon.</p>
            <button className="btn btn-dark success-again" type="button" onClick={sendAnother}>
              Send another
            </button>
          </section>
        ) : (
          <form className="tile contact-form" onSubmit={submit}>
            <label className="dark-field">Full name<input name="name" autoComplete="name" required /></label>
            <label className="dark-field">Email address<input name="email" type="email" autoComplete="email" required /></label>
            <label className="dark-field">Message<textarea name="message" rows="5" required /></label>
            <button className="btn btn-teal btn-wide" type="submit">Send Message</button>
          </form>
        )}

        <div>
          <div className="tile info-card">
            <h3>Project Information</h3>
            <div className="info-line">
              <Mail size={16} />
              <div><small>PROJECT EMAIL</small>examguard.ai@cis.alexu.edu.eg</div>
            </div>
            <div className="info-line">
              <MapPin size={16} />
              <div><small>INSTITUTION</small>Faculty of Computers and Data Science<br />Alexandria University, Egypt</div>
            </div>
          </div>
          <div className="note-box">
            This is a graduation project for the academic year 2025–2026. The platform is a research prototype built to explore AI-driven academic integrity tools.
          </div>
        </div>
      </div>
    </div>
  );
}
