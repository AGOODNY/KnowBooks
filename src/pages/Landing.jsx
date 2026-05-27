import { useNavigate } from 'react-router-dom'
import { mockFeatureHighlights } from '../data/mockData'
import './Landing.css'

const FEATURE_ICONS = {
  recommend: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
    </svg>
  ),
  review: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
    </svg>
  ),
  collection: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z" />
    </svg>
  ),
  community: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
      <circle cx="9" cy="7" r="4" />
      <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
      <path d="M16 3.13a4 4 0 0 1 0 7.75" />
    </svg>
  ),
}

function Landing() {
  const navigate = useNavigate()

  const scrollToFeatures = () => {
    document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' })
  }

  return (
    <div className="landing">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-inner container">
          <div className="hero-text">
            <h1 className="hero-title">
              Discover your<br /><span className="highlight">next great read</span>
            </h1>
            <p className="hero-subtitle">
              From an ocean of books, find the ones truly worth your time.
            </p>
            <p className="hero-tagline">
              Smart recommendations · Authentic reviews · Collection management · Reader community
            </p>
            <div className="hero-actions">
              <button className="btn-hero-primary" onClick={() => navigate('/home')}>Start exploring</button>
              <button className="btn-hero-secondary" onClick={scrollToFeatures}>Learn more</button>
            </div>
          </div>
          <div className="hero-visual">
            <div className="hero-graphic">
              <div className="hero-book hero-book--1"></div>
              <div className="hero-book hero-book--2"></div>
              <div className="hero-book hero-book--3"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Highlights */}
      <section id="features" className="features">
        <div className="container">
          <div className="features-header">
            <h2 className="features-heading">Everything you need to read better</h2>
            <p className="features-subheading">
              Knowbooks combines intelligent technology with a thoughtful reading experience.
            </p>
          </div>
          <div className="features-grid">
            {mockFeatureHighlights.map((feature, index) => (
              <div key={index} className="feature-card">
                <div
                  className="feature-icon"
                  style={{ background: feature.bgColor, color: feature.iconColor }}
                >
                  {FEATURE_ICONS[feature.iconKey]}
                </div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-desc">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="container footer-inner">
          <span className="footer-brand">KnowBooks</span>
          <nav className="footer-links">
            <a href="#about">About</a>
            <a href="#privacy">Privacy Policy</a>
            <a href="#terms">Terms</a>
          </nav>
        </div>
      </footer>
    </div>
  )
}

export default Landing
