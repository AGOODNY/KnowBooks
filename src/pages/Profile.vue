<template>
  <div class="profile-page">
    <!-- 全局加载 -->
    <div v-if="isPageLoading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading your profile...</p>
    </div>

    <div v-else class="container">
      <!-- Header -->
      <section class="profile-header">
        <div
          class="profile-avatar"
          @click="triggerAvatarUpload"
        >
          <img
            v-if="avatar"
            :src="avatar"
            alt="avatar"
            class="avatar-image"
          />
          <div v-else class="default-avatar">
            {{ userInitial }}
          </div>
        </div>
        <input
          ref="avatarInput"
          type="file"
          accept="image/*"
          style="display: none"
          @change="handleAvatarChange"
        />
        <div class="profile-info">
          <h1 class="profile-name">{{ profile.nickname || profile.username }}</h1>
          <p class="profile-email">{{ profile.email }}</p>
        </div>
      </section>

      <!-- Stats - 骨架屏 -->
      <section class="stats-section">
        <div v-if="isStatsLoading" class="stat-card skeleton-stat">
          <div class="skeleton" style="width: 50px; height: 32px; margin: 0 auto 8px;"></div>
          <div class="skeleton" style="width: 60px; height: 14px; margin: 0 auto;"></div>
        </div>
        <div v-else class="stat-card">
          <span class="stat-number">{{ stats.favorites || 0 }}</span>
          <span class="stat-label">Favorites</span>
        </div>
        <div v-if="isStatsLoading" class="stat-card skeleton-stat">
          <div class="skeleton" style="width: 50px; height: 32px; margin: 0 auto 8px;"></div>
          <div class="skeleton" style="width: 60px; height: 14px; margin: 0 auto;"></div>
        </div>
        <div v-else class="stat-card">
          <span class="stat-number">{{ stats.books_read || 0 }}</span>
          <span class="stat-label">Books Read</span>
        </div>
        <div v-if="isStatsLoading" class="stat-card skeleton-stat">
          <div class="skeleton" style="width: 50px; height: 32px; margin: 0 auto 8px;"></div>
          <div class="skeleton" style="width: 60px; height: 14px; margin: 0 auto;"></div>
        </div>
        <div v-else class="stat-card">
          <span class="stat-number">{{ stats.likes || 0 }}</span>
          <span class="stat-label">Likes</span>
        </div>
      </section>

      <!-- Favourite Books -->
      <section class="section">
        <div class="section-header">
          <h2>Favourite Books</h2>
        </div>

        <div class="book-grid">
          <!-- 骨架屏 -->
          <template v-if="isFavoritesLoading">
            <div v-for="i in 3" :key="i" class="book-card skeleton">
              <div class="skeleton" style="width: 80px; height: 110px; margin-bottom: 0.75rem;"></div>
              <div class="skeleton" style="width: 100%; height: 16px; margin-bottom: 8px;"></div>
              <div class="skeleton" style="width: 60%; height: 14px;"></div>
            </div>
          </template>
          <template v-else>
            <div
              class="book-card"
              v-for="book in favourites"
              :key="book.id"
            >
              <router-link
                :to="`/book/${book.id}`"
                class="book-link"
              >
                <div class="book-cover-small">
                  <img
                    v-if="book.cover"
                    :src="getCoverUrl(book.cover)"
                    :alt="book.title"
                  />
                  <div v-else class="book-placeholder-small">
                    No cover
                  </div>
                </div>
                <h3>{{ book.title }}</h3>
                <p>{{ book.author }}</p>
              </router-link>
            </div>
          </template>

          <div v-if="!isFavoritesLoading && favourites.length === 0" class="empty-state">
            <p>No favorite books yet.</p>
          </div>
        </div>
      </section>

      <!-- My Uploads -->
      <section class="section">
        <div class="section-header">
          <h2>My Uploads</h2>
          <button
            class="upload-link"
            @click="router.push('/upload')"
          >
            + Upload Book
          </button>
        </div>

        <div class="book-grid">
          <!-- 骨架屏 -->
          <template v-if="isUploadsLoading">
            <div v-for="i in 3" :key="i" class="book-card skeleton">
              <div class="skeleton" style="width: 120px; height: 160px; margin-bottom: 0.75rem;"></div>
              <div class="skeleton" style="width: 100%; height: 16px; margin-bottom: 8px;"></div>
              <div class="skeleton" style="width: 60%; height: 14px;"></div>
            </div>
          </template>
          <template v-else>
            <div
              class="book-card"
              v-for="book in myUploads"
              :key="book.id"
              @click="goToDetail(book)"
              :class="{ 'disabled-card': book.status !== 'approved' }"
            >
              <div class="book-cover">
                <img
                  v-if="book.cover"
                  :src="getCoverUrl(book.cover)"
                  alt="book cover"
                />
                <div v-else class="book-placeholder">
                  No cover
                </div>
              </div>
              <h3>{{ book.title }}</h3>
              <p>{{ book.author }}</p>
              <span class="upload-tag" :class="statusClass(book.status)">
                {{ book.status === 'approved' ? 'Uploaded' : (book.status === 'pending' ? 'Pending' : 'Rejected') }}
              </span>
            </div>
          </template>
        </div>
      </section>

      <!-- Reviews -->
      <section class="section">
        <div class="section-header">
          <h2>My Reviews</h2>
        </div>

        <!-- 骨架屏 -->
        <div v-if="isReviewsLoading">
          <div v-for="i in 2" :key="i" class="review-card skeleton">
            <div class="skeleton" style="width: 60%; height: 20px; margin-bottom: 12px;"></div>
            <div class="skeleton" style="width: 100%; height: 60px; margin-bottom: 8px;"></div>
            <div class="skeleton" style="width: 30%; height: 14px;"></div>
          </div>
        </div>
        <template v-else>
          <div
            v-for="review in comments"
            :key="review.id"
            class="review-card-wrapper"
          >
            <router-link
              :to="`/book/${review.book_id}`"
              class="book-link"
            >
              <div class="review-card"> 
                <div class="review-top">
                  <h3>{{ review.book_title }}</h3>
                  <div class="review-rating">
                    <span v-for="star in 5" :key="star">
                      {{ star <= (review.rating || 0) ? '★' : '☆' }}
                    </span>
                  </div>
                </div>
                <p>{{ review.content }}</p>
                <div class="review-footer">
                  <span class="review-date">{{ formatDate(review.created_at) }}</span>
                </div>
              </div>
            </router-link>
          </div>
        </template>

        <div v-if="!isReviewsLoading && comments.length === 0" class="empty-state">
          <p>No reviews yet.</p>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

