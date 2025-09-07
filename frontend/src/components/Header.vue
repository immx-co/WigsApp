<template>
  <header class="site-header">
    <nav class="nav">
      <div class="left">
        <router-link class="btn primary" :to="{ name: 'home' }">Главная</router-link>
        <router-link class="btn primary" :to="{ name: 'assortment' }">Ассортимент</router-link>
      </div>
      <div class="right">
        <router-link class="btn" :to="{ name: 'cart' }">Корзина</router-link>
        <router-link class="btn" :to="{ name: 'account' }">Личный кабинет</router-link>
      </div>
    </nav>
  </header>
</template>

<script>
export default {
  name: 'AppHeader'
}
</script>

<style scoped>
.site-header {
  background: #ffffff;
  border-bottom: 1px solid #ececec;
}

.nav {
  max-width: 1100px;
  margin: 0 auto;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.left,
.right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn {
  text-decoration: none;
  padding: 8px 12px;
  border-radius: 10px;
  border: 1px solid #e2e2e2;
  transition: transform 0.05s ease-in-out, background-color 0.2s ease-in-out, border-color 0.2s ease-in-out;
  font-weight: 500;
}

.btn:hover {
  transform: translateY(-1px);
  background-color: #f8f8f8;
  border-color: #d8d8d8;
}

.primary {
  border-color: #3b82f6;
}

.primary:hover {
  background-color: #eff6ff;
  border-color: #2563eb;
}
</style>
