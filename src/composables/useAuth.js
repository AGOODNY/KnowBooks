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

let storedToken = localStorage.getItem('access_token')

const currentUser = ref(parsedUser)
const token = ref(storedToken)

export function useAuth() {

  const login = ({ user, jwt }) => {
    currentUser.value = user
    localStorage.setItem('user', JSON.stringify(user))

    token.value = jwt
    localStorage.setItem('access_token', jwt)  // 改为 access_token
  }

  const logout = () => {
    currentUser.value = null
    token.value = null
    localStorage.removeItem('user')
    localStorage.removeItem('access_token')  // 改为 access_token
  }

  const isAuthenticated = computed(() => !!token.value)

  const isAdmin = computed(() => {
    return currentUser.value?.is_staff === true || currentUser.value?.role === 'admin'
  })

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