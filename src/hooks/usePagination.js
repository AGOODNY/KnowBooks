import { useState, useCallback } from 'react'

function usePagination({ fetchFn, pageSize = 10 }) {
  const [data, setData] = useState([])
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [loading, setLoading] = useState(false)

  const loadPage = useCallback(async (pageNum) => {
    setLoading(true)
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 300))

    const result = fetchFn(pageNum, pageSize)
    setData(result.items)
    setTotalPages(Math.max(1, Math.ceil(result.total / pageSize)))
    setPage(pageNum)
    setLoading(false)
  }, [fetchFn, pageSize])

  const goToPage = useCallback((pageNum) => {
    if (pageNum >= 1 && pageNum <= totalPages) {
      loadPage(pageNum)
    }
  }, [totalPages, loadPage])

  const reset = useCallback(() => {
    setData([])
    setPage(1)
    setTotalPages(1)
  }, [])

  return {
    data,
    page,
    totalPages,
    loading,
    loadPage,
    goToPage,
    reset,
  }
}

export default usePagination
