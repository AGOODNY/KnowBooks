<template>
  <form class="search-bar" @submit.prevent="handleSubmit">
    <input
      type="text"
      class="search-input"
      placeholder="Search books you like"
      v-model="query"
    />
    <button type="submit" class="search-btn" title="Search">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="11" cy="11" r="8" />
        <line x1="21" y1="21" x2="16.65" y2="16.65" />
      </svg>
    </button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const query = ref('')
const router = useRouter()

function handleSubmit() {
  if (query.value.trim()) {
    router.push(`/search?keyword=${encodeURIComponent(query.value.trim())}`)
  }
}
</script>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  background: var(--color-light);
  border: 1px solid var(--color-light-gray);
  border-radius: 20px;
  overflow: hidden;
  transition: border-color 0.15s;
}

.search-bar:focus-within {
  border-color: var(--color-mid-gray);
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  padding: 0.45rem 0.75rem 0.45rem 1rem;
  font-family: var(--font-body);
  font-size: 0.9rem;
  color: var(--color-dark);
}

.search-input::placeholder {
  color: var(--color-mid-gray);
}

.search-btn {
  background: none;
  padding: 0.45rem 0.75rem;
  color: var(--color-mid-gray);
  display: flex;
  align-items: center;
  transition: color 0.15s;
}

.search-btn:hover {
  color: var(--color-dark);
}
</style>
