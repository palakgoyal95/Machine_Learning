import { useEffect, useMemo, useState } from 'react'
import axios from 'axios'
import './App.css'
import heroImg from './assets/hero.png'
import UploadResume from './components/UploadResume'
import ResultCard from './components/ResultCard'

const API_URL = import.meta.env.VITE_API_URL || '/api/upload/'

const starterResult = {
  predicted_role: 'AI Resume Screener',
  confidence: 92,
  top_matches: [
    { role: 'Machine Learning Engineer', confidence: 92 },
    { role: 'Data Scientist', confidence: 84 },
    { role: 'Backend Developer', confidence: 71 },
  ],
}

const focusRoles = [
  'Machine Learning Engineer',
  'Data Scientist',
  'Frontend Developer',
  'Backend Developer',
]

const auditTrail = [
  { label: 'Document intake', state: 'Encrypted PDF received' },
  { label: 'Text extraction', state: 'Pages parsed and normalized' },
  { label: 'Model ranking', state: 'Role probabilities calculated' },
  { label: 'Recruiter review', state: 'Human decision stays in control' },
]

const hiringSignals = [
  { label: 'Signal quality', value: 'A-', tone: 'green' },
  { label: 'Review time', value: '38s', tone: 'amber' },
  { label: 'Bias check', value: 'Manual', tone: 'rose' },
]

const skillRoadmap = [
  {
    title: 'Portfolio depth',
    detail: 'Add 2 to 3 case studies with metrics, scope, and tooling details.',
    level: 'High priority',
    score: 42,
  },
  {
    title: 'Leadership keywords',
    detail: 'Show ownership, mentoring, roadmap decisions, and project outcomes.',
    level: 'Medium priority',
    score: 34,
  },
  {
    title: 'Domain evidence',
    detail: 'Highlight industry context, customer impact, and business alignment.',
    level: 'Medium priority',
    score: 24,
  },
]

const roleLabelMap = new Map([
  ['AI/ML Specialists', 'AI / ML Specialist'],
  ['Backend Developers', 'Backend Developer'],
  ['Blockchain Developers', 'Blockchain Developer'],
  ['Cloud Architects', 'Cloud Architect'],
  ['Data Analysts', 'Data Analyst'],
  ['Database Administrators', 'Database Administrator'],
  ['DevOps Engineers', 'DevOps Engineer'],
  ['Frontend Developers', 'Frontend Developer'],
  ['Full Stack Developers', 'Full Stack Developer'],
  ['Game Developers', 'Game Developer'],
  ['Python Developers', 'Python Developer'],
  ['QA Engineers', 'QA Engineer'],
])

function humanizeRoleLabel(label) {
  const trimmedLabel = String(label || '').replace(/\s+Resumes?$/i, '').trim()

  if (roleLabelMap.has(trimmedLabel)) {
    return roleLabelMap.get(trimmedLabel)
  }

  return trimmedLabel || 'Best fit role'
}

function normalizePrediction(payload) {
  const prediction = payload?.prediction || payload || {}
  const topMatches = prediction.top_matches || prediction.topMatches || []

  return {
    predicted_role: humanizeRoleLabel(
      prediction.predicted_role || prediction.predictedRole || topMatches[0]?.role || 'Best fit role',
    ),
    confidence: Number(prediction.confidence || topMatches[0]?.confidence || 0),
    top_matches: topMatches.length
      ? topMatches.map((match) => ({
          role: humanizeRoleLabel(match.role || match.predicted_role || 'Role match'),
          confidence: Number(match.confidence || 0),
        }))
      : [
          {
            role: humanizeRoleLabel(prediction.predicted_role || 'Best fit role'),
            confidence: Number(prediction.confidence || 0),
          },
        ],
  }
}

