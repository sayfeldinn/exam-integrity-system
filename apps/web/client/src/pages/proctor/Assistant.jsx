import { useEffect, useRef, useState } from 'react';
import { Brain, Send } from 'lucide-react';

const suggestions = [
  'Which student has the most violations?',
  'Show students who used a phone',
  'Which students are currently high risk?',
  "Summarize today's exam session",
];

const greeting = "Hello Dr. Mona! I'm your AI exam integrity assistant. I can help you analyze student behavior, identify risk patterns, and generate summaries. What would you like to know about the current exam session?";

export default function Assistant() {
  const [messages, setMessages] = useState([{ from: 'bot', text: greeting }]);
  const [draft, setDraft] = useState('');
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ block: 'end' });
  }, [messages]);

  // canned reply - there is no real model behind this demo
  function ask(question) {
    const text = question.trim();
    if (!text) return;
    const reply = `I analyzed the current exam session data. Here's what I found regarding "${text}": Based on real-time monitoring data from 240 active students, I can provide a detailed breakdown. Would you like me to generate a full report or filter by specific risk criteria?`;
    setMessages((m) => [...m, { from: 'me', text }, { from: 'bot', text: reply }]);
    setDraft('');
  }

  return (
    <div className="assistant-page">
      <div className="chat-scroll">
        {messages.map((m, i) => (
          <div className={`chat-line ${m.from === 'me' ? 'mine' : ''}`} key={i}>
            {m.from === 'bot' && <span className="bot-icon"><Brain size={17} /></span>}
            <div className="bubble">{m.text}</div>
          </div>
        ))}

        {messages.length === 1 && (
          <>
            <div className="suggest-title">SUGGESTED QUESTIONS</div>
            <div className="suggest-row">
              {suggestions.map((s) => (
                <button key={s} className="suggest" onClick={() => ask(s)}>{s}</button>
              ))}
            </div>
          </>
        )}
        <div ref={bottomRef} />
      </div>

      <form className="chat-bar" onSubmit={(e) => { e.preventDefault(); ask(draft); }}>
        <input
          aria-label="Message"
          placeholder="Ask about students, violations, risk patterns..."
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
        />
        <button className="btn btn-blue" disabled={!draft.trim()}>
          <Send size={16} /> Send
        </button>
      </form>
    </div>
  );
}
