// src/composables/useAuth.js
import { ref, computed } from 'vue'

let storedUser = localStorage.getItem('user')
let parsedUser = null
try {
  parsedUser = storedUser && storedUser !== 'undefined'
    ? JSON.parse(storedUser)
    : null
} catch (e) {
  parsedUser = null
}

const currentUser = ref(parsedUser)

// token
const token = ref(localStorage.getItem('token'))

export function useAuth() {

  const login = ({ user, jwt }) => {
    currentUser.value = user
    localStorage.setItem('user', JSON.stringify(user))

    token.value = jwt
    localStorage.setItem('token', jwt)
  }

  const logout = () => {
    currentUser.value = null
    token.value = null
    localStorage.removeItem('user')
    localStorage.removeItem('token')
  }

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => currentUser.value?.role === 'admin')
  const getToken = () => token.value

  return {
    currentUser,
    token,
    isAuthenticated,
    isAdmin,
    login,
    logout,
    getToken
  }
}