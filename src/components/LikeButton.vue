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

// 获取点赞状态和数量
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
    console.error('获取点赞状态失败:', err)
  }
}

// 切换点赞
const toggleLike = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('Please log in first')
    return
  }

  try {
    if (liked.value) {
      // 取消点赞
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
      // 点赞
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
    console.error('点赞操作失败:', err)
    alert(err.response?.data?.error || '操作失败，请重试')
  }
}

onMounted(() => {
  fetchLikeStatus()
})

// 监听 book.id 变化，重新获取状态（如果页面内切换书籍）
watch(() => props.book.id, () => {
  fetchLikeStatus()
})
</script>