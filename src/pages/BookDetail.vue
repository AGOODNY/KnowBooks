<template>
  <div class="book-detail-page">
    <!-- 全局加载 -->
    <div v-if="isPageLoading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading book details...</p>
    </div>

    <div v-else class="container">
      <!-- Book Hero -->
      <section class="book-hero">
        <!-- 书籍详情骨架屏 -->
        <div v-if="isBookLoading" class="book-hero-skeleton">
          <div class="skeleton skeleton-cover"></div>
          <div class="book-info-skeleton">
            <div class="skeleton skeleton-title" style="width: 60%;"></div>
            <div class="skeleton skeleton-text" style="width: 40%;"></div>
            <div class="skeleton skeleton-text" style="width: 30%;"></div>
            <div class="skeleton skeleton-text" style="width: 100%;"></div>
            <div class="skeleton skeleton-text" style="width: 90%;"></div>
            <div class="skeleton skeleton-button" style="width: 120px;"></div>
          </div>
        </div>
        <template v-else>
          <div class="book-cover">
            <img
              :src="getCoverUrl(book.cover)"
              :alt="book.title"
            >
          </div>
          <div class="book-info">
            <span class="book-category">
              {{ book.category }}
            </span>
            <h1 class="book-title">
              {{ book?.title }}
            </h1>
            <h3 class="book-author">
              {{ book.author }}
            </h3>
            <div class="book-rating">
              ⭐ {{ averageRating }}
              <span>
                ({{ bookReviews.length }} reviews)
              </span>
            </div>
            <p class="book-description">
              {{ book.description }}
            </p>
            <div class="book-actions">
              <LikeButton :book="book" />
              <FavoriteButton :book="book" />
            </div>
          </div>
        </template>
      </section>

      <!-- Reviews -->
      <section class="review-section">
        <h2 class="section-title">
          Reviews
        </h2>

        <!-- 评论骨架屏 -->
        <div v-if="isCommentsLoading" class="reviews-skeleton">
          <div class="skeleton skeleton-rating-summary"></div>
          <div v-for="i in 3" :key="i" class="skeleton skeleton-review-card"></div>
          <div class="skeleton skeleton-review-form"></div>
        </div>
        <template v-else>
          <!-- Rating Summary -->
          <div class="rating-summary">
            <div class="average-score">
              {{ averageRating }}
            </div>
            <div>
              <div class="summary-stars">
                ⭐ {{ averageRating }}/5
              </div>
              <p>
                Based on {{ bookReviews.length }} reviews
              </p>
            </div>
          </div>

          <!-- Review List -->
          <div class="review-list">
            <div
              v-for="review in bookReviews"
              :key="review.id"
              class="review-card"
            >
              <div class="review-header">
                <strong>
                  {{ review.username }}
                </strong>
                <div class="review-rating">
                  <span
                    v-for="star in 5"
                    :key="star"
                  >
                    {{ star <= (review.rating || 0) ? '★' : '☆' }}
                  </span>
                </div>
              </div>
              <p class="review-content">
                {{ review.content }}
              </p>
              <span class="review-date">
                {{ formatDate(review.created_at) }}
              </span>
            </div>
          </div>

          <!-- Review Form -->
          <div class="review-form">
            <h3>Write a Review</h3>
            <div class="rating-selector">
              <span
                v-for="star in 5"
                :key="star"
                class="star"
                @click="selectedRating = star"
              >
                {{ star <= selectedRating ? '★' : '☆' }}
              </span>
            </div>
            <textarea
              v-model="newReview"
              placeholder="Share your thoughts about this book..."
            />
            <button
              class="btn-submit"
              @click="submitReview"
            >
              Submit Review
            </button>
          </div>
        </template>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import LikeButton from '../components/LikeButton.vue'
import FavoriteButton from '../components/FavoriteButton.vue'
import { useAuth } from '../composables/useAuth.js'
import { useRoute } from 'vue-router'

const route = useRoute()
const { currentUser } = useAuth()
const bookId = Number(route.params.id)

// 加载状态
const isPageLoading = ref(true)
const isBookLoading = ref(true)
const isCommentsLoading = ref(true)

const book = ref({})
const liked = ref(false)
const favourite = ref(false)
const selectedRating = ref(0)
const newReview = ref('')
const bookReviews = ref([])

const averageRating = computed(() => {
  return book.value.average_rating || 0
})

