<template>
  <div class="auth-page">

    <div class="auth-card">

      <!-- 标题 -->
      <h1>Create Account</h1>
      <p class="subtitle">
        Join the KnowBooks community.
      </p>

      <!-- 注册表单 -->
      <form @submit.prevent="handleSignup">

        <div class="form-group">
          <label>Username</label>
          <input
            v-model="username"
            type="text"
            placeholder="Enter your username"
            required
          >
        </div>

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
          Sign up
        </button>

      </form>

      <!-- 跳转登录 -->
      <p class="bottom-text">
        Already have an account?
        <span @click="router.push('/login')">Log in</span>
      </p>

    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {users, saveUsers } from '../stores/userStore'

const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')

const handleSignup = () => {
  const exists = users.value.find(
    u => u.email === email.value
  )

  if (exists) {
    alert('Email already exists')
    return
  }

  users.value.push({
    id: Date.now(),
    username: username.value,
    email: email.value,
    password: password.value,
    role: 'user'
  })

  saveUsers()

  alert('Account created successfully!')

  router.push('/login')
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