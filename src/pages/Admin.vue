<template>
  <div class="admin-page">
    <div class="container">
      <h1>Book Approval Dashboard</h1>
      
      <!-- 全局加载 -->
      <div v-if="isPageLoading" class="loading-container">
        <div class="spinner"></div>
        <p>Loading pending books...</p>
      </div>

      <!-- 内容区域 -->
      <template v-else>
        <div v-if="loading" class="loading">Loading...</div>
        <div v-else-if="pendingBooks.length === 0" class="empty-state">
          <p>No pending books for approval.</p>
        </div>
        <div
          v-else
          v-for="book in pendingBooks"
          :key="book.id"
          class="admin-card"
        >
          <img
            :src="getCoverUrl(book.cover)"
            class="admin-cover"
            alt="cover"
          />
          <div>
            <h3>{{ book.title }}</h3>
            <p>{{ book.author }}</p>
            <p class="uploader-info">Uploaded by: {{ book.uploaded_by?.username || book.uploaded_by?.email || 'Unknown' }}</p>
          </div>
          <div class="actions">
            <button
              class="btn-approve"
              @click="approveBook(book)"
              :disabled="loading"
            >
              Approve
            </button>
            <button
              class="btn-reject"
              @click="rejectBook(book)"
              :disabled="loading"
            >
              Reject
            </button>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const pendingBooks = ref([])
const loading = ref(false)
const isPageLoading = ref(true)

// 获取封面图片完整 URL
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

// 获取待审批的书籍列表
const loadPendingBooks = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('Please log in first')
    isPageLoading.value = false
    return
  }

  loading.value = true
  try {
    const res = await axios.get(
      'http://127.0.0.1:8000/api/recommendations/books/pending/',
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    pendingBooks.value = res.data
    console.log('Pending books:', res.data)
  } catch (err) {
    console.error('Error details:', err.response)
    if (err.response?.status === 401) {
      alert('Please log in again')
    } else if (err.response?.status === 403) {
      alert('You do not have admin permission. Please login with an admin account.')
    } else {
      alert(`Failed to load pending books: ${err.response?.data?.detail || err.message}`)
    }
  } finally {
    loading.value = false
    isPageLoading.value = false
  }
}

// 批准书籍
const approveBook = async (book) => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('Please log in as admin')
    return
  }

  loading.value = true
  try {
    await axios.post(
      `http://127.0.0.1:8000/api/recommendations/books/${book.id}/approve/`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    pendingBooks.value = pendingBooks.value.filter(b => b.id !== book.id)
    alert(`"${book.title}" has been approved`)
  } catch (err) {
    console.error(err)
    alert('Failed to approve book')
  } finally {
    loading.value = false
  }
}

// 拒绝书籍
const rejectBook = async (book) => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('Please log in as admin')
    return
  }

  loading.value = true
  try {
    await axios.post(
      `http://127.0.0.1:8000/api/recommendations/books/${book.id}/reject/`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    pendingBooks.value = pendingBooks.value.filter(b => b.id !== book.id)
    alert(`"${book.title}" has been rejected`)
  } catch (err) {
    console.error(err)
    alert('Failed to reject book')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadPendingBooks()
})
</script>

<style scoped>
.admin-page {
  padding: 4rem 0;
}

.admin-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border: 1px solid #eee;
  border-radius: 12px;
  margin-bottom: 1rem;
}

.admin-cover {
  width: 80px;
  height: 110px;
  object-fit: cover;
  border-radius: 8px;
}

.actions {
  display: flex;
  gap: 0.75rem;
}

.btn-approve {
  background: #d9704a;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.btn-reject {
  background: #8c8982;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.btn-approve:hover, .btn-reject:hover {
  opacity: 0.9;
}

.btn-approve:disabled, .btn-reject:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.uploader-info {
  font-size: 0.8rem;
  color: #666;
  margin-top: 4px;
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
  border: 3px solid var(--color-light-gray, #e0e0e0);
  border-top-color: var(--color-accent-orange, #d9704a);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading {
  text-align: center;
  padding: 3rem 0;
  color: var(--color-mid-gray, #888);
  font-size: 0.9rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 0;
  color: var(--color-mid-gray, #888);
}
</style>