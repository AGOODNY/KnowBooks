<template>

  <button
    class="btn-like"
    @click="toggleLike"
  >
    {{ liked ? '❤️ Liked' : '🤍 Like' }}
    ({{ likes }})
  </button>

</template>

<script setup>
import { ref } from 'vue'

const liked = ref(false)

const likes = ref(125)

const toggleLike = () => {

  if (liked.value) {
    likes.value--
  } else {
    likes.value++
  }

  liked.value = !liked.value
}
</script>