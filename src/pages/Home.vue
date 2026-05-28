<template>
  <div class="home container">
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

      <div class="header-stats">
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

      <div class="recommend-scroll">
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
            <BookCard v-for="book in popularBooks" :key="book.id" :book="book" size="compact" />
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
            <BookCard v-for="book in latestBooks" :key="book.id" :book="book" size="compact" />
          </div>
        </div>
      </div>
    </section>

    <!-- Popular Tags -->
    <section class="home-tags">
      <div class="tags-header">
        <div class="tags-title-group">
          <h3 class="tags-title">Popular Tags</h3>
          <span class="tags-badge">{{ mockTags.length }}</span>
        </div>
        <router-link to="/search" class="tags-link">Browse all &rarr;</router-link>
      </div>
      <p class="tags-desc">Click a tag to explore books in that category</p>
      <TagCloud :tags="mockTags" />
    </section>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import BookCard from '../components/BookCard.vue'
import TagCloud from '../components/TagCloud.vue'
import {
  mockUserStats,
  mockTags,
  getRecommendedBooks,
  getPopularBooks,
  getLatestBooks,
} from '../data/mockData'

const TAB_BOOKS = {
  foryou: () => getRecommendedBooks(8),
  popular: () => getPopularBooks(8),
  latest: () => getLatestBooks(8),
}

const tabs = [
  { key: 'foryou', label: 'For You' },
  { key: 'popular', label: 'Popular' },
  { key: 'latest', label: 'Latest' },
]

const activeTab = ref('foryou')
const stats = mockUserStats
const currentBooks = computed(() => TAB_BOOKS[activeTab.value]())
const popularBooks = getPopularBooks(3)
const latestBooks = getLatestBooks(3)
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
