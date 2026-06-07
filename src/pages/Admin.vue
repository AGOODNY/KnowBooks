<template>

<div class="admin-page">

  <div class="container">

    <h1>Book Approval Dashboard</h1>

    <div
      v-for="book in pendingBooks"
      :key="book.id"
      class="admin-card"
    >
      <img
        :src="book.cover"
        class="admin-cover"
        alt="cover"
      />

      <div>

        <h3>{{ book.title }}</h3>

        <p>{{ book.author }}</p>

      </div>

      <div class="actions">

        <button
          class="btn-approve"
          @click="approveBook(book)"
        >
          Approve
        </button>

        <button
          class="btn-reject"
          @click="rejectBook(book)"
        >
          Reject
        </button>

      </div>

    </div>

  </div>

</div>

</template>

<script setup>
import { computed } from 'vue'
import { uploads } from '../stores/uploadsStore'


const pendingBooks = computed(() =>
  uploads.value.filter(
    book => book.status === 'Pending'
  )
)

const approveBook = (book) => {
  book.status = 'Uploaded'
}

const rejectBook = (book) => {
  book.status = 'Rejected'
}
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
  padding: 5px;
  border: 3px solid #eee;
  border-radius: 10px;
}

.btn-reject {
  background: #8c8982 ;
  color: white;
  padding: 5px;
  border: 3px solid #eee;
  border-radius: 10px;
}
</style>