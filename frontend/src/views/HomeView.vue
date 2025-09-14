<template>
  <section class="home">
    <div class="hero">
      <h1 class="brand">VOLOS.NET</h1>
      <p class="tagline">
        Магазин стильных париков и аксессуаров. Подчеркните образ — от повседневной
        классики до смелых трендов.
      </p>
      <router-link class="cta" :to="{ name: 'assortment' }">Смотреть ассортимент</router-link>
    </div>

    <div class="footlinks">
      <router-link class="tiny" :to="{ name: 'assortment' }">Ассортимент</router-link>
      <span class="dot">·</span>
      <router-link class="tiny" :to="{ name: 'assortment' }">Каталог</router-link>
      <span class="dot">·</span>
      <router-link class="tiny" :to="{ name: 'assortment' }">Все товары</router-link>
    </div>
  </section>
</template>

<script setup>
</script>

<style scoped>
.home {
  min-height: calc(100vh - 64px);
  display: grid;
  grid-template-rows: 1fr auto;
  padding: 24px 16px;
}
.hero {
  max-width: 900px;
  margin: 0 auto;
  display: grid;
  gap: 16px;
  align-content: center;
  justify-items: center;
  text-align: center;
}
.brand {
  font-size: clamp(36px, 7vw, 64px);
  font-weight: 900;
  letter-spacing: 1px;
}
.tagline {
  max-width: 680px;
  color: #4b5563;
  line-height: 1.6;
}
.cta {
  margin-top: 8px;
  padding: 10px 14px;
  border-radius: 12px;
  border: 1px solid #111827;
  background: #111827;
  color: #fff;
  text-decoration: none;
  font-weight: 600;
}
.cta:hover { opacity: .95; }

.footlinks {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 24px;
  color: #6b7280;
}
.tiny {
  font-size: 13px;
  color: #6b7280;
  text-decoration: underline;
}
.tiny:hover { color: #111827; }
.dot { color: #9ca3af; }
</style>
