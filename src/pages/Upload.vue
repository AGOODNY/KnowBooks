<template>
  <div class="upload-page">
    <div class="container">
      <div class="upload-card">
        <h1 class="page-title">
          Upload a Book
        </h1>
        <p class="page-subtitle">
          Share a book with the KnowBooks community.
        </p>
        
        <!-- 页面整体加载 -->
        <div v-if="isPageLoading" class="loading-container">
          <div class="spinner"></div>
          <p>Loading upload form...</p>
        </div>

        <form v-else @submit.prevent="handleSubmit">
          <!-- Cover Upload -->
          <div class="form-group">
            <label>
              Book Cover
            </label>
            <div 
              class="upload-area"
              @click="triggerFileInput"
            >
              <template v-if="!previewImage">
                <div class="upload-icon">
                  +
                </div>
                <p>Upload Cover</p>
              </template>
              <img
                v-else
                :src="previewImage"
                alt="Book Cover"
                class="preview-image"
              >
            </div>
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              class="hidden-input"
              @change="handleImageUpload"
            />
          </div>

          <!-- Title -->
          <div class="form-group">
            <label>
              Title
            </label>
            <input
              v-model="book.title"
              type="text"
              placeholder="Book title"
              required
            />
          </div>

          <!-- Author -->
          <div class="form-group">
            <label>
              Author
            </label>
            <input
              v-model="book.author"
              type="text"
              placeholder="Author name"
              required
            />
          </div>

          <!-- Tags - 多选下拉框 -->
          <div class="form-group">
            <label>
              Tags
            </label>
            
            <!-- 标签加载骨架屏 -->
            <div v-if="loadingTags" class="tags-loading-skeleton">
              <div class="skeleton" style="height: 52px; border-radius: 12px;"></div>
            </div>
            
            <div v-else class="tags-select-container">
              <div 
                class="tags-select-trigger"
                @click="toggleDropdown"
                :class="{ 'is-open': isDropdownOpen }"
              >
                <div class="selected-tags">
                  <span v-if="selectedTags.length === 0" class="placeholder">
                    Select tags...
                  </span>
                  <span v-else class="selected-count">
                    {{ selectedTags.length }} tag(s) selected
                  </span>
                </div>
                <span class="dropdown-arrow">▼</span>
              </div>
              
              <div v-if="isDropdownOpen" class="tags-dropdown">
                <div 
                  v-for="tag in allTags" 
                  :key="tag.id"
                  class="tag-option"
                  @click="toggleTag(tag)"
                >
                  <input 
                    type="checkbox" 
                    :checked="isTagSelected(tag)"
                    @click.stop
                  />
                  <span class="tag-name">{{ tag.name }}</span>
                  <span class="tag-count">({{ tag.count || 0 }})</span>
                </div>
                <div v-if="allTags.length === 0" class="no-tags">
                  No tags available
                </div>
              </div>
            </div>
            <small>Select one or more tags for your book</small>
          </div>

          <!-- Description -->
          <div class="form-group">
            <label>
              Description
            </label>
            <textarea
              v-model="book.description"
              placeholder="Write a short description..."
            />
          </div>

          <button
            type="submit"
            class="btn-submit"
            :disabled="submitting || loadingTags"
          >
            {{ submitting ? 'Uploading...' : 'Upload Book' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// 加载状态
const isPageLoading = ref(true)
const loadingTags = ref(false)

const selectedFile = ref(null)
const previewImage = ref('')
const submitting = ref(false)

// 标签相关
const allTags = ref([])
const selectedTags = ref([])
const isDropdownOpen = ref(false)

const book = ref({
  title: '',
  author: '',
  description: ''
})

const fileInput = ref(null)

// 获取所有可用标签
const loadTags = async () => {
  loadingTags.value = true
  try {
    const res = await axios.get(
      'http://127.0.0.1:8000/api/recommendations/tags/cloud/'
    )
    allTags.value = res.data
  } catch (err) {
    console.error('Failed to load tags:', err)
    allTags.value = []
  } finally {
    loadingTags.value = false
  }
}

// 切换下拉框
const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value
}

// 关闭下拉框（点击其他地方时）
const closeDropdown = (event) => {
  const container = document.querySelector('.tags-select-container')
  if (container && !container.contains(event.target)) {
    isDropdownOpen.value = false
  }
}

// 检查标签是否被选中
const isTagSelected = (tag) => {
  return selectedTags.value.some(t => t.id === tag.id)
}

// 切换标签选中状态
const toggleTag = (tag) => {
  if (isTagSelected(tag)) {
    selectedTags.value = selectedTags.value.filter(t => t.id !== tag.id)
  } else {
    selectedTags.value.push(tag)
  }
}

function triggerFileInput() {
  fileInput.value.click()
}

function handleImageUpload(event) {
  const file = event.target.files[0]
  if (!file) return
  selectedFile.value = file
  previewImage.value = URL.createObjectURL(file)
}

async function handleSubmit() {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('Please log in first')
    router.push('/login')
    return
  }

  if (!book.value.title.trim()) {
    alert('Please enter a title')
    return
  }

  if (!book.value.author.trim()) {
    alert('Please enter an author')
    return
  }

  submitting.value = true

  try {
    const formData = new FormData()
    
    // 添加文本字段
    formData.append('title', book.value.title)
    formData.append('author', book.value.author)
    formData.append('description', book.value.description || '')
    
    // 添加封面图片
    if (selectedFile.value) {
      formData.append('cover', selectedFile.value)
    }
    
    if (selectedTags.value.length > 0) {
      selectedTags.value.forEach(tag => {
        formData.append('existing_tag_ids', tag.id)
      })
    }

    const res = await axios.post(
      'http://127.0.0.1:8000/api/recommendations/books/',
      formData,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      }
    )

    alert('Book uploaded successfully! It will be reviewed by an admin.')
    resetForm()
    router.push('/profile')

  } catch (err) {
    console.error('Upload error:', err)
    console.error('Error response:', err.response?.data)
    
    let errorMsg = 'Upload failed. Please try again.'
    if (err.response?.data?.existing_tag_ids) {
      errorMsg = `Tag error: ${err.response.data.existing_tag_ids.join(', ')}`
    } else if (err.response?.data?.error) {
      errorMsg = err.response.data.error
    } else if (err.response?.data?.detail) {
      errorMsg = err.response.data.detail
    }
    alert(errorMsg)
  } finally {
    submitting.value = false
  }
}

