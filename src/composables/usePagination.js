import { ref } from 'vue'

export function usePagination({ fetchFn, pageSize = 10 }) {
  const data = ref([])
  const page = ref(1)
  const totalPages = ref(1)
  const loading = ref(false)

  async function loadPage(pageNum) {
    loading.value = true
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 300))

    const result = fetchFn(pageNum, pageSize)
    data.value = result.items
    totalPages.value = Math.max(1, Math.ceil(result.total / pageSize))
    page.value = pageNum
    loading.value = false
  }

  function goToPage(pageNum) {
    if (pageNum >= 1 && pageNum <= totalPages.value) {
      loadPage(pageNum)
    }
  }

  function reset() {
    data.value = []
    page.value = 1
    totalPages.value = 1
  }

  return { data, page, totalPages, loading, loadPage, goToPage, reset }
}
