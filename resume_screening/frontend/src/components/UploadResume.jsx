import { useRef, useState } from 'react'

function UploadIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 3l4.8 4.8-1.4 1.4-2.4-2.4V16h-2V6.8L8.6 9.2 7.2 7.8 12 3z" />
      <path d="M5 17h2v2h10v-2h2v4H5v-4z" />
    </svg>
  )
}

function UploadResume({ onUpload, status }) {
  const inputRef = useRef(null)
  const [selectedFile, setSelectedFile] = useState(null)
  const [isDragging, setIsDragging] = useState(false)
  const [priority, setPriority] = useState('Standard')

  function pickFile(file) {
    if (!file) return
    setSelectedFile(file)
    onUpload(file)
  }

  function handleDrop(event) {
    event.preventDefault()
    setIsDragging(false)
    pickFile(event.dataTransfer.files?.[0])
  }

  return (
    <section className="upload-panel" aria-label="Upload resume">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Input</p>
          <h2>Resume intake</h2>
        </div>
        <span className="secure-pill">Local API</span>
      </div>

      <button
        className={`drop-zone ${isDragging ? 'dragging' : ''}`}
        type="button"
        onClick={() => inputRef.current?.click()}
        onDragEnter={() => setIsDragging(true)}
        onDragLeave={() => setIsDragging(false)}
        onDragOver={(event) => event.preventDefault()}
        onDrop={handleDrop}
      >
        <span className="upload-icon">
          <UploadIcon />
        </span>
        <span className="drop-title">
          {selectedFile ? selectedFile.name : 'Drop a resume PDF here'}
        </span>
        <span className="drop-copy">PDF parser, model ranking, and confidence output</span>
        {selectedFile ? (
          <span className="file-meta">
            {Math.max(1, Math.round(selectedFile.size / 1024))} KB uploaded
          </span>
        ) : (
          <span className="file-meta">Supports recruiter-ready PDFs</span>
        )}
      </button>

      <input
        ref={inputRef}
        className="file-input"
        type="file"
        accept="application/pdf,.pdf"
        onChange={(event) => pickFile(event.target.files?.[0])}
      />

      <div className="upload-footer">
        <div>
          <span className={`status-dot ${status}`}></span>
          <span>
            {status === 'loading'
              ? 'Analyzing resume'
              : status === 'error'
                ? 'Upload requires attention'
                : 'Ready for upload'}
          </span>
        </div>
        <button className="text-button" type="button" onClick={() => inputRef.current?.click()}>
          Browse
        </button>
      </div>

      <div className="intake-settings" aria-label="Screening settings">
        <div>
          <label htmlFor="priority">Review lane</label>
          <select id="priority" value={priority} onChange={(event) => setPriority(event.target.value)}>
            <option>Standard</option>
            <option>Priority</option>
            <option>Executive</option>
          </select>
        </div>
        <div>
          <span>Accepted format</span>
          <strong>PDF</strong>
        </div>
      </div>

      <div className="quality-panel">
        <strong>Pre-flight checks</strong>
        <ul>
          <li>Readable text layer</li>
          <li>Role classifier ready</li>
          <li>Top three matches ranked</li>
        </ul>
      </div>
    </section>
  )
}

export default UploadResume
