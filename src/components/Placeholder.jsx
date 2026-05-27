import './Placeholder.css'

function Placeholder({ pageTitle, icon = '📄' }) {
  return (
    <div className="placeholder">
      <div className="placeholder-inner">
        <span className="placeholder-icon">{icon}</span>
        <h2 className="placeholder-title">{pageTitle}</h2>
        <p className="placeholder-text">Page under development...</p>
      </div>
    </div>
  )
}

export default Placeholder
