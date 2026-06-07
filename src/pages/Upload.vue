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

          <!-- Preview -->

          <div
            v-if="previewImage"
            class="preview"
          >

            <h3>Cover Preview</h3>

            <img
              :src="previewImage"
              alt="Book Cover"
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

          <!-- Category -->

          <div class="form-group">

            <label>
              Category
            </label>

            <select v-model="book.category">

              <option>Fiction</option>
              <option>Fantasy</option>
              <option>Science Fiction</option>
              <option>Romance</option>
              <option>Biography</option>
              <option>History</option>

            </select>

          </div>

          <!-- Year -->

          <div class="form-group">

            <label>
              Publish Year
            </label>

            <input
              v-model="book.year"
              type="number"
              placeholder="2024"
            />

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
          >
            Upload Book
          </button>

        </form>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { uploads } from '../stores/uploadsStore'

const router = useRouter()

const selectedFile = ref(null)
const previewImage = ref('')

const book = ref({
  title: '',
  author: '',
  category: 'Fiction',
  year: '',
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

function handleSubmit() {

  const formData = new FormData()
  formData.append('cover', selectedFile.value)
  formData.append('title', book.value.title)
  formData.append('author', book.value.author)
  formData.append('category', book.value.category)
  formData.append('year', book.value.year)
  formData.append('description', book.value.description)

  uploads.value.push({
    id: Date.now(), 
    title: book.value.title,
    author: book.value.author,
    category: book.value.category,
    year: book.value.year,
    description: book.value.description,
    cover: selectedFile.value,
    status: 'Pending'
  })

  alert('The uploading request is sent successfully!')

  resetForm()

  router.push('/profile')
}

function resetForm() {

  book.value = {
    title: '',
    author: '',
    category: 'Fiction',
    year: '',
    description: ''
  }

  selectedFile.value = null
  previewImage.value = ''
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

@media (max-width: 768px) {

  .upload-card {
    padding: 2rem;
  }

  .preview img {
    width: 180px;
  }

}
</style>