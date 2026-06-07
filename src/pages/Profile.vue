<template>
  <div class="profile-page">

```
<div class="container">

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

      <span v-else>
        👤
      </span>

    </div>

    <input
      ref="avatarInput"
      type="file"
      accept="image/*"
      style="display: none"
      @change="handleAvatarChange"
    />

    <div class="profile-info">
      <h1 class="profile-name">{{ currentUser.name }}</h1>
      <p class="profile-email">{{ currentUser.email }}</p>
    </div>

  </section>

  <!-- Stats -->
  <section class="stats-section">

    <div class="stat-card">
      <span class="stat-number">{{ favourites.length }}</span>
      <span class="stat-label">Favorites</span>
    </div>

    <div class="stat-card">
      <span class="stat-number">{{ uploads.length }}</span>
      <span class="stat-label">Uploads</span>
    </div>

    <div class="stat-card">
      <span class="stat-number">{{ comments.length }}</span>
      <span class="stat-label">Reviews</span>
    </div>

  </section>

  <!-- Favourite Books -->
  <section class="section">

    <div class="section-header">
      <h2>Favourite Books</h2>
    </div>

    <div class="book-grid">

      <div
        class="book-card"
        v-for="book in favourites"
        :key="book.id"
      >
      <router-link
        :to="`/book/${book.id}`"
        class="book-link"
      >

        <h3>{{ book.title }}</h3>
        <p>{{ book.author }}</p>

      </router-link>
        
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

      <div
        class="book-card"
        v-for="book in myUploads"
        :key="book.id"
        @click="goToDetail(book)"
        :class="{ 'disabled-card': book.status !== 'Uploaded' }"
      >
        <div class="book-cover">
          <img
            v-if="book.cover"
            :src="book.cover"
            alt="book cover"
          />
          <div v-else class="book-placeholder">
            No cover
          </div>
        </div>

        <h3>{{ book.title }}</h3>
        <p>{{ book.author }}</p>
        <span
          class="upload-tag"
          :class="statusClass(book.status)"
        >
          {{ book.status }}
        </span>
      </div>

    </div>

  </section>

  <!-- Reviews -->
  <section class="section">

    <div class="section-header">
      <h2>My Reviews</h2>
    </div>

    <router-link
    v-for="review in comments"
    :key="review.id"
    :to="`/book/${review.bookId}`"
    class="book-link"
    >
      <div
        class="review-card"
      > 

      <div class="review-top">
          <h3>{{ review.book }}</h3>

        <div class="review-rating">

          <span
            v-for="star in 5"
            :key="star"
          >
            {{ star <= review.rating ? '★' : '☆' }}
          </span>

        </div>

      </div>

      <p>
        {{ review.content }}
      </p>

    </div>
    </router-link>

  </section>

</div>
```

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter} from 'vue-router'

import { favourites } from '../stores/favouriteStore'
import { uploads } from '../stores/uploadsStore'
import { reviews } from '../stores/reviewStore'
import { useAuth } from '../composables/useAuth'

const { currentUser } = useAuth()
const router = useRouter()

const avatarInput = ref(null)

const avatar = ref(
  localStorage.getItem('avatar')
)

function triggerAvatarUpload() {
  avatarInput.value.click()
}

function handleAvatarChange(event) {

  const file = event.target.files[0]

  if (!file) return

  const imageUrl = URL.createObjectURL(file)

  avatar.value = imageUrl

  localStorage.setItem(
    'avatar',
    imageUrl
  )
}

const comments = computed(() => {

  if (!currentUser.value) {
    return []
  }

  return reviews.value.filter(
    review =>
      review.userId === currentUser.value.id
  )

})

const myUploads = uploads 

function statusClass(status) {
  switch (status) {
    case 'Uploaded':
      return 'status-uploaded'
    case 'Pending':
      return 'status-pending'
    case 'Rejected':
      return 'status-rejected'
  }
}

function goToDetail(book) {
  if (book.status === 'Uploaded') {
    router.push(`/book/${book.id}`)
  } else {
    alert('You can only access the detail page after it is uploaded.')
  }
}



</script>

<style scoped>

.profile-page {
  padding: 4rem 0;
  background: var(--color-light);
}

/* Header */

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
  grid-template-columns: repeat(3,1fr);
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
  grid-template-columns: repeat(3,1fr);
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
  box-shadow: 0 8px 24px rgba(0,0,0,0.06);
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

  font-size: 2rem;
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
