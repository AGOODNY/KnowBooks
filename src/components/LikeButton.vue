<template>
  <button
    class="btn-like"
    @click="toggleLike"
  >
    {{ liked ? '❤️ Liked' : '🤍 Like' }}
    ({{ likesCount }})
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

const liked = ref(false)
const likesCount = ref(0)


const fetchLikeStatus = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) return

  try {
    const res = await axios.get(
      `http://127.0.0.1:8000/api/interactions/like/${props.book.id}/`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    liked.value = res.data.is_liked || false
    likesCount.value = res.data.likes_count || 0
  } catch (err) {
    console.error('Failed to fetch like status:', err)
  }
}

// Toggle like
const toggleLike = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('Please log in first')
    return
  }

  try {
    if (liked.value) {
      // Unlike
      await axios.delete(
        `http://127.0.0.1:8000/api/interactions/like/${props.book.id}/`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
      likesCount.value--
    } else {
      // Like
      await axios.post(
        `http://127.0.0.1:8000/api/interactions/like/${props.book.id}/`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
      likesCount.value++
    }
    liked.value = !liked.value
  } catch (err) {
    console.error('Like operation failed:', err)
    alert(err.response?.data?.error || 'Operation failed, please try again')
  }
}

onMounted(() => {
  fetchLikeStatus()
})

watch(() => props.book.id, () => {
  fetchLikeStatus()
})
</script>