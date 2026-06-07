// Mock data generation following project naming conventions
// book_exampleX, author_exampleX, text_exampleX, tag_exampleX

const categories = [
  'Fiction', 'Science', 'History', 'Philosophy', 'Technology',
  'Art', 'Biography', 'Mystery', 'Adventure', 'Poetry'
]

const generateTags = () => {
  const tags = []
  for (let i = 1; i <= 10; i++) {
    tags.push({
      id: i,
      name: `tag_example${i}`,
      category: categories[i - 1],
    })
  }
  return tags
}

  const generateBooks = (count = 20) => {
  const books = []
  const tagPool = generateTags()

  for (let i = 1; i <= count; i++) {
    const bookTags = []
    const tagCount = 1 + Math.floor(Math.random() * 3)
    const usedIndices = new Set()
    while (bookTags.length < tagCount) {
      const idx = Math.floor(Math.random() * tagPool.length)
      if (!usedIndices.has(idx)) {
        usedIndices.add(idx)
        bookTags.push(tagPool[idx])
      }
    }

    const daysAgo = Math.floor(Math.random() * 180)
    const date = new Date()
    date.setDate(date.getDate() - daysAgo)

    books.push({
      id: i,
      title: `book_example${i}`,
      author: `author_example${i}`,
      description: `text_example${i}`,
      cover: null,
      tags: bookTags,
      likes: Math.floor(Math.random() * 200),
      favorites: Math.floor(Math.random() * 80),
      rating: (1 + Math.random() * 4).toFixed(1),
      ratingCount: Math.floor(Math.random() * 100),
      dateAdded: date.toISOString().split('T')[0],
      status:
        i % 3 === 0
          ? 'pending'
          : i % 3 === 1
          ? 'approved'
          : 'rejected',
    })
  }
  return books
} 



const generateUserStats = () => ({
  booksRead: 12,
  favorites: 8,
  comments: 23,
})

const featureHighlights = [
  {
    iconKey: 'recommend',
    title: 'Smart Recommendations',
    description: 'Discover books tailored to your reading preferences through our intelligent recommendation engine.',
    bgColor: '#fdf0e9',
    iconColor: '#d9704a',
  },
  {
    iconKey: 'review',
    title: 'Genuine Reviews',
    description: 'Read honest ratings and thoughtful comments from real readers before committing to your next book.',
    bgColor: '#e9f0f8',
    iconColor: '#6a9bcc',
  },
  {
    iconKey: 'collection',
    title: 'Collection Management',
    description: 'Build your personal reading list, track what you have read, and revisit books at any time.',
    bgColor: '#eff2e9',
    iconColor: '#788c5d',
  },
  {
    iconKey: 'community',
    title: 'Reader Community',
    description: 'Like, comment, and exchange reading insights with fellow book enthusiasts who share your taste.',
    bgColor: '#fbf5e8',
    iconColor: '#d4a84b',
  },
]

export const mockBooks = generateBooks(20)
export const mockTags = generateTags()
export const mockUserStats = generateUserStats()
export const mockFeatureHighlights = featureHighlights

export function getBooksByTag(tagName) {
  return mockBooks.filter(book =>
    book.tags.some(tag => tag.name === tagName)
  )
}

export function getBooksByKeyword(keyword) {
  const lower = keyword.toLowerCase()
  return mockBooks.filter(book =>
    book.title.toLowerCase().includes(lower)
    || book.author.toLowerCase().includes(lower)
    || book.tags.some(tag => tag.name.toLowerCase().includes(lower))
  )
}

export function getRecommendedBooks(limit = 5) {
  // Simulate collaborative filtering: return highest-rated + most-liked
  return [...mockBooks]
    .sort((a, b) => (b.likes + b.favorites) - (a.likes + a.favorites))
    .slice(0, limit)
}

export function getPopularBooks(limit = 3) {
  return [...mockBooks]
    .sort((a, b) => b.likes - a.likes)
    .slice(0, limit)
}

export function getLatestBooks(limit = 3) {
  return [...mockBooks]
    .sort((a, b) => new Date(b.dateAdded) - new Date(a.dateAdded))
    .slice(0, limit)
}

export function getRelatedBooks(bookId, limit = 5) {
  const book = mockBooks.find(b => b.id === bookId)
  if (!book) return []
  return mockBooks
    .filter(b => b.id !== bookId && b.tags.some(tag => book.tags.some(t => t.id === tag.id)))
    .slice(0, limit)
}
