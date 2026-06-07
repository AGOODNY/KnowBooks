<template>
  <nav class="navbar">
    <div class="navbar-inner">
      <div class="navbar-left">
        <button
          v-if="!isLanding"
          class="nav-back-btn"
          @click="router.back()"
          title="Go back"
        >
          &larr;
        </button>
        <router-link
          :to="isAuthenticated ? '/home' : '/'"
          class="navbar-brand"
        >
          KnowBooks
      </router-link>
      </div>

      <div
        v-if="!isLanding && !hideNavbarFeatures"
        class="navbar-center"
      >
        <SearchBar />
      </div>

      <div class="navbar-right">
        <template v-if="isLanding">
          <button class="btn-text" @click="router.push('/login')">Log in</button>
          <button class="btn-primary btn-sm" @click="router.push('/signup')">Sign up</button>
        </template>
       <div
          v-else-if="!hideNavbarFeatures"
          class="navbar-user"> 
          
          <div class="user-avatar">U</div>
          <span class="user-name">User</span>
          <div class="user-dropdown">
            <router-link to="/profile">Profile</router-link>
            <router-link v-if="isAdmin" to="/admin">Admin</router-link>
            <hr />
            <button class="btn-logout" @click="handleLogout" >Log out</button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SearchBar from './SearchBar.vue'
import { useAuth } from '../composables/useAuth'

const { isAdmin } = useAuth()

const route = useRoute()
const router = useRouter()
const isLanding = computed(() => route.path === '/')
const { isAuthenticated, logout } = useAuth()
const handleLogout = () => {
  logout()
  router.push('/')
}

const hideNavbarFeatures = computed(() =>
  route.path === '/login' ||
  route.path === '/signup'
)
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--color-light-gray);
  z-index: 100;
}

.navbar-inner {
  width: 100%;
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 1.5rem;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-shrink: 0;
}

.nav-back-btn {
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  font-size: 1.1rem;
  color: var(--color-mid-gray);
  border-radius: var(--radius);
  transition: color 0.15s, background 0.15s;
}

.nav-back-btn:hover {
  color: var(--color-dark);
  background: var(--color-light-gray);
}

.navbar-brand {
  font-family: var(--font-heading);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-dark);
  letter-spacing: -0.02em;
}

.navbar-center {
  flex: 1;
  max-width: 420px;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-shrink: 0;
}

/* Buttons */
.btn-text {
  background: none;
  color: var(--color-dark);
  font-weight: 500;
  padding: 0.4rem 0.75rem;
  border-radius: var(--radius);
  transition: background 0.15s;
}

.btn-text:hover {
  background: var(--color-light-gray);
}

.btn-primary {
  background: var(--color-accent-orange);
  color: #fff;
  padding: 0.5rem 1.25rem;
  border-radius: var(--radius);
  font-weight: 600;
  transition: opacity 0.15s;
}

.btn-primary:hover {
  opacity: 0.85;
}

.btn-sm {
  padding: 0.4rem 1rem;
  font-size: 0.85rem;
}

/* User area */
.navbar-user {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius);
}

.navbar-user:hover {
  background: var(--color-light-gray);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-mid-gray);
  color: var(--color-light);
  font-family: var(--font-heading);
  font-size: 0.8rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-name {
  font-family: var(--font-heading);
  font-size: 0.9rem;
  font-weight: 500;
}

.user-dropdown {
  display: none;
  position: absolute;
  top: 100%;
  right: 0;
  padding-top: 0.5rem;
  background: var(--color-light);
  border: 1px solid var(--color-light-gray);
  border-radius: var(--radius);
  margin-top: 0;
  min-width: 160px;
  box-shadow: 0 4px 12px rgba(20, 20, 19, 0.06);
}

.user-dropdown::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 0.5rem;
  background: transparent;
}

.navbar-user:hover .user-dropdown {
  display: block;
}

/* Keep the actual menu content below the bridge */
.user-dropdown > * {
  position: relative;
  z-index: 1;
}

.user-dropdown hr {
  border: none;
  border-top: 1px solid var(--color-light-gray);
  margin: 0.25rem 0;
  position: relative;
  z-index: 1;
}

.user-dropdown a,
.btn-logout {
  display: block;
  width: 100%;
  text-align: left;
  padding: 0.5rem 1rem;
  font-family: var(--font-heading);
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--color-dark);
  background: none;
  transition: background 0.1s;
}

.user-dropdown a:hover,
.btn-logout:hover {
  background: var(--color-light-gray);
}

.btn-logout {
  color: var(--color-accent-orange) !important;
}
</style>
