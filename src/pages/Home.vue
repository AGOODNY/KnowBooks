<template>
  <div class="home container">
    <!-- 全局加载 -->
    <div v-if="isPageLoading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading your personalized recommendations...</p>
    </div>

    <template v-else>
      <!-- Header — greeting + stats -->
      <header class="home-header">
        <div class="header-greeting">
          <div class="header-icon-wrap">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
              <line x1="8" y1="7" x2="16" y2="7" />
              <line x1="8" y1="11" x2="14" y2="11" />
            </svg>
          </div>
          <div>
            <p class="header-eyebrow">WELCOME BACK</p>
            <h1 class="header-title">What will you read today?</h1>
          </div>
        </div>

        <!-- 统计数据 - 骨架屏 -->
        <div v-if="isStatsLoading" class="header-stats">
          <div class="stat-card skeleton-stat">
            <div class="skeleton" style="width: 40px; height: 40px; border-radius: 10px;"></div>
            <div>
              <div class="skeleton" style="width: 50px; height: 22px; margin-bottom: 5px;"></div>
              <div class="skeleton" style="width: 60px; height: 12px;"></div>
            </div>
          </div>
          <div class="stat-card skeleton-stat">
            <div class="skeleton" style="width: 40px; height: 40px; border-radius: 10px;"></div>
            <div>
              <div class="skeleton" style="width: 50px; height: 22px; margin-bottom: 5px;"></div>
              <div class="skeleton" style="width: 60px; height: 12px;"></div>
            </div>
          </div>
          <div class="stat-card skeleton-stat">
            <div class="skeleton" style="width: 40px; height: 40px; border-radius: 10px;"></div>
            <div>
              <div class="skeleton" style="width: 50px; height: 22px; margin-bottom: 5px;"></div>
              <div class="skeleton" style="width: 60px; height: 12px;"></div>
            </div>
          </div>
        </div>
        <div v-else class="header-stats">
          <div class="stat-card">
            <div class="stat-icon" style="background: #fdf0e9; color: #d9704a">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
              </svg>
            </div>
            <div>
              <span class="stat-value">{{ stats.booksRead }}</span>
              <span class="stat-label">Books read</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon" style="background: #fbf5e8; color: #d4a84b">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
              </svg>
            </div>
            <div>
              <span class="stat-value">{{ stats.favorites }}</span>
              <span class="stat-label">Favorites</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon" style="background: #eff2e9; color: #788c5d">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
              </svg>
            </div>
            <div>
              <span class="stat-value">{{ stats.comments }}</span>
              <span class="stat-label">Comments</span>
            </div>
          </div>
        </div>
      </header>

      <!-- Recommendations — title + tabs + horizontal scroll -->
      <section class="home-recommend">
        <div class="recommend-header">
          <div>
            <h2 class="recommend-title">Recommended for You</h2>
            <p class="recommend-subtitle">Based on your reading history</p>
          </div>
          <div class="recommend-tabs">
            <button
              v-for="tab in tabs"
              :key="tab.key"
              :class="['tab', { 'tab--active': activeTab === tab.key }]"
              @click="activeTab = tab.key"
            >
              {{ tab.label }}
            </button>
          </div>
        </div>

        <!-- 推荐书籍 - 骨架屏 -->
        <div v-if="isBooksLoading" class="recommend-scroll">
          <div v-for="i in 6" :key="i" class="skeleton skeleton-book-card"></div>
        </div>
        <div v-else class="recommend-scroll">
          <BookCard v-for="book in currentBooks" :key="book.id" :book="book" size="small" />
        </div>

        <div class="recommend-more">
          <router-link to="/recommend" class="more-link">View more recommendations &rarr;</router-link>
        </div>
      </section>

      <!-- Popular & Latest dual column -->
      <section class="home-dual">
        <div class="dual-column">
          <!-- Popular Books -->
          <div>
            <div class="dual-col-header">
              <div class="dual-col-title">
                <span class="dual-col-icon" style="color: #d9704a">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
                  </svg>
                </span>
                <h3>Popular Books</h3>
              </div>
              <router-link to="/search?sort=popular" class="dual-col-link">See all</router-link>
            </div>
            <div class="dual-col-list">
              <div v-if="isBooksLoading" class="skeleton skeleton-compact-card" v-for="i in 3" :key="i"></div>
              <BookCard v-else v-for="book in popularBooks" :key="book.id" :book="book" size="compact" />
            </div>
          </div>

          <!-- Latest Arrivals -->
          <div>
            <div class="dual-col-header">
              <div class="dual-col-title">
                <span class="dual-col-icon" style="color: #6a9bcc">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="12" cy="12" r="10" />
                    <polyline points="12 6 12 12 16 14" />
                  </svg>
                </span>
                <h3>Latest Arrivals</h3>
              </div>
              <router-link to="/search?sort=latest" class="dual-col-link">See all</router-link>
            </div>
            <div class="dual-col-list">
              <div v-if="isBooksLoading" class="skeleton skeleton-compact-card" v-for="i in 3" :key="i"></div>
              <BookCard v-else v-for="book in latestBooks" :key="book.id" :book="book" size="compact" />
            </div>
          </div>
        </div>
      </section>

      <!-- Popular Tags -->
      <section class="home-tags">
        <div class="tags-header">
          <div class="tags-title-group">
            <h3 class="tags-title">Popular Tags</h3>
            <span class="tags-badge">{{ tags.length }}</span>
          </div>
          <router-link to="/search" class="tags-link">Browse all &rarr;</router-link>
        </div>
        <p class="tags-desc">Click a tag to explore books in that category</p>
        
        <!-- 标签云 - 骨架屏 -->
        <div v-if="isTagsLoading" class="tags-skeleton">
          <div v-for="i in 12" :key="i" class="skeleton skeleton-tag"></div>
        </div>
        <TagCloud v-else :tags="tags" />
      </section>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import BookCard from '../components/BookCard.vue'
