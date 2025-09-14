<template>
  <header class="site-header">
    <nav class="nav">
      <div class="left">
        <router-link class="logo" to="/">Главная</router-link>
        <router-link class="btn primary" :to="{ name: 'assortment' }">Ассортимент</router-link>
      </div>
      <div class="right">
        <router-link class="btn" :to="{ name: 'cart' }">
          Корзина
          <span v-if="cartCount && cartCount > 0" class="badge">{{ cartCount }}</span>
        </router-link>
        <router-link class="btn" :to="{ name: 'account' }">Личный кабинет</router-link>
      </div>
    </nav>
  </header>
</template>

<script setup>
defineProps({ cartCount: { type: [Number, Object], default: 0 } })
</script>

<style scoped>
.site-header { background: #ffffff; border-bottom: 1px solid #ececec; }
.nav { max-width: 1100px; margin: 0 auto; padding: 12px 16px; display: flex; align-items: center; justify-content: space-between; }
.left, .right { display: flex; align-items: center; gap: 12px; }
.logo { text-decoration: none; font-weight: 700; }
.btn { text-decoration: none; padding: 8px 12px; border-radius: 10px; border: 1px solid #e2e2e2; transition: .15s; font-weight: 500; position: relative; }
.btn:hover { background-color: #f8f8f8; border-color: #d8d8d8; }
.primary { border-color: #3b82f6; }
.primary:hover { background-color: #eff6ff; border-color: #2563eb; }
.badge { display: inline-block; min-width: 20px; padding: 0 6px; margin-left: 6px; border-radius: 999px; background: #111827; color: #fff; font-size: 12px; line-height: 20px; text-align: center; }
</style>
