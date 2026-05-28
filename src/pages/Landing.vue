<template>
  <div class="landing">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-inner container">
        <div class="hero-text">
          <h1 class="hero-title">
            Discover your<br /><span class="highlight">next great read</span>
          </h1>
          <p class="hero-subtitle">
            From an ocean of books, find the ones truly worth your time.
          </p>
          <p class="hero-tagline">
            Smart recommendations &middot; Authentic reviews &middot; Collection management &middot; Reader community
          </p>
          <div class="hero-actions">
            <button class="btn-hero-primary" @click="router.push('/home')">Start exploring</button>
            <button class="btn-hero-secondary" @click="scrollToFeatures">Learn more</button>
          </div>
        </div>
        <div class="hero-visual">
          <div class="hero-graphic">
            <div class="hero-book hero-book--1"></div>
            <div class="hero-book hero-book--2"></div>
            <div class="hero-book hero-book--3"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Feature Highlights -->
    <section id="features" ref="featuresRef" class="features">
      <div class="container">
        <div class="features-header">
          <h2 class="features-heading">Everything you need to read better</h2>
          <p class="features-subheading">
            Knowbooks combines intelligent technology with a thoughtful reading experience.
          </p>
        </div>
        <div class="features-grid">
          <div v-for="(feature, index) in mockFeatureHighlights" :key="index" class="feature-card">
            <div
              class="feature-icon"
              :style="{ background: feature.bgColor, color: feature.iconColor }"
            >
              <!-- Recommend icon -->
              <svg v-if="feature.iconKey === 'recommend'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
              </svg>
              <!-- Review icon -->
              <svg v-else-if="feature.iconKey === 'review'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
              </svg>
              <!-- Collection icon -->
              <svg v-else-if="feature.iconKey === 'collection'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z" />
              </svg>
              <!-- Community icon -->
              <svg v-else-if="feature.iconKey === 'community'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                <circle cx="9" cy="7" r="4" />
                <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                <path d="M16 3.13a4 4 0 0 1 0 7.75" />
              </svg>
            </div>
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-desc">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="landing-footer">
      <div class="container footer-inner">
        <span class="footer-brand">KnowBooks</span>
        <nav class="footer-links">
          <a href="#about">About</a>
          <a href="#privacy">Privacy Policy</a>
          <a href="#terms">Terms</a>
        </nav>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { mockFeatureHighlights } from '../data/mockData'

const router = useRouter()
const featuresRef = ref(null)

function scrollToFeatures() {
  featuresRef.value?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<style scoped>
/* ===== Hero ===== */
.hero {
  min-height: calc(100vh - 64px);
  display: flex;
  align-items: center;
  padding: 3rem 0;
  background: linear-gradient(180deg, var(--color-bg-secondary) 0%, var(--color-light) 100%);
}

.hero-inner {
  display: flex;
  align-items: center;
  gap: 4rem;
}

.hero-text {
  flex: 1;
}

.hero-title {
  font-family: var(--font-heading);
  font-size: 3rem;
  font-weight: 800;
  line-height: 1.15;
  color: var(--color-dark);
  letter-spacing: -0.03em;
  margin-bottom: 1.25rem;
}

.hero-title .highlight {
  color: var(--color-accent-orange);
  font-style: normal;
}

.hero-subtitle {
  font-size: 1.1rem;
  color: var(--color-dark);
  margin-bottom: 0.75rem;
  max-width: 460px;
}

.hero-tagline {
  font-size: 0.9rem;
  color: var(--color-mid-gray);
  margin-bottom: 2rem;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.btn-hero-primary {
  background: var(--color-accent-orange);
  color: #fff;
  font-family: var(--font-heading);
  font-size: 0.95rem;
  font-weight: 700;
  padding: 0.75rem 1.9rem;
  border-radius: var(--radius);
  transition: opacity 0.15s;
}

.btn-hero-primary:hover {
  opacity: 0.88;
}

.btn-hero-secondary {
  background: none;
  font-family: var(--font-heading);
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--color-dark);
  padding: 0.7rem 1.75rem;
  border: 1px solid var(--color-light-gray);
  border-radius: var(--radius);
  transition: border-color 0.15s, background 0.15s;
}

.btn-hero-secondary:hover {
  border-color: var(--color-mid-gray);
  background: var(--color-bg-secondary);
}

/* Hero visual */
.hero-visual {
  flex: 0 0 340px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-graphic {
  position: relative;
  width: 240px;
  height: 280px;
}

.hero-book {
  position: absolute;
  width: 140px;
  height: 190px;
  border-radius: 6px 12px 12px 6px;
  border: 2px solid var(--color-light-gray);
  background: var(--color-light);
}

.hero-book--1 {
  top: 0;
  left: 0;
  background: var(--color-dark);
  border-color: var(--color-dark);
  transform: rotate(-6deg);
}

.hero-book--2 {
  top: 20px;
  left: 55px;
  background: var(--color-accent-orange);
  border-color: var(--color-accent-orange);
  z-index: 1;
}

.hero-book--3 {
  top: 50px;
  left: 100px;
  background: var(--color-mid-gray);
  border-color: var(--color-mid-gray);
  transform: rotate(8deg);
  z-index: 2;
}

/* ===== Features ===== */
.features {
  padding: 5rem 0;
  background: var(--color-bg-secondary);
}

.features-header {
  text-align: center;
  margin-bottom: 4rem;
}

.features-heading {
  font-family: var(--font-heading);
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-dark);
  letter-spacing: -0.02em;
  margin-bottom: 0.75rem;
}

.features-subheading {
  font-size: 1rem;
  color: var(--color-mid-gray);
  max-width: 520px;
  margin: 0 auto;
  line-height: 1.6;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.feature-card {
  border: 1px solid var(--color-light-gray);
  border-radius: var(--radius-lg);
  padding: 2rem 1.5rem;
  background: #fff;
  text-align: left;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.feature-card:hover {
  border-color: transparent;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.feature-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  margin-bottom: 1.25rem;
}

.feature-title {
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-dark);
  margin-bottom: 0.5rem;
}

.feature-desc {
  font-size: 0.85rem;
  color: var(--color-mid-gray);
  line-height: 1.7;
}

/* ===== Footer ===== */
.landing-footer {
  border-top: 1px solid var(--color-light-gray);
  padding: 1.5rem 0;
}

.footer-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.footer-brand {
  font-family: var(--font-heading);
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--color-mid-gray);
}

.footer-links {
  display: flex;
  gap: 1.5rem;
}

.footer-links a {
  font-size: 0.8rem;
  color: var(--color-mid-gray);
  transition: color 0.15s;
}

.footer-links a:hover {
  color: var(--color-dark);
}

/* ===== Responsive ===== */
@media (max-width: 768px) {
  .hero-inner {
    flex-direction: column;
    gap: 2rem;
  }

  .hero-title {
    font-size: 2rem;
  }

  .hero-visual {
    flex: 0 0 auto;
  }

  .hero-graphic {
    width: 180px;
    height: 220px;
  }

  .hero-book {
    width: 110px;
    height: 150px;
  }

  .hero-book--2 { left: 40px; }
  .hero-book--3 { left: 75px; }

  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>