import TagCloud from '../components/TagCloud.vue'

// 加载状态
const isPageLoading = ref(true)
const isStatsLoading = ref(true)
const isBooksLoading = ref(true)
const isTagsLoading = ref(true)

const tabs = [
  { key: 'foryou', label: 'For You' },
  { key: 'popular', label: 'Popular' },
  { key: 'latest', label: 'Latest' },
]

const activeTab = ref('foryou')

// Data
const stats = ref({
  booksRead: 0,
  favorites: 0,
  comments: 0
})

const tags = ref([])

const recommendBooks = ref([])

const popularBooks = ref([])

const latestBooks = ref([])

// Get user stats
const loadStats = async () => {
  isStatsLoading.value = true
  const token = localStorage.getItem('access_token')
  if (!token) {
    isStatsLoading.value = false
    return
  }

  try {
    // Get stats info
    const statsRes = await axios.get(
      'http://127.0.0.1:8000/api/users/stats/',
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    // Get comments list to count
    const commentsRes = await axios.get(
      'http://127.0.0.1:8000/api/users/comments/',
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    stats.value = {
      booksRead: statsRes.data.books_read || 0,
      favorites: statsRes.data.favorites || 0,
      comments: commentsRes.data.length || 0
    }
  } catch (err) {
    console.error('Failed to load stats:', err)
    stats.value = {
      booksRead: 0,
      favorites: 0,
      comments: 0
    }
  } finally {
    isStatsLoading.value = false
  }
}

// Get recommendations
const loadRecommendBooks = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) return

  try {
    const res = await axios.get(
      'http://127.0.0.1:8000/api/recommendations/home/?type=recommend',
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    recommendBooks.value = res.data
  } catch (err) {
    console.error('Failed to load recommendations:', err)
  }
}

// Get popular books
const loadPopularBooks = async () => {
  try {
    const res = await axios.get(
      'http://127.0.0.1:8000/api/recommendations/home/?type=hot'
    )

    popularBooks.value = res.data
  } catch (err) {
    console.error('Failed to load popular books:', err)
  }
}

// Get latest books
const loadLatestBooks = async () => {
  try {
    const res = await axios.get(
      'http://127.0.0.1:8000/api/recommendations/home/?type=latest'
    )

    latestBooks.value = res.data
  } catch (err) {
    console.error('Failed to load latest books:', err)
  }
}

// Get tag cloud
const loadTags = async () => {
  isTagsLoading.value = true
  try {
    const res = await axios.get(
      'http://127.0.0.1:8000/api/recommendations/tags/cloud/'
    )

    tags.value = res.data
  } catch (err) {
    console.error('Failed to load tags:', err)
  } finally {
    isTagsLoading.value = false
  }
}

// Initialize page
onMounted(async () => {
  isPageLoading.value = true
  isBooksLoading.value = true
  
  await Promise.all([
    loadStats(),
    loadRecommendBooks(),
    loadPopularBooks(),
    loadLatestBooks(),
    loadTags()
  ])
  
  isBooksLoading.value = false
  isPageLoading.value = false
})

// Modify currentBooks
const currentBooks = computed(() => {
  if (activeTab.value === 'foryou') {
    return recommendBooks.value
  }

  if (activeTab.value === 'popular') {
    return popularBooks.value
  }

  return latestBooks.value
})
</script>

<style scoped>
/* ===== Header ===== */
.home-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  padding: 3rem 0 2rem;
  flex-wrap: wrap;
}

.header-greeting {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-icon-wrap {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  background: var(--color-bg-secondary);
  color: var(--color-accent-orange);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.header-eyebrow {
  font-family: var(--font-heading);
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  color: var(--color-mid-gray);
  margin-bottom: 0.2rem;
}

.header-title {
  font-family: var(--font-heading);
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--color-dark);
  letter-spacing: -0.02em;
}

/* ===== Stats ===== */
.header-stats {
  display: flex;
  gap: 0.75rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: #fff;
  border: 1px solid var(--color-light-gray);
  border-radius: var(--radius-lg);
  padding: 0.75rem 1.1rem;
  min-width: 136px;
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-value {
  display: block;
  font-family: var(--font-heading);
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--color-dark);
  line-height: 1;
}

.stat-label {
  display: block;
  font-family: var(--font-body);
  font-size: 0.72rem;
  color: var(--color-mid-gray);
  margin-top: 0.15rem;
}

/* ===== Recommendations ===== */
.home-recommend {
  padding: 2rem 0;
}

.recommend-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  gap: 1rem;
  flex-wrap: wrap;
}

.recommend-title {
  font-family: var(--font-heading);
  font-size: 1.35rem;
  font-weight: 700;
  color: var(--color-dark);
  margin-bottom: 0.2rem;
}

.recommend-subtitle {
  font-family: var(--font-body);
  font-size: 0.85rem;
  color: var(--color-mid-gray);
}

/* Tabs */
.recommend-tabs {
  display: flex;
  gap: 0.35rem;
  background: var(--color-light-gray);
  border-radius: 20px;
  padding: 3px;
}

.tab {
  font-family: var(--font-heading);
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--color-mid-gray);
  background: transparent;
  padding: 0.4rem 1rem;
  border-radius: 18px;
  transition: all 0.15s;
}

.tab:hover {
  color: var(--color-dark);
}

.tab--active {
  background: #fff;
  color: var(--color-dark);
  font-weight: 600;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

/* Horizontal scroll */
.recommend-scroll {
  display: flex;
  gap: 1.25rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
  scroll-snap-type: x mandatory;
}

.recommend-scroll::-webkit-scrollbar {
  height: 5px;
}

.recommend-scroll::-webkit-scrollbar-track {
  background: transparent;
}

.recommend-scroll::-webkit-scrollbar-thumb {
  background: var(--color-light-gray);
  border-radius: 5px;
}

.recommend-scroll > * {
  scroll-snap-align: start;
  flex-shrink: 0;
  width: 195px;
}

.recommend-more {
  margin-top: 1.25rem;
  display: flex;
  justify-content: flex-end;
}

.more-link {
  font-family: var(--font-heading);
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--color-accent-orange);
  transition: opacity 0.15s;
}

.more-link:hover {
  opacity: 0.8;
}

/* ===== Popular & Latest Dual Column ===== */
.home-dual {
  padding: 1rem 0 2rem;
}

.dual-column {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.dual-col-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.85rem;
}

.dual-col-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-dark);
}

.dual-col-icon {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.dual-col-link {
  font-family: var(--font-heading);
  font-size: 0.76rem;
  font-weight: 500;
  color: var(--color-mid-gray);
  transition: color 0.15s;
}

.dual-col-link:hover {
  color: var(--color-dark);
}

.dual-col-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* ===== Tags ===== */
.home-tags {
  padding: 1.5rem 0 3rem;
  border-top: 1px solid var(--color-light-gray);
}

.tags-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.4rem;
}

.tags-title-group {
  display: flex;
  align-items: center;
  gap: 0.55rem;
}

.tags-title {
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-dark);
}

.tags-badge {
  font-family: var(--font-heading);
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--color-mid-gray);
  background: var(--color-light-gray);
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tags-link {
  font-family: var(--font-heading);
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--color-mid-gray);
  transition: color 0.15s;
}

.tags-link:hover {
  color: var(--color-dark);
}

.tags-desc {
  font-family: var(--font-body);
  font-size: 0.82rem;
  color: var(--color-mid-gray);
  margin-bottom: 1rem;
}

/* ===== Loading & Skeleton Styles ===== */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: 4rem 2rem;
  text-align: center;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 3px solid var(--color-light-gray);
  border-top-color: var(--color-accent-orange);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 8px;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.skeleton-stat {
  background: #fff;
}

.skeleton-book-card {
  width: 180px;
  height: 240px;
  border-radius: 12px;
}

.skeleton-compact-card {
  width: 100%;
  height: 80px;
  border-radius: 8px;
}

.skeleton-tag {
  display: inline-block;
  width: 80px;
  height: 32px;
  margin: 4px;
  border-radius: 20px;
}

.tags-skeleton {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

/* ===== Responsive ===== */
@media (max-width: 768px) {
  .home-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.25rem;
  }

  .header-title {
    font-size: 1.3rem;
  }

  .header-stats {
    width: 100%;
  }

  .stat-card {
    flex: 1;
    min-width: 0;
  }

  .recommend-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .dual-column {
    grid-template-columns: 1fr;
  }
}
</style>