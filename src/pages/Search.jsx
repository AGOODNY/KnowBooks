import { useEffect, useState, useMemo } from 'react'
import { useSearchParams } from 'react-router-dom'
import BookCard from '../components/BookCard'
import usePagination from '../hooks/usePagination'
import { mockBooks, mockTags } from '../data/mockData'
import './Search.css'

const SORT_OPTIONS = [
  { value: 'latest', label: 'Latest' },
  { value: 'rating', label: 'Highest rated' },
  { value: 'popular', label: 'Most popular' },
]

const RATING_FILTERS = [
  { value: '', label: 'Any rating' },
  { value: '4', label: '4+ stars' },
  { value: '3', label: '3+ stars' },
]

function Search() {
  const [searchParams, setSearchParams] = useSearchParams()
  const keyword = searchParams.get('keyword') || ''
  const tagFilter = searchParams.get('tag') || ''

  const [selectedTags, setSelectedTags] = useState(() =>
    tagFilter ? tagFilter.split(',').filter(Boolean) : []
  )
  const [authorFilter, setAuthorFilter] = useState('')
  const [ratingFilter, setRatingFilter] = useState('')
  const [sortBy, setSortBy] = useState('latest')

  // Build filtered list
  const filteredBooks = useMemo(() => {
    let result = [...mockBooks]

    if (keyword) {
      const lower = keyword.toLowerCase()
      result = result.filter(book =>
        book.title.toLowerCase().includes(lower)
        || book.author.toLowerCase().includes(lower)
        || book.tags.some(tag => tag.name.toLowerCase().includes(lower))
      )
    }

    if (selectedTags.length > 0) {
      result = result.filter(book =>
        selectedTags.some(t => book.tags.some(bt => bt.name === t))
      )
    }

    if (authorFilter) {
      const lower = authorFilter.toLowerCase()
      result = result.filter(book => book.author.toLowerCase().includes(lower))
    }

    if (ratingFilter) {
      const minRating = parseFloat(ratingFilter)
      result = result.filter(book => parseFloat(book.rating) >= minRating)
    }

    // Sort
    switch (sortBy) {
      case 'rating':
        result.sort((a, b) => parseFloat(b.rating) - parseFloat(a.rating))
        break
      case 'popular':
        result.sort((a, b) => b.likes - a.likes)
        break
      case 'latest':
      default:
        result.sort((a, b) => new Date(b.dateAdded) - new Date(a.dateAdded))
        break
    }

    return result
  }, [keyword, selectedTags, authorFilter, ratingFilter, sortBy])

  // Pagination fetch function
  const fetchFn = (pageNum, pageSize) => {
    const start = (pageNum - 1) * pageSize
    const items = filteredBooks.slice(start, start + pageSize)
    return { items, total: filteredBooks.length }
  }

  const { data, page, totalPages, loading, loadPage, goToPage, reset } = usePagination({ fetchFn })

  useEffect(() => {
    reset()
    loadPage(1)
  }, [keyword, selectedTags, authorFilter, ratingFilter, sortBy])

  const handleTagToggle = (tagName) => {
    setSelectedTags(prev => {
      const next = prev.includes(tagName)
        ? prev.filter(t => t !== tagName)
        : [...prev, tagName]

      // Sync tag filter to URL
      const params = new URLSearchParams(searchParams)
      if (next.length > 0) {
        params.set('tag', next.join(','))
      } else {
        params.delete('tag')
      }
      if (keyword) params.set('keyword', keyword)
      setSearchParams(params)
      return next
    })
  }

  const handleResetFilters = () => {
    setSelectedTags([])
    setAuthorFilter('')
    setRatingFilter('')
    setSortBy('latest')
    setSearchParams({})
  }

  return (
    <div className="search-page">
      <div className="search-layout container">
        {/* Sidebar Filters */}
        <aside className="search-sidebar">
          <h3 className="filter-heading">Filters</h3>

          <div className="filter-group">
            <label className="filter-label">Tags</label>
            <div className="filter-tags">
              {mockTags.map(tag => (
                <button
                  key={tag.id}
                  className={`filter-tag ${selectedTags.includes(tag.name) ? 'filter-tag--active' : ''}`}
                  onClick={() => handleTagToggle(tag.name)}
                >
                  {tag.name}
                </button>
              ))}
            </div>
          </div>

          <div className="filter-group">
            <label className="filter-label" htmlFor="filter-author">Author</label>
            <input
              id="filter-author"
              type="text"
              className="filter-input"
              placeholder="Filter by author..."
              value={authorFilter}
              onChange={(e) => setAuthorFilter(e.target.value)}
            />
          </div>

          <div className="filter-group">
            <label className="filter-label" htmlFor="filter-rating">Rating</label>
            <select
              id="filter-rating"
              className="filter-select"
              value={ratingFilter}
              onChange={(e) => setRatingFilter(e.target.value)}
            >
              {RATING_FILTERS.map(opt => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label className="filter-label" htmlFor="filter-sort">Sort by</label>
            <select
              id="filter-sort"
              className="filter-select"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              {SORT_OPTIONS.map(opt => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>

          <button className="filter-reset" onClick={handleResetFilters}>
            Reset filters
          </button>
        </aside>

        {/* Results */}
        <section className="search-results">
          <div className="search-summary">
            {keyword && (
              <p className="search-keyword">Results for &ldquo;{keyword}&rdquo;</p>
            )}
            <p className="search-count">{filteredBooks.length} books found</p>
          </div>

          {loading ? (
            <div className="search-loading">Loading...</div>
          ) : data.length === 0 ? (
            <div className="search-empty">
              <p>No books match your criteria.</p>
              <p className="search-empty-hint">Try adjusting your filters or search term.</p>
            </div>
          ) : (
            <>
              <div className="search-grid">
                {data.map(book => (
                  <BookCard key={book.id} book={book} />
                ))}
              </div>

              {/* Pagination */}
              {totalPages > 1 && (
                <div className="pagination">
                  <button
                    className="pagination-btn"
                    disabled={page <= 1}
                    onClick={() => goToPage(page - 1)}
                  >
                    ← Previous
                  </button>
                  <span className="pagination-info">
                    Page {page} of {totalPages}
                  </span>
                  <button
                    className="pagination-btn"
                    disabled={page >= totalPages}
                    onClick={() => goToPage(page + 1)}
                  >
                    Next →
                  </button>
                </div>
              )}
            </>
          )}
        </section>
      </div>
    </div>
  )
}

export default Search