function resetForm() {
  book.value = {
    title: '',
    author: '',
    description: ''
  }
  selectedTags.value = []
  selectedFile.value = null
  previewImage.value = ''
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

// 页面初始化
onMounted(async () => {
  isPageLoading.value = true
  await loadTags()
  isPageLoading.value = false
  document.addEventListener('click', closeDropdown)
})
</script>

<style scoped>
.upload-page {
  padding: 4rem 0;
}

.upload-card {
  max-width: 800px;
  margin: auto;
  background: white;
  border: 1px solid var(--color-light-gray);
  border-radius: 24px;
  padding: 3rem;
}

.page-title {
  font-family: var(--font-heading);
  font-size: 2rem;
  margin-bottom: .5rem;
}

.page-subtitle {
  color: var(--color-mid-gray);
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: .5rem;
  font-weight: 600;
}

input,
select,
textarea {
  width: 100%;
  padding: .9rem 1rem;
  border: 1px solid var(--color-light-gray);
  border-radius: 12px;
  font-size: .95rem;
}

/* 标签选择器样式 */
.tags-select-container {
  position: relative;
  user-select: none;
}

.tags-select-trigger {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: .9rem 1rem;
  border: 1px solid var(--color-light-gray);
  border-radius: 12px;
  background: white;
  cursor: pointer;
  transition: border-color 0.2s;
}

.tags-select-trigger:hover {
  border-color: var(--color-accent-orange);
}

.tags-select-trigger.is-open {
  border-color: var(--color-accent-orange);
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}

.selected-tags {
  flex: 1;
}

.placeholder {
  color: #999;
}

.selected-count {
  color: var(--color-dark);
  font-weight: 500;
}

.dropdown-arrow {
  color: var(--color-mid-gray);
  font-size: 0.7rem;
  transition: transform 0.2s;
}

.tags-select-trigger.is-open .dropdown-arrow {
  transform: rotate(180deg);
}

.tags-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  max-height: 250px;
  overflow-y: auto;
  background: white;
  border: 1px solid var(--color-light-gray);
  border-top: none;
  border-radius: 0 0 12px 12px;
  z-index: 100;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.tag-option {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.7rem 1rem;
  cursor: pointer;
  transition: background 0.15s;
}

.tag-option:hover {
  background: var(--color-light-gray);
}

.tag-option input {
  width: 18px;
  height: 18px;
  cursor: pointer;
  margin: 0;
  padding: 0;
}

.tag-name {
  flex: 1;
  font-size: 0.9rem;
  color: var(--color-dark);
}

.tag-count {
  font-size: 0.75rem;
  color: var(--color-mid-gray);
}

.no-tags {
  padding: 1rem;
  text-align: center;
  color: var(--color-mid-gray);
}

.upload-area {
  width: 220px;
  height: 300px;
  border: 2px dashed var(--color-light-gray);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all .2s ease;
  overflow: hidden;
}

.upload-area:hover {
  border-color: var(--color-accent-orange);
  background: rgba(255, 140, 0, 0.03);
}

.upload-icon {
  font-size: 4rem;
  line-height: 1;
  color: var(--color-accent-orange);
  margin-bottom: .5rem;
}

.upload-area p {
  color: var(--color-mid-gray);
  margin: 0;
}

.hidden-input {
  display: none;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

textarea {
  min-height: 140px;
  resize: vertical;
}

.preview {
  margin: 2rem 0;
  text-align: center;
}

.preview h3 {
  margin-bottom: 1rem;
}

.preview img {
  width: 220px;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0,0,0,.08);
}

.btn-submit {
  background: var(--color-accent-orange);
  color: white;
  border: none;
  border-radius: 12px;
  padding: .9rem 1.5rem;
  font-weight: 600;
  cursor: pointer;
}

.btn-submit:hover {
  opacity: .9;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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

.tags-loading-skeleton {
  width: 100%;
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

@media (max-width: 768px) {
  .upload-card {
    padding: 2rem;
  }
  .preview img {
    width: 180px;
  }
}
</style>