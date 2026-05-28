<template>
  <p v-if="!tags || tags.length === 0" class="tag-cloud-empty">No tags available.</p>
  <div v-else class="tag-cloud">
    <router-link
      v-for="tag in tags"
      :key="tag.id"
      :to="`/search?tag=${encodeURIComponent(tag.name)}`"
      class="tag-cloud-item"
    >
      {{ tag.name }}
    </router-link>
  </div>
</template>

<script setup>
defineProps({
  tags: Array,
})
</script>

<style scoped>
.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag-cloud-empty {
  color: var(--color-mid-gray);
  font-size: 0.9rem;
}

.tag-cloud-item {
  font-family: var(--font-heading);
  font-size: 0.82rem;
  font-weight: 500;
  color: var(--color-dark);
  background: #fff;
  border: 1px solid var(--color-light-gray);
  padding: 0.35rem 0.85rem;
  border-radius: 20px;
  transition: background 0.15s, border-color 0.15s, color 0.15s;
}

.tag-cloud-item:hover {
  background: var(--color-accent-orange);
  border-color: var(--color-accent-orange);
  color: #fff;
}
</style>
