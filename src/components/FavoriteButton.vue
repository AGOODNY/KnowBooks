<template>

<button class="btn-like" @click="toggleFavourite" > {{ favourite ? '🔖 Saved' : '📑 Save'}} </button>

</template>

<script setup>
import { computed } from 'vue'
import { favourites } from '../stores/favouriteStore'

const props = defineProps({
  book: {
    type: Object,
    required: true
  }
})


const favourite = computed(() =>
  favourites.value.some(b => b.id === props.book.id)
)

const toggleFavourite = () => {
  const index = favourites.value.findIndex(
    b => b.id === props.book.id
  )

  if (index !== -1) {
    favourites.value.splice(index, 1)
  } else {
    favourites.value.push(props.book)
  }

}
</script>