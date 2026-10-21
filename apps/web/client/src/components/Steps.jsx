// "STEP 2 OF 5" header shared by the pre-exam screens.
export default function Steps({ current, title, subtitle }) {
  return (
    <>
      <div className="steps">
        {[1, 2, 3, 4, 5].map((n) => <i key={n} className={n <= current ? 'done' : ''} />)}
      </div>
      <div className="step-count">STEP {current} OF 5</div>
      <h2 className="step-title">{title}</h2>
      <p className="step-sub">{subtitle}</p>
    </>
  );
}