function App() {
  const [result, setResult] = useState(starterResult)
  const [fileName, setFileName] = useState('sample-resume.pdf')
  const [status, setStatus] = useState('idle')
  const [error, setError] = useState('')
  const [focusRole, setFocusRole] = useState(focusRoles[0])
  const [theme, setTheme] = useState(() => {
    if (typeof window === 'undefined') return 'light'

    return window.localStorage.getItem('resume-radar-theme') || 'light'
  })

  useEffect(() => {
    document.documentElement.dataset.theme = theme
    window.localStorage.setItem('resume-radar-theme', theme)
  }, [theme])

  const pipelineStats = useMemo(
    () => [
      { label: 'Parsing', value: status === 'loading' ? 'Live' : 'Ready' },
      { label: 'Top match', value: `${Math.round(result.confidence)}%` },
      { label: 'Roles ranked', value: result.top_matches.length },
    ],
    [result, status],
  )

  const insightStats = useMemo(
    () => [
      { label: 'Top match', value: humanizeRoleLabel(result.predicted_role) },
      { label: 'Confidence', value: `${Math.round(result.confidence)}%` },
      { label: 'Ranked roles', value: result.top_matches.length },
    ],
    [result],
  )

  const skillTotal = skillRoadmap.reduce((total, item) => total + item.score, 0)
  const skillSegments = skillRoadmap.map((item, index) => ({
    ...item,
    color: ['var(--accent)', 'var(--accent-2)', 'var(--accent-3)'][index],
  }))

  async function handleUpload(file) {
    setStatus('loading')
    setError('')
    setFileName(file.name)

    const formData = new FormData()
    formData.append('resume', file)

    try {
      const response = await axios.post(API_URL, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setResult(normalizePrediction(response.data))
      setStatus('success')
    } catch (uploadError) {
      const isNetworkError = uploadError.message === 'Network Error' || !uploadError.response
      const message =
        uploadError.response?.data?.error ||
        (isNetworkError
          ? 'Network error: start Django on http://127.0.0.1:8000, then refresh this page and upload again.'
          : uploadError.message) ||
        'The resume could not be analyzed. Check that the Django API is running.'
      setError(message)
      setStatus('error')
    }
  }

  return (
    <main className="app-shell">
      <section className="hero-section">
        <nav className="topbar" aria-label="Primary">
          <a className="brand" href="#top" aria-label="Resume Radar home">
            <span className="brand-mark">RR</span>
            <span>Resume Radar</span>
          </a>
          <div className="nav-actions" aria-label="Screening stages and theme controls">
            <span>Upload</span>
            <span>Analyze</span>
            <span>Shortlist</span>
            <button className="theme-toggle" type="button" onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
              {theme === 'light' ? 'Dark mode' : 'Light mode'}
            </button>
          </div>
        </nav>

        <div className="hero-grid">
          <div className="hero-copy">
            <p className="eyebrow">AI resume screening workspace</p>
            <h1>Screen resumes with a clean, systematic hiring workflow.</h1>
            <p className="hero-text">
              Upload a resume PDF, score it against role families, and turn the model
              output into a recruiter-ready decision panel.
            </p>

            <div className="hero-metrics" aria-label="Product highlights">
              {insightStats.map((item) => (
                <article key={item.label} className="hero-metric">
                  <span>{item.label}</span>
                  <strong>{item.value}</strong>
                </article>
              ))}
            </div>

            <div className="role-picker" aria-label="Hiring focus">
              {focusRoles.map((role) => (
                <button
                  className={focusRole === role ? 'active' : ''}
                  key={role}
                  type="button"
                  onClick={() => setFocusRole(role)}
                >
                  {role}
                </button>
              ))}
            </div>

            <div className="stat-strip" aria-label="Pipeline overview">
              {pipelineStats.map((stat) => (
                <div className="stat-item" key={stat.label}>
                  <strong>{stat.value}</strong>
                  <span>{stat.label}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="hero-visual" aria-hidden="true">
            <div className="hero-frame"></div>
            <img src={heroImg} alt="" />
            <div className="scan-card scan-card-top">
              <span>Skill density</span>
              <strong>High</strong>
            </div>
            <div className="scan-card scan-card-bottom">
              <span>Model confidence</span>
              <strong>{Math.round(result.confidence)}%</strong>
            </div>
          </div>
        </div>
      </section>

      <section className="ops-band" aria-label="Screening operations">
        <div className="ops-card live-queue">
          <span className="section-kicker">Live desk</span>
          <strong>Candidate intelligence queue</strong>
          <p>Structured intake, model output, and recruiter next steps in one workflow.</p>
        </div>
        {hiringSignals.map((signal) => (
          <div className={`ops-card tone-${signal.tone}`} key={signal.label}>
            <span>{signal.label}</span>
            <strong>{signal.value}</strong>
          </div>
        ))}
      </section>

      <section className="workspace" aria-label="Resume analysis workspace">
        <UploadResume onUpload={handleUpload} status={status} />
        <ResultCard
          error={error}
          fileName={fileName}
          focusRole={focusRole}
          result={result}
          status={status}
        />
      </section>

      <section className="audit-section" aria-label="Analysis audit trail">
        <div>
          <p className="eyebrow">Governance</p>
          <h2>Transparent enough for real hiring reviews.</h2>
        </div>
        <div className="audit-grid">
          {auditTrail.map((item, index) => (
            <article className="audit-step" key={item.label}>
              <span>{String(index + 1).padStart(2, '0')}</span>
              <strong>{item.label}</strong>
              <p>{item.state}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="skill-section" aria-label="Skill improvement roadmap">
        <div className="section-header">
          <div>
            <p className="eyebrow">Skill improvement</p>
            <h2>What to strengthen for the next screening cycle.</h2>
          </div>
          <p className="section-note">
            The roadmap below keeps feedback practical: each item is written as a next action,
            not a vague label.
          </p>
        </div>

        <div className="skill-layout">
          <article className="skill-pie-card">
            <div
              className="skill-pie"
              style={{
                '--pie': skillSegments.reduce((accumulator, item, index) => {
                  const previous = skillSegments
                    .slice(0, index)
                    .reduce((total, previousItem) => total + previousItem.score, 0)
                  return `${accumulator}${previous} ${previous + item.score}% ${item.color}, `
                }, ''),
              }}
            >
              <div className="skill-pie-center">
                <strong>{skillTotal}%</strong>
                <span>improvement focus</span>
              </div>
            </div>
            <div className="skill-pie-caption">
              <h3>Improvement mix</h3>
              <p>Each slice shows where the next resume iteration should spend attention.</p>
            </div>
          </article>

          <div className="skill-list-compact">
            {skillSegments.map((item, index) => (
              <article className="skill-compact-row" key={item.title}>
                <div className="skill-compact-head">
                  <span className="skill-step">0{index + 1}</span>
                  <strong>{item.title}</strong>
                </div>
                <p>{item.detail}</p>
                <div className="skill-compact-meta">
                  <span>{item.level}</span>
                  <span>{item.score}%</span>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>
    </main>
  )
}

export default App
