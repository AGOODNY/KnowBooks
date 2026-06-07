<template>
  <button class="btn-like" @click="toggleFavourite">
    {{ isFavorited ? '🔖 Saved' : '📑 Save' }}
  </button>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
  book: {
    type: Object,
    required: true
  }
})

const isFavorited = ref(false)

// Fetch favorite status (backend has no GET endpoint, default to false)
const fetchFavoriteStatus = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) return
  
  if (!props.book?.id) {
    console.warn('FavoriteButton: book.id is missing', props.book)
    return
  }

  try {
    // Backend has no GET endpoint, cannot fetch user's favorite status
    // Can get from localStorage or props.book, default to false if not available
    isFavorited.value = props.book.is_favorited || false
  } catch (err) {
    console.error('Failed to fetch favorite status:', err)
  }
}

// Toggle favorite
const toggleFavourite = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('Please log in first')
    return
  }

  if (!props.book?.id) {
    console.error('FavoriteButton: Cannot toggle favorite, book.id is missing')
    return
  }

  try {
    // Backend only accepts POST request to toggle favorite status
    await axios.post(
      `http://127.0.0.1:8000/api/interactions/favorite/${props.book.id}/`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    
    // Toggle local status
    isFavorited.value = !isFavorited.value
    
  } catch (err) {
    console.error('Favorite operation failed:', err)
    alert(err.response?.data?.error || 'Operation failed, please try again')
  }
}

onMounted(() => {
  fetchFavoriteStatus()
})

// Watch for book.id changes
watch(() => props.book?.id, (newId) => {
  if (newId) {
    fetchFavoriteStatus()
  }
})
</script>