// 获取封面图片 URL
const getCoverUrl = (cover) => {
  if (!cover) return ''
  if (cover.startsWith('http://') || cover.startsWith('https://')) {
    return cover
  }
  if (cover.startsWith('/media/')) {
    return `http://127.0.0.1:8000${cover}`
  }
  return `http://127.0.0.1:8000/media/${cover}`
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

function toggleLike() {
  liked.value = !liked.value
}

function toggleFavourite() {
  favourite.value = !favourite.value
}

// 获取书籍详情
const loadBook = async () => {
  isBookLoading.value = true
  try {
    const res = await axios.get(
      `http://127.0.0.1:8000/api/recommendations/books/${bookId}/`
    )
    book.value = res.data
  } catch (err) {
    console.error('Failed to load book:', err)
    if (err.response?.status === 404) {
      alert('Book not found')
    }
  } finally {
    isBookLoading.value = false
  }
}

// 获取评论
const loadComments = async () => {
  isCommentsLoading.value = true
  try {
    const res = await axios.get(
      `http://127.0.0.1:8000/api/interactions/comments/${bookId}/`
    )
    bookReviews.value = res.data
  } catch (err) {
    console.error('Failed to load comments:', err)
    bookReviews.value = []
  } finally {
    isCommentsLoading.value = false
  }
}

// 提交评论
const submitReview = async () => {
  if (!currentUser.value) {
    alert('Please log in first')
    return
  }
  if (!newReview.value.trim()) {
    alert('Please enter a review')
    return
  }
  
  try {
    const token = localStorage.getItem('access_token')
    const commentData = {
      content: newReview.value
    }
    
    console.log('Submitting review:', commentData)
    
    const commentResponse = await axios.post(
      `http://127.0.0.1:8000/api/interactions/comment/${bookId}/`,
      commentData,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    )
    
    console.log('Review submitted successfully:', commentResponse.data)
    
    // If there's a rating, submit it separately
    if (selectedRating.value > 0) {
      try {
        await axios.post(
          `http://127.0.0.1:8000/api/interactions/rate/${bookId}/`,
          {
            score: selectedRating.value
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          }
        )
        console.log('Rating submitted successfully')
      } catch (rateErr) {
        console.error('Rating submission failed:', rateErr)
        // Rating failure doesn't affect the comment, continue execution
      }
    }
    
    newReview.value = ''
    selectedRating.value = 0
    
    // Reload comments and book information
    await loadComments()
    await loadBook()
    
    alert('Review submitted successfully!')
    
  } catch (err) {
    console.error('Failed to submit review:', err)
    console.error('Error response:', err.response?.data)
    
    const errorMsg = err.response?.data?.content?.[0] || 
                    err.response?.data?.detail || 
                    err.response?.data?.error ||
                    'Failed to submit review'
    alert(errorMsg)
  }
}

// 自动记录浏览历史
const addHistory = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) return
  try {
    await axios.post(
      `http://127.0.0.1:8000/api/interactions/history/add/${bookId}/`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
  } catch (err) {
    console.error('Failed to add history:', err)
  }
}

// 页面加载时获取数据
onMounted(async () => {
  isPageLoading.value = true
  
  await Promise.all([
    loadBook(),
    loadComments(),
    addHistory()
  ])
  
  isPageLoading.value = false
})
</script>

<style scoped>

.book-detail-page {
  padding: 3rem 0;
}

/* Hero */
.book-hero {
  display: flex;
  gap: 3rem;
  margin-bottom: 4rem;
}

.book-cover img {
  width: 280px;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}

.book-info {
  flex: 1;
}

.book-category {
  color: var(--color-accent-orange);
  font-weight: 600;
}

.book-title {
  font-family: var(--font-heading);
  font-size: 2.5rem;
  margin: .5rem 0;
}

.book-author {
  color: var(--color-mid-gray);
  margin-bottom: 1rem;
}

.book-rating {
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.book-rating span {
  color: var(--color-mid-gray);
  font-weight: 400;
}

.book-description {
  line-height: 1.8;
  max-width: 700px;
}

.book-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-like,
.btn-save,
.btn-submit {
  border: none;
  cursor: pointer;
  border-radius: 12px;
  padding: .85rem 1.4rem;
  font-weight: 600;
}

.btn-like,
.btn-submit {
  background: var(--color-accent-orange);
  color: white;
}

.btn-save {
  background: var(--color-bg-secondary);
}

/* Reviews */
.review-section {
  margin-top: 3rem;
}

.section-title {
  font-family: var(--font-heading);
  margin-bottom: 2rem;
}

.rating-summary {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  background: var(--color-bg-secondary);
  padding: 1.5rem;
  border-radius: 20px;
  margin-bottom: 2rem;
}

.average-score {
  font-size: 3rem;
  font-weight: 700;
  color: var(--color-accent-orange);
}

.review-form {
  margin-bottom: 3rem;
}

.review-form h3 {
  margin-bottom: 1rem;
}

.rating-selector {
  margin-bottom: 1rem;
}

.star {
  font-size: 2rem;
  cursor: pointer;
  color: #f5b301;
}

.review-form textarea {
  width: 100%;
  min-height: 120px;
  padding: 1rem;
  border-radius: 16px;
  border: 1px solid var(--color-light-gray);
  resize: vertical;
  margin-bottom: 1rem;
}

.review-card {
  border: 1px solid var(--color-light-gray);
  border-radius: 16px;
  padding: 1.25rem;
  margin-bottom: 1rem;
  background: white;
}

.review-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: .75rem;
}

.review-rating {
  color: #f5b301;
}

.review-content {
  line-height: 1.7;
}

.review-date {
  font-size: .8rem;
  color: var(--color-mid-gray);
}

/* Loading & Skeleton Styles */
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

.book-hero-skeleton {
  display: flex;
  gap: 3rem;
  margin-bottom: 4rem;
}

.skeleton-cover {
  width: 280px;
  height: 420px;
  border-radius: 20px;
}

.book-info-skeleton {
  flex: 1;
}

.skeleton-title {
  height: 36px;
  margin-bottom: 12px;
}

.skeleton-text {
  height: 20px;
  margin-bottom: 12px;
}

.skeleton-button {
  height: 48px;
  border-radius: 12px;
  margin-top: 20px;
}

.skeleton-rating-summary {
  height: 100px;
  border-radius: 20px;
  margin-bottom: 2rem;
}

.skeleton-review-card {
  height: 120px;
  border-radius: 16px;
  margin-bottom: 1rem;
}

.skeleton-review-form {
  height: 280px;
  border-radius: 16px;
  margin-top: 2rem;
}

/* Responsive */
@media (max-width: 768px) {
  .book-hero {
    flex-direction: column;
  }

  .book-cover img {
    width: 100%;
    max-width: 300px;
  }

  .rating-summary {
    flex-direction: column;
    align-items: flex-start;
  }

  .book-hero-skeleton {
    flex-direction: column;
    align-items: center;
  }

  .skeleton-cover {
    width: 100%;
    max-width: 280px;
  }
}
</style>