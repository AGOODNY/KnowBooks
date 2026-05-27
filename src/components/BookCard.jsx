import { Link } from 'react-router-dom'
import './BookCard.css'

function BookCard({ book, size = 'default' }) {
  const starDisplay = '★'.repeat(Math.round(book.rating)) + '☆'.repeat(5 - Math.round(book.rating))

  if (size === 'compact') {
    return (
      <Link to={`/book/${book.id}`} className="book-card book-card--compact">
        <div className="book-card-cover book-card-cover--compact">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="cover-icon">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
          </svg>
        </div>
        <div className="book-card-info book-card-info--compact">
          <h3 className="book-card-title">{book.title}</h3>
          <p className="book-card-author">{book.author}</p>
          <div className="book-card-meta">
            <span className="book-card-rating book-card-rating--compact" title={`${book.rating}/5`}><span className="rating-star">★</span> {book.rating}</span>
          </div>
        </div>
      </Link>
    )
  }

  return (
    <Link to={`/book/${book.id}`} className={`book-card book-card--${size}`}>
      <div className="book-card-cover">
        <span className="cover-placeholder">Not uploaded</span>
      </div>
      <div className="book-card-info">
        <h3 className="book-card-title">{book.title}</h3>
        <p className="book-card-author">{book.author}</p>
        <div className="book-card-meta">
          <span className="book-card-rating" title={`${book.rating}/5`}>
            {starDisplay}
          </span>
          <span className="book-card-likes">
            {book.likes} likes
          </span>
        </div>
        {book.tags && book.tags.length > 0 && (
          <div className="book-card-tags">
            {book.tags.map(tag => (
              <span key={tag.id} className="book-card-tag">{tag.name}</span>
            ))}
          </div>
        )}
      </div>
    </Link>
  )
}

export default BookCard