import { useAuth } from '../composables/useAuth'

const { currentUser } = useAuth()
const router = useRouter()

// 加载状态
const isPageLoading = ref(true)
const isStatsLoading = ref(true)
const isFavoritesLoading = ref(true)
const isUploadsLoading = ref(true)
const isReviewsLoading = ref(true)

const avatarInput = ref(null)

const avatar = ref(
  localStorage.getItem('avatar')
)

// 计算用户首字母（用于默认头像）
const userInitial = computed(() => {
  const name = profile.value.nickname || profile.value.username || currentUser.value?.username || 'U'
  return name.charAt(0).toUpperCase()
})

// 数据
const profile = ref({})
const favourites = ref([])
const comments = ref([])
const stats = ref({})

// 上传相关
const myUploads = ref([])

const loadMyUploads = async () => {
  isUploadsLoading.value = true
  const token = localStorage.getItem('access_token')
  if (!token) {
    isUploadsLoading.value = false
    return
  }

  try {
    const res = await axios.get(
      'http://127.0.0.1:8000/api/recommendations/books/my_uploads/',
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    myUploads.value = res.data
  } catch (err) {
    console.error('Failed to load my uploads:', err)
    myUploads.value = []
  } finally {
    isUploadsLoading.value = false
  }
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

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

function triggerAvatarUpload() {
  avatarInput.value.click()
}

const isUploading = ref(false)

async function handleAvatarChange(event) {
  const file = event.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    alert('Please upload an image file')
    return
  }

  if (file.size > 10 * 1024 * 1024) {
    alert('Image size should be less than 10MB')
    return
  }

  isUploading.value = true

  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      alert('Please log in first')
      return
    }

    const formData = new FormData()
    formData.append('avatar', file)

    const response = await axios.put(
      'http://127.0.0.1:8000/api/users/update/',
      formData,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      }
    )

    const imageUrl = URL.createObjectURL(file)
    avatar.value = imageUrl

    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      const user = JSON.parse(storedUser)
      user.avatar = response.data.avatar || imageUrl
      localStorage.setItem('user', JSON.stringify(user))
    }

    await loadProfile()
    alert('Avatar updated successfully!')

    setTimeout(() => {
      window.location.reload()
    }, 500)

  } catch (err) {
    console.error('Avatar upload failed:', err)
    const errorMsg = err.response?.data?.error || err.response?.data?.detail || 'Upload failed'
    alert(`Failed to upload avatar: ${errorMsg}`)
  } finally {
    isUploading.value = false
  }
}

function statusClass(status) {
  switch (status) {
    case 'approved':
      return 'status-uploaded'
    case 'pending':
      return 'status-pending'
    case 'rejected':
      return 'status-rejected'
    default:
      return ''
  }
}

function goToDetail(book) {
  if (book.status === 'approved') {
    router.push(`/book/${book.id}`)
  } else {
    alert('You can only access the detail page after it is approved.')
  }
}

// 获取用户资料
const loadProfile = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) return

  try {
    const res = await axios.get(
      'http://127.0.0.1:8000/api/users/me/',
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    profile.value = res.data

    if (profile.value.avatar) {
      if (profile.value.avatar.startsWith('http')) {
        avatar.value = profile.value.avatar
      } else if (profile.value.avatar.startsWith('/media/')) {
        avatar.value = `http://127.0.0.1:8000${profile.value.avatar}`
      } else {
        avatar.value = `http://127.0.0.1:8000/media/${profile.value.avatar}`
      }
    }
  } catch (err) {
    console.error(err)
  }
}

