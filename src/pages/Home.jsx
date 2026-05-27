import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import BookCard from '../components/BookCard'
import TagCloud from '../components/TagCloud'
import {
  mockUserStats,
  mockTags,
  getRecommendedBooks,
  getPopularBooks,
  getLatestBooks,
} from '../data/mockData'
import './Home.css'

const TAB_BOOKS = {
  foryou: () => getRecommendedBooks(8),
  popular: () => getPopularBooks(8),
  latest: () => getLatestBooks(8),
}

const STAT_ICONS = {
  booksRead: {
    bg: '#fdf0e9',
    color: '#d9704a',
    svg: (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
        <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
      </svg>
    ),
  },
  favorites: {
    bg: '#fbf5e8',
    color: '#d4a84b',
    svg: (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
      </svg>
    ),
  },
  comments: {
    bg: '#eff2e9',
    color: '#788c5d',
    svg: (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
      </svg>
    ),
  },
}

function Home() {
  const [activeTab, setActiveTab] = useState('foryou')
  const stats = mockUserStats
  const currentBooks = useMemo(() => TAB_BOOKS[activeTab](), [activeTab])
  const popularBooks = useMemo(() => getPopularBooks(3), [])
  const latestBooks = useMemo(() => getLatestBooks(3), [])

  return (
    <div className="home container">
      {/* Header — greeting + stats */}
      <header className="home-header">
        <div className="header-greeting">
          <div className="header-icon-wrap">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
              <line x1="8" y1="7" x2="16" y2="7" />
              <line x1="8" y1="11" x2="14" y2="11" />
            </svg>
          </div>
          <div>
            <p className="header-eyebrow">WELCOME BACK</p>
            <h1 className="header-title">What will you read today?</h1>
          </div>
        </div>

        <div className="header-stats">
          <div className="stat-card">
            <div className="stat-icon" style={{ background: STAT_ICONS.booksRead.bg, color: STAT_ICONS.booksRead.color }}>
              {STAT_ICONS.booksRead.svg}
            </div>
            <div>
              <span className="stat-value">{stats.booksRead}</span>
              <span className="stat-label">Books read</span>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon" style={{ background: STAT_ICONS.favorites.bg, color: STAT_ICONS.favorites.color }}>
              {STAT_ICONS.favorites.svg}
            </div>
            <div>
              <span className="stat-value">{stats.favorites}</span>
              <span className="stat-label">Favorites</span>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon" style={{ background: STAT_ICONS.comments.bg, color: STAT_ICONS.comments.color }}>
              {STAT_ICONS.comments.svg}
            </div>
            <div>
              <span className="stat-value">{stats.comments}</span>
              <span className="stat-label">Comments</span>
            </div>
          </div>
        </div>
      </header>

      {/* Recommendations — title + tabs + horizontal scroll */}
      <section className="home-recommend">
        <div className="recommend-header">
          <div>
            <h2 className="recommend-title">Recommended for You</h2>
            <p className="recommend-subtitle">Based on your reading history</p>
          </div>
          <div className="recommend-tabs">
            {[
              { key: 'foryou', label: 'For You' },
              { key: 'popular', label: 'Popular' },
              { key: 'latest', label: 'Latest' },
            ].map(tab => (
              <button
                key={tab.key}
                className={`tab ${activeTab === tab.key ? 'tab--active' : ''}`}
                onClick={() => setActiveTab(tab.key)}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        <div className="recommend-scroll">
          {currentBooks.map(book => (
            <BookCard key={book.id} book={book} size="small" />
          ))}
        </div>

        <div className="recommend-more">
          <Link to="/recommend" className="more-link">View more recommendations →</Link>
        </div>
      </section>

      {/* Popular & Latest dual column */}
      <section className="home-dual">
        <div className="dual-column">
          {/* Popular Books */}
          <div>
            <div className="dual-col-header">
              <div className="dual-col-title">
                <span className="dual-col-icon" style={{ color: '#d9704a' }}>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
                  </svg>
                </span>
                <h3>Popular Books</h3>
              </div>
              <Link to="/search?sort=popular" className="dual-col-link">See all</Link>
            </div>
            <div className="dual-col-list">
              {popularBooks.map(book => (
                <BookCard key={book.id} book={book} size="compact" />
              ))}
            </div>
          </div>

          {/* Latest Arrivals */}
          <div>
            <div className="dual-col-header">
              <div className="dual-col-title">
                <span className="dual-col-icon" style={{ color: '#6a9bcc' }}>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="12" cy="12" r="10" />
                    <polyline points="12 6 12 12 16 14" />
                  </svg>
                </span>
                <h3>Latest Arrivals</h3>
              </div>
              <Link to="/search?sort=latest" className="dual-col-link">See all</Link>
            </div>
            <div className="dual-col-list">
              {latestBooks.map(book => (
                <BookCard key={book.id} book={book} size="compact" />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Popular Tags */}
      <section className="home-tags">
        <div className="tags-header">
          <div className="tags-title-group">
            <h3 className="tags-title">Popular Tags</h3>
            <span className="tags-badge">{mockTags.length}</span>
          </div>
          <Link to="/search" className="tags-link">Browse all →</Link>
        </div>
        <p className="tags-desc">Click a tag to explore books in that category</p>
        <TagCloud tags={mockTags} />
      </section>
    </div>
  )
}

export default Home
