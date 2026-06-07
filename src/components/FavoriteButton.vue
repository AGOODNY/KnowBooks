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

// 获取收藏状态
const fetchFavoriteStatus = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) return

  try {
    const res = await axios.get(
      `http://127.0.0.1:8000/api/interactions/favorite/${props.book.id}/`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    isFavorited.value = res.data.is_favorited || false
  } catch (err) {
    console.error('获取收藏状态失败:', err)
  }
}

// 切换收藏
const toggleFavourite = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('Please log in first')
    return
  }

  try {
    if (isFavorited.value) {
      // 取消收藏
      await axios.delete(
        `http://127.0.0.1:8000/api/interactions/favorite/${props.book.id}/`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
      isFavorited.value = false
    } else {
      // 添加收藏
      await axios.post(
        `http://127.0.0.1:8000/api/interactions/favorite/${props.book.id}/`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
      isFavorited.value = true
    }
  } catch (err) {
    console.error('收藏操作失败:', err)
    alert(err.response?.data?.error || '操作失败，请重试')
  }
}

onMounted(() => {
  fetchFavoriteStatus()
})

// 监听 book.id 变化，重新获取状态（如果页面内切换书籍）
watch(() => props.book.id, () => {
  fetchFavoriteStatus()
})
</script>