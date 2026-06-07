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
        <form @submit.prevent="handleSubmit">
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

          <!-- Tags -->
          <div class="form-group">
            <label>
              Tags (comma separated)
            </label>
            <input
              v-model="tagsInput"
              type="text"
              placeholder="e.g., Fiction, Fantasy, Romance"
            />
            <small>Separate multiple tags with commas</small>
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
            :disabled="submitting"
          >
            {{ submitting ? 'Uploading...' : 'Upload Book' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const selectedFile = ref(null)
const previewImage = ref('')
const submitting = ref(false)
const tagsInput = ref('')

const book = ref({
  title: '',
  author: '',
  description: ''
})

const fileInput = ref(null)

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
    // 处理标签：将逗号分隔的字符串转换为数组
    let tagNames = []
    if (tagsInput.value.trim()) {
      tagNames = tagsInput.value
        .split(',')
        .map(t => t.trim())
        .filter(t => t !== '')
    }

    // 使用 FormData（支持文件上传）
    const formData = new FormData()
    
    // 添加文本字段
    formData.append('title', book.value.title)
    formData.append('author', book.value.author)
    formData.append('description', book.value.description || '')
    
    // 添加封面图片
    if (selectedFile.value) {
      formData.append('cover', selectedFile.value)
    }
    
    if (tagNames.length > 0) {
      formData.append('new_tag_names', JSON.stringify(tagNames))
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
    if (err.response?.data?.new_tag_names) {
      errorMsg = `Tag error: ${err.response.data.new_tag_names.join(', ')}`
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
  tagsInput.value = ''
  selectedFile.value = null
  previewImage.value = ''
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}
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

@media (max-width: 768px) {
  .upload-card {
    padding: 2rem;
  }
  .preview img {
    width: 180px;
  }
}
</style>