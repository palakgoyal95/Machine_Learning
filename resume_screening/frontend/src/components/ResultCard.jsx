const strengths = ['Technical signal', 'Role alignment', 'Screening priority']
const evidence = [
  { label: 'Classifier', value: 'Multiclass role model' },
  { label: 'Ranking', value: 'Probability weighted' },
  { label: 'Decision', value: 'Recruiter reviewed' },
]

function clampScore(score) {
  return Math.max(0, Math.min(100, Number(score) || 0))
}

function ResultCard({ error, fileName, focusRole, result, status }) {
  const score = clampScore(result.confidence)
  const matches = result.top_matches || []
  const recommendation = score >= 85 ? 'Advance' : score >= 65 ? 'Review' : 'Hold'

  return (
    <section className="result-panel" aria-label="Screening result">
      <div className="result-header">
        <div>
          <p className="eyebrow">Output</p>
          <h2>Screening intelligence</h2>
        </div>
        <span className={`analysis-pill ${status}`}>
          {status === 'loading' ? 'Running model' : status === 'error' ? 'Needs attention' : 'Analyzed'}
        </span>
      </div>

      {error ? <div className="error-banner">{error}</div> : null}

      <div className="decision-bar">
        <div>
          <span>Recommended action</span>
          <strong>{recommendation}</strong>
        </div>
        <div>
          <span>Confidence band</span>
          <strong>{score >= 80 ? 'High' : score >= 60 ? 'Medium' : 'Low'}</strong>
        </div>
        <div>
          <span>Review owner</span>
          <strong>Talent team</strong>
        </div>
      </div>

      <div className="score-layout">
        <div className="score-ring" style={{ '--score': `${score * 3.6}deg` }}>
          <div>
            <strong>{Math.round(score)}%</strong>
            <span>match</span>
          </div>
        </div>
        <div className="role-summary">
          <span className="file-name">{fileName}</span>
          <h3>{result.predicted_role}</h3>
          <p>
            Focus role: <strong>{focusRole}</strong>
          </p>
        </div>
      </div>

      <div className="match-list">
        {matches.map((match) => {
          const confidence = clampScore(match.confidence)
          return (
            <article className="match-row" key={match.role}>
              <div>
                <strong>{match.role}</strong>
                <span>{Math.round(confidence)}% confidence</span>
              </div>
              <div className="meter" aria-hidden="true">
                <span style={{ width: `${confidence}%` }}></span>
              </div>
            </article>
          )
        })}
      </div>

      <div className="evidence-grid">
        {evidence.map((item) => (
          <div key={item.label}>
            <span>{item.label}</span>
            <strong>{item.value}</strong>
          </div>
        ))}
      </div>

      <div className="signal-grid">
        <div>
          <h4>Strong signals</h4>
          <div className="chip-group">
            {strengths.map((item) => (
              <span className="chip positive" key={item}>
                {item}
              </span>
            ))}
          </div>
        </div>
        <div>
          <h4>Review next</h4>
          <p className="section-note">The pie chart below shows what to prioritize first.</p>
        </div>
      </div>
    </section>
  )
}

export default ResultCard
