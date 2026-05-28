<template>
  <div class="placeholder">
    <div class="placeholder-inner">
      <span class="placeholder-icon">{{ icon }}</span>
      <h2 class="placeholder-title">{{ pageTitle }}</h2>
      <p class="placeholder-text">Page under development...</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  pageTitle: String,
  icon: { type: String, default: '\u{1F4C4}' },
})
</script>

<style scoped>
.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 64px);
  padding: 2rem;
}

.placeholder-inner {
  text-align: center;
}

.placeholder-icon {
  font-size: 2.5rem;
  display: block;
  margin-bottom: 1rem;
}

.placeholder-title {
  font-family: var(--font-heading);
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-dark);
  margin-bottom: 0.5rem;
}

.placeholder-text {
  color: var(--color-mid-gray);
  font-size: 0.95rem;
}
</style>
