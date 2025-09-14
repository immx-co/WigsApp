<template>
  <section class="details" v-if="product">
    <div class="media">
      <img :src="product.image" :alt="product.title" />
    </div>
    <div class="info">
      <h1 class="title">{{ product.title }}</h1>
      <div class="price">{{ formatPrice(product.price) }}</div>
      <p class="desc">{{ product.description }}</p>
      <button class="buy" @click="add()">В корзину</button>
    </div>
  </section>
  <section v-else class="notfound">
    Товар не найден.
  </section>
</template>

<script setup>
import { inject, computed } from 'vue'
import { useRoute } from 'vue-router'

const catalog = inject('catalog')
const cart = inject('cart')
const route = useRoute()
const id = computed(() => route.params.id)

const product = computed(() => {
  return catalog?.items?.find?.(i => String(i.id) === String(id.value))
})

function formatPrice(v) {
  const num = Number(v)
  if (Number.isFinite(num)) {
    try { return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(num) }
    catch { return new Intl.NumberFormat('ru-RU').format(num) + ' ₽' }
  }
  return v
}

function add() {
  if (!product.value) return
  cart?.addToCart?.(product.value, 1)
}
</script>

<style scoped>
.details { max-width: 1100px; margin: 0 auto; padding: 16px; display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.media img { width: 100%; height: auto; border-radius: 12px; background: #fafafa; }
.info { display: grid; gap: 12px; align-content: start; }
.title { font-size: 1.75rem; font-weight: 700; }
.price { font-size: 1.2rem; font-weight: 700; }
.buy { padding: 12px 14px; border-radius: 12px; border: 1px solid #e2e2e2; background: #111827; color: #fff; font-weight: 600; cursor: pointer; }
.notfound { max-width: 1100px; margin: 0 auto; padding: 16px; }
@media (max-width: 900px) { .details { grid-template-columns: 1fr; } }
</style>