// 获取收藏（后端现在返回完整的书籍信息）
const loadFavorites = async () => {
  isFavoritesLoading.value = true
  const token = localStorage.getItem('access_token')
  if (!token) {
    isFavoritesLoading.value = false
    return
  }

  try {
    const res = await axios.get(
      'http://127.0.0.1:8000/api/users/favorites/',
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    favourites.value = res.data
  } catch (err) {
    console.error(err)
    favourites.value = []
  } finally {
    isFavoritesLoading.value = false
  }
}

// 获取评论
const loadComments = async () => {
  isReviewsLoading.value = true
  const token = localStorage.getItem('access_token')
  if (!token) {
    isReviewsLoading.value = false
    return
  }

  try {
    const res = await axios.get(
      'http://127.0.0.1:8000/api/users/comments/',
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    comments.value = res.data
  } catch (err) {
    console.error(err)
  } finally {
    isReviewsLoading.value = false
  }
}

// 获取统计
const loadStats = async () => {
  isStatsLoading.value = true
  const token = localStorage.getItem('access_token')
  if (!token) {
    isStatsLoading.value = false
    return
  }

  try {
    const res = await axios.get(
      'http://127.0.0.1:8000/api/users/stats/',
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    stats.value = res.data
  } catch (err) {
    console.error(err)
  } finally {
    isStatsLoading.value = false
  }
}

// 页面初始化
onMounted(async () => {
  isPageLoading.value = true
  
  await Promise.all([
    loadProfile(),
    loadFavorites(),
    loadComments(),
    loadStats(),
    loadMyUploads()
  ])
  
  isPageLoading.value = false
})
</script>

<style scoped>
.profile-page {
  padding: 4rem 0;
  background: var(--color-light);
}

/* Header */
.default-avatar {
  width: 100%;
  height: 100%;
  background: var(--color-accent-orange, #8C8982);
  color: white;
  font-family: var(--font-heading, system-ui);
  font-size: 1.5rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.profile-avatar {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  overflow: hidden;
  cursor: pointer;
  background: var(--color-bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  transition: 0.2s;
}

.profile-avatar:hover {
  transform: scale(1.05);
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-name {
  font-family: var(--font-heading);
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-dark);
}

.profile-email {
  color: var(--color-mid-gray);
}

/* Stats */
.stats-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 4rem;
}

.stat-card {
  background: white;
  border: 1px solid var(--color-light-gray);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  text-align: center;
}

.stat-number {
  display: block;
  font-family: var(--font-heading);
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-accent-orange);
}

.stat-label {
  color: var(--color-mid-gray);
  font-size: 0.9rem;
}

/* Sections */
.section {
  margin-bottom: 4rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  font-family: var(--font-heading);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-dark);
}

/* Books */
.book-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.book-card {
  border: 1px solid var(--color-light-gray);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  background: white;
  transition: all 0.2s ease;
}

.book-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
}

.book-card h3 {
  font-family: var(--font-heading);
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.book-card p {
  color: var(--color-mid-gray);
  margin: 0;
}

.book-cover-small {
  width: 80px;
  height: 110px;
  margin-bottom: 0.75rem;
  overflow: hidden;
  border-radius: 8px;
  border: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f9f9f9;
}

.book-cover-small img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.book-placeholder-small {
  font-size: 0.7rem;
  color: #999;
  text-align: center;
}

/* Upload */
.book-cover {
  width: 120px;
  height: 160px;
  margin-bottom: 0.75rem;
  overflow: hidden;
  border-radius: 8px;
  border: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f9f9f9;
}

.book-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.book-placeholder {
  font-size: 0.8rem;
  color: #999;
  text-align: center;
}

.upload-link {
  background: var(--color-accent-orange);
  color: white;
  text-decoration: none;
  border: none;
  border-radius: 12px;
  padding: 0.6rem 1rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.upload-link:hover {
  opacity: 0.9;
}

.status-uploaded {
  background-color: #d1fae5;
  color: #059669;
}

.status-pending {
  background-color: #fef3c7;
  color: #b45309;
}

.status-rejected {
  background-color: #fee2e2;
  color: #b91c1c;
}

.upload-tag {
  display: inline-block;
  padding: 0.25rem 0.6rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 600;
}

/* Reviews */
.review-card {
  background: white;
  border: 1px solid var(--color-light-gray);
  border-radius: var(--radius-lg);
  padding: 1.25rem;
  margin-bottom: 1rem;
}

.review-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.review-top h3 {
  margin: 0;
}

.review-rating {
  color: #f5b301;
}

.review-footer {
  margin-top: 0.5rem;
  font-size: 0.8rem;
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

.skeleton-stat {
  background: #fff;
}

/* Responsive */
@media (max-width: 768px) {
  .stats-section {
    grid-template-columns: 1fr;
  }
  .book-grid {
    grid-template-columns: 1fr;
  }
  .profile-header {
    flex-direction: column;
    text-align: center;
  }
}
</style>