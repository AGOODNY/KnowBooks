// src/stores/userStore.js

import { ref } from 'vue'
import { defaultUsers } from '../data/mockUsers'

const storedUsers = localStorage.getItem('users')

export const users = ref(
  storedUsers
    ? JSON.parse(storedUsers)
    : defaultUsers
)

export function saveUsers() {
  localStorage.setItem(
    'users',
    JSON.stringify(users.value)
  )
}