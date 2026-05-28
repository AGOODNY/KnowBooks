<template>
  <div class="search-page">
    <div class="search-layout container">
      <!-- Sidebar Filters -->
      <aside class="search-sidebar">
        <h3 class="filter-heading">Filters</h3>

        <div class="filter-group">
          <label class="filter-label">Tags</label>
          <div class="filter-tags">
            <button
              v-for="tag in mockTags"
              :key="tag.id"
              :class="['filter-tag', { 'filter-tag--active': selectedTags.includes(tag.name) }]"
              @click="handleTagToggle(tag.name)"
            >
              {{ tag.name }}
            </button>
          </div>
        </div>

        <div class="filter-group">
          <label class="filter-label" for="filter-author">Author</label>
          <input
            id="filter-author"
            type="text"
            class="filter-input"
            placeholder="Filter by author..."
            v-model="authorFilter"
          />
        </div>

        <div class="filter-group">
          <label class="filter-label" for="filter-rating">Rating</label>
          <select
            id="filter-rating"
            class="filter-select"
            v-model="ratingFilter"
          >
            <option v-for="opt in RATING_FILTERS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
          </select>
        </div>

        <div class="filter-group">
          <label class="filter-label" for="filter-sort">Sort by</label>
          <select
            id="filter-sort"
            class="filter-select"
            v-model="sortBy"
          >
            <option v-for="opt in SORT_OPTIONS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
          </select>
        </div>

        <button class="filter-reset" @click="handleResetFilters">
          Reset filters
        </button>
      </aside>

      <!-- Results -->
      <section class="search-results">
        <div class="search-summary">
          <p v-if="keyword" class="search-keyword">Results for &ldquo;{{ keyword }}&rdquo;</p>
          <p class="search-count">{{ filteredBooks.length }} books found</p>
        </div>

        <div v-if="loading" class="search-loading">Loading...</div>
        <div v-else-if="data.length === 0" class="search-empty">
          <p>No books match your criteria.</p>
          <p class="search-empty-hint">Try adjusting your filters or search term.</p>
        </div>
        <template v-else>
          <div class="search-grid">
            <BookCard v-for="book in data" :key="book.id" :book="book" />
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="pagination">
            <button
              class="pagination-btn"
              :disabled="page <= 1"
              @click="goToPage(page - 1)"
            >
              &larr; Previous
            </button>
            <span class="pagination-info">
              Page {{ page }} of {{ totalPages }}
            </span>
            <button
              class="pagination-btn"
              :disabled="page >= totalPages"
              @click="goToPage(page + 1)"
            >
              Next &rarr;
            </button>
          </div>
        </template>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BookCard from '../components/BookCard.vue'
import { usePagination } from '../composables/usePagination'
import { mockBooks, mockTags } from '../data/mockData'

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

const route = useRoute()
const router = useRouter()

const keyword = computed(() => route.query.keyword || '')
const tagFilter = computed(() => route.query.tag || '')

const selectedTags = ref(tagFilter.value ? tagFilter.value.split(',').filter(Boolean) : [])
const authorFilter = ref('')
const ratingFilter = ref('')
const sortBy = ref('latest')

const filteredBooks = computed(() => {
  let result = [...mockBooks]

  if (keyword.value) {
    const lower = keyword.value.toLowerCase()
    result = result.filter(book =>
      book.title.toLowerCase().includes(lower)
      || book.author.toLowerCase().includes(lower)
      || book.tags.some(tag => tag.name.toLowerCase().includes(lower))
    )
  }

  if (selectedTags.value.length > 0) {
    result = result.filter(book =>
      selectedTags.value.some(t => book.tags.some(bt => bt.name === t))
    )
  }

  if (authorFilter.value) {
    const lower = authorFilter.value.toLowerCase()
    result = result.filter(book => book.author.toLowerCase().includes(lower))
  }

  if (ratingFilter.value) {
    const minRating = parseFloat(ratingFilter.value)
    result = result.filter(book => parseFloat(book.rating) >= minRating)
  }

  // Sort
  switch (sortBy.value) {
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
})

const fetchFn = (pageNum, pageSize) => {
  const start = (pageNum - 1) * pageSize
  const items = filteredBooks.value.slice(start, start + pageSize)
  return { items, total: filteredBooks.value.length }
}

const { data, page, totalPages, loading, loadPage, goToPage, reset } = usePagination({ fetchFn })

// Re-run pagination whenever filters change
watch(
  [keyword, selectedTags, authorFilter, ratingFilter, sortBy],
  () => { reset(); loadPage(1) },
  { immediate: true }
)

function handleTagToggle(tagName) {
  const prev = selectedTags.value
  const next = prev.includes(tagName)
    ? prev.filter(t => t !== tagName)
    : [...prev, tagName]

  selectedTags.value = next

  // Sync tag filter to URL
  const query = { ...route.query }
  if (next.length > 0) {
    query.tag = next.join(',')
  } else {
    delete query.tag
  }
  if (keyword.value) query.keyword = keyword.value
  router.replace({ query })
}

function handleResetFilters() {
  selectedTags.value = []
  authorFilter.value = ''
  ratingFilter.value = ''
  sortBy.value = 'latest'
  router.replace({ query: {} })
}
</script>

<style scoped>
.search-page {
  min-height: calc(100vh - 64px);
  padding: 2rem 0;
}

.search-layout {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
}

/* ===== Sidebar ===== */
.search-sidebar {
  flex: 0 0 240px;
  border: 1px solid var(--color-light-gray);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  background: #fff;
  position: sticky;
  top: 84px;
}

.filter-heading {
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.filter-group {
  margin-bottom: 1.25rem;
}

.filter-label {
  display: block;
  font-family: var(--font-heading);
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--color-mid-gray);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 0.5rem;
}

.filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
}

.filter-tag {
  font-family: var(--font-heading);
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--color-mid-gray);
  background: var(--color-light);
  border: 1px solid var(--color-light-gray);
  padding: 0.2rem 0.55rem;
  border-radius: 16px;
  transition: all 0.15s;
}

.filter-tag:hover {
  color: var(--color-dark);
  border-color: var(--color-mid-gray);
}

.filter-tag--active {
  background: var(--color-accent-orange);
  border-color: var(--color-accent-orange);
  color: #fff;
}

.filter-input,
.filter-select {
  width: 100%;
  padding: 0.45rem 0.65rem;
  border: 1px solid var(--color-light-gray);
  border-radius: var(--radius);
  background: #fff;
  color: var(--color-dark);
  font-size: 0.85rem;
}

.filter-input:focus,
.filter-select:focus {
  outline: none;
  border-color: var(--color-mid-gray);
}

.filter-input::placeholder {
  color: var(--color-mid-gray);
}

.filter-reset {
  width: 100%;
  padding: 0.5rem;
  font-family: var(--font-heading);
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--color-accent-orange);
  background: none;
  border: 1px solid var(--color-light-gray);
  border-radius: var(--radius);
  transition: background 0.15s, border-color 0.15s;
}

.filter-reset:hover {
  background: rgba(217, 112, 74, 0.05);
  border-color: var(--color-accent-orange);
}

/* ===== Results ===== */
.search-results {
  flex: 1;
  min-width: 0;
}

.search-summary {
  margin-bottom: 1.25rem;
}

.search-keyword {
  font-family: var(--font-heading);
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.2rem;
}

.search-count {
  font-size: 0.85rem;
  color: var(--color-mid-gray);
}

.search-loading {
  text-align: center;
  padding: 3rem 0;
  color: var(--color-mid-gray);
  font-size: 0.9rem;
}

.search-empty {
  text-align: center;
  padding: 3rem 0;
  color: var(--color-mid-gray);
}

.search-empty-hint {
  font-size: 0.85rem;
  margin-top: 0.5rem;
}

.search-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

/* ===== Pagination ===== */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 2rem 0 1rem;
}

.pagination-btn {
  padding: 0.4rem 1rem;
  font-family: var(--font-heading);
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--color-dark);
  background: var(--color-light);
  border: 1px solid var(--color-light-gray);
  border-radius: var(--radius);
  transition: background 0.15s, border-color 0.15s;
}

.pagination-btn:hover:not(:disabled) {
  background: var(--color-light-gray);
  border-color: var(--color-mid-gray);
}

.pagination-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.pagination-info {
  font-size: 0.85rem;
  color: var(--color-mid-gray);
}

/* Responsive */
@media (max-width: 768px) {
  .search-layout {
    flex-direction: column;
  }

  .search-sidebar {
    flex: none;
    width: 100%;
    position: static;
  }
}
</style>
