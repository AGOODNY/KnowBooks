<template>
  <div class="book-detail-page">

    <div class="container">

      <!-- Book Hero -->
      <section class="book-hero">

        <div class="book-cover">
          <img
            :src="book.cover"
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

            <LikeButton/>
            <FavoriteButton :book="book" />

          </div>

        </div>

      </section>

      <!-- Reviews -->

      <section class="review-section">

        <h2 class="section-title">
          Reviews
        </h2>

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
                  {{ star <= review.rating ? '★' : '☆' }}
                </span>

              </div>

            </div>

            <p class="review-content">
              {{ review.content }}
            </p>

            <span class="review-date">
              {{ review.date }}
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

      </section>

    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import LikeButton from '../components/LikeButton.vue'
import FavoriteButton from '../components/FavoriteButton.vue'
import { useAuth } from '../composables/useAuth.js'
import { useRoute } from 'vue-router'
import { mockBooks } from '../data/mockData'
import { reviews } from '../stores/reviewStore'

const route = useRoute()

const {currentUser} = useAuth()

const bookId = Number(route.params.id)

const book = ref(
  mockBooks. find(
    b => b.id === bookId
  )
)

const liked = ref(false)
const favourite = ref(false)

const selectedRating = ref(0)

const newReview = ref('')

const bookReviews = computed(() =>
  reviews.value.filter(
    review => review.bookId === bookId
  )
)

const averageRating = computed(() => {

  if (bookReviews.value.length === 0) {
    return '0.0'
  }

  const total = bookReviews.value.reduce(
    (sum, review) => sum + review.rating,
    0
  )

  return (
    total / bookReviews.value.length
  ).toFixed(1)

})

function toggleLike() {
  liked.value = !liked.value
}

function toggleFavourite() {
  favourite.value = !favourite.value
}

const submitReview = () => {

  if (!currentUser.value) {
    alert('Please log in first')
    return
  }

  if (!newReview.value.trim()) {
    return
  }

  reviews.value.push({

    id: Date.now(),

    userId: currentUser.value.id,

    username: currentUser.value.username,

    bookId: book.value.id,

    book: book.value.title,

    rating: selectedRating.value,

    content: newReview.value,

    date: new Date().toLocaleDateString()

  })

  newReview.value = ''
  selectedRating.value = 0
}
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

}
</style>