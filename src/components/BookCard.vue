<template>
  <router-link v-if="size === 'compact'" :to="`/book/${book.id}`" class="book-card book-card--compact">
    <div class="book-card-cover book-card-cover--compact">
      <img 
        v-if="book.cover" 
        :src="getCoverUrl(book.cover)" 
        :alt="book.title"
        class="cover-image cover-image--compact"
      />
      <svg v-else width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" class="cover-icon">
        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
        <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
      </svg>
    </div>
    <div class="book-card-info book-card-info--compact">
      <h3 class="book-card-title">{{ book.title }}</h3>
      <p class="book-card-author">{{ book.author }}</p>
      <div class="book-card-meta">
        <span class="book-card-rating book-card-rating--compact" :title="`${book.average_rating || book.rating}/5`">
          <span class="rating-star">&#9733;</span> {{ (book.average_rating || book.rating || 0).toFixed(1) }}
        </span>
      </div>
    </div>
  </router-link>

  <router-link v-else :to="`/book/${book.id}`" :class="['book-card', `book-card--${size}`]">
    <div class="book-card-cover">
      <img 
        v-if="book.cover" 
        :src="getCoverUrl(book.cover)" 
        :alt="book.title"
        class="cover-image"
      />
      <span v-else class="cover-placeholder">No Cover</span>
    </div>
    <div class="book-card-info">
      <h3 class="book-card-title">{{ book.title }}</h3>
      <p class="book-card-author">{{ book.author }}</p>
      <div class="book-card-meta">
        <span class="book-card-rating" :title="`${book.average_rating || book.rating}/5`">
          {{ starDisplay }}
        </span>
        <span class="book-card-likes">
          {{ book.likes_count || book.likes || 0 }} likes
        </span>
      </div>
      <div v-if="book.tags && book.tags.length > 0" class="book-card-tags">
        <span v-for="tag in book.tags" :key="tag.id" class="book-card-tag">{{ tag.name }}</span>
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  book: {
    type: Object,
    required: true
  },
  size: { 
    type: String, 
    default: 'default',
    validator: (value) => ['default', 'small', 'compact'].includes(value)
  },
})

// 获取封面图片 URL
const getCoverUrl = (cover) => {
  if (!cover) return ''
  // 如果已经是完整的 URL，直接返回
  if (cover.startsWith('http://') || cover.startsWith('https://')) {
    return cover
  }
  // 如果是相对路径，添加 media 前缀
  if (cover.startsWith('/media/')) {
    return `http://127.0.0.1:8000${cover}`
  }
  // 其他情况，假设是媒体文件路径
  return `http://127.0.0.1:8000/media/${cover}`
}

const starDisplay = computed(() => {
  const rating = props.book.average_rating || props.book.rating || 0
  const fullStars = Math.round(rating)
  return '★'.repeat(fullStars) + '☆'.repeat(5 - fullStars)
})
</script>

<style scoped>
.book-card {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--color-light-gray);
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: #fff;
  transition: border-color 0.2s, box-shadow 0.2s;
  text-decoration: none;
}

.book-card:hover {
  border-color: var(--color-accent-orange);
  box-shadow: 0 2px 12px rgba(217, 112, 74, 0.08);
}

.book-card-cover {
  width: 100%;
  aspect-ratio: 3 / 4;
  background: #f5f2ec;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-image--compact {
  width: 52px;
  height: auto;
  object-fit: cover;
}

.cover-placeholder {
  font-family: var(--font-heading);
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--color-mid-gray);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.book-card-info {
  padding: 0.9rem 0.95rem;
}

.book-card-title {
  font-family: var(--font-heading);
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--color-dark);
  margin-bottom: 0.15rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.book-card-author {
  font-size: 0.8rem;
  color: var(--color-mid-gray);
  margin-bottom: 0.5rem;
}

.book-card-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.75rem;
  margin-bottom: 0.5rem;
}

.book-card-rating {
  color: var(--color-accent-orange);
  letter-spacing: 1px;
}

.book-card-likes {
  color: var(--color-mid-gray);
}

.book-card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
}

.book-card-tag {
  font-family: var(--font-heading);
  font-size: 0.7rem;
  font-weight: 500;
  color: var(--color-accent-orange);
  background: rgba(217, 112, 74, 0.06);
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
}

/* Size variant: small (horizontal scroll items) */
.book-card--small {
  min-width: 180px;
  max-width: 180px;
}

.book-card--small .book-card-info {
  padding: 0.55rem 0.65rem;
}

.book-card--small .book-card-title {
  font-size: 0.85rem;
  font-weight: 500;
}

/* Size variant: compact (horizontal layout for vertical lists) */
.book-card--compact {
  flex-direction: row;
  border-radius: var(--radius);
  border-color: var(--color-light-gray);
}

.book-card--compact:hover {
  border-color: var(--color-light-gray);
  box-shadow: none;
  background: var(--color-bg-secondary);
}

.book-card-cover--compact {
  width: 52px;
  min-width: 52px;
  aspect-ratio: auto;
  height: auto;
  background: #f5f2ec;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.cover-icon {
  color: var(--color-mid-gray);
  opacity: 0.5;
}

.book-card-info--compact {
  padding: 0.55rem 0.7rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;
}

.book-card--compact .book-card-title {
  font-size: 0.88rem;
  font-weight: 500;
  margin-bottom: 0.1rem;
}

.book-card--compact .book-card-author {
  font-size: 0.76rem;
  margin-bottom: 0.2rem;
}

.book-card--compact .book-card-meta {
  margin-bottom: 0;
}

.book-card-rating--compact {
  font-size: 0.75rem;
  color: var(--color-dark);
}

.rating-star {
  color: var(--color-accent-orange);
}
</style>