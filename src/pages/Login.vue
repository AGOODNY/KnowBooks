<template>
  <div class="auth-page">

    <div class="auth-card">

      <h1>Welcome Back</h1>

      <p class="subtitle">
        Log in to continue your reading journey.
      </p>

      <form @submit.prevent="handleLogin">

        <div class="form-group">
          <label>Email</label>

          <input
            v-model="email"
            type="email"
            placeholder="Enter your email"
            required
          >
        </div>

        <div class="form-group">
          <label>Password</label>

          <input
            v-model="password"
            type="password"
            placeholder="Enter your password"
            required
          >
        </div>

        <button
          class="btn-primary"
          type="submit"
        >
          Log In
        </button>

      </form>

      <p class="bottom-text">
        Don't have an account?

        <span @click="router.push('/signup')">
          Sign up
        </span>
      </p>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import { useAuth } from '../composables/useAuth'

import axios from 'axios'

const router = useRouter()

const email = ref('')
const password = ref('')

const {
  login,
  isAuthenticated
} = useAuth()

onMounted(() => {
  if (isAuthenticated.value) {
    router.push('/home')
  }
})

const handleLogin = async () => {

  try {
    const res = await axios.post(
      'http://127.0.0.1:8000/api/users/login/',
      {
        email: email.value,
        password: password.value
      }
    )

    const token = res.data.access

    // 获取当前用户信息
    const me = await axios.get(
      'http://127.0.0.1:8000/api/users/me/',
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    login({
      user: me.data,
      jwt: token
    })

    router.push('/home')

  }
  catch(err){
    alert(
      err.response?.data?.error ||
      err.response?.data?.detail ||
      'Login Failed'
    )
  }

}
</script>

<style scoped>
/* Page Container */
.auth-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: var(--color-bg-secondary);
}

/* Form Card */
.auth-card {
  width: 420px;
  background: white;
  padding: 3rem;
  border-radius: 24px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.06);
}

/* Title */
h1 {
  font-family: var(--font-heading);
  margin-bottom: 0.5rem;
}

.subtitle {
  color: var(--color-mid-gray);
  margin-bottom: 2rem;
  text-align: center;
}

/* Forms */
.form-group {
  margin-bottom: 1.25rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
}

input {
  width: 100%;
  padding: 0.85rem 1rem;
  border: 1px solid var(--color-light-gray);
  border-radius: 12px;
  outline: none;
  transition: border-color 0.2s;
}

input:focus {
  border-color: var(--color-accent-orange);
}

/* Buttons */
.btn-primary {
  width: 100%;
  margin-top: 1rem;
  padding: 0.9rem;
  border: none;
  border-radius: 12px;
  background: var(--color-accent-orange);
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-primary:hover {
  opacity: 0.88;
}

/* Bottom Texts */
.bottom-text {
  margin-top: 1.5rem;
  text-align: center;
}

.bottom-text span {
  color: var(--color-accent-orange);
  cursor: pointer;
  font-weight: 600;
}
</style>