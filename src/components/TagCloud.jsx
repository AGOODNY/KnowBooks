import { Link } from 'react-router-dom'
import './TagCloud.css'

function TagCloud({ tags }) {
  if (!tags || tags.length === 0) {
    return <p className="tag-cloud-empty">No tags available.</p>
  }

  return (
    <div className="tag-cloud">
      {tags.map(tag => (
        <Link
          key={tag.id}
          to={`/search?tag=${encodeURIComponent(tag.name)}`}
          className="tag-cloud-item"
        >
          {tag.name}
        </Link>
      ))}
    </div>
  )
}

export default TagCloud
