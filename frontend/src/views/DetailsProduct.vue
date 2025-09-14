<template>
  <section v-if="loading" class="details">
    Загрузка…
  </section>

  <section v-else-if="error" class="notfound">
    {{ error }}
  </section>

  <section v-else-if="product" class="details">
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
import { inject, ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const API_BASE =
  (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_API_BASE) ||
  (typeof process !== 'undefined' && process.env && process.env.VUE_APP_API_BASE) ||
  'http://localhost:8000'
const apiUrl = (p) => `${API_BASE}${p}`

const cart = inject('cart', null)
const route = useRoute()
const id = computed(() => String(route.params.id ?? ''))

const product = ref(null)
const loading = ref(false)
const error = ref('')

async function fetchProduct() {
  loading.value = true
  error.value = ''
  product.value = null
  try {
    const res = await axios.get(apiUrl(`/goods/${encodeURIComponent(id.value)}`), {
      withCredentials: true,
      headers: { 'Accept': 'application/json' }
    })
    // Подстрахуемся по полям, чтобы не было исключений в шаблоне
    const raw = res.data || {}
    product.value = {
      id: raw.id ?? raw.goods_id ?? '',
      title: raw.title ?? '',
      price: raw.price ?? 0,
      image: raw.image ?? '',
      description: raw.description ?? '',
      category: raw.category ?? null,
    }
  } catch (e) {
    const s = e?.response?.status
    if (s === 404) error.value = 'Товар не найден'
    else error.value = e?.message || 'Ошибка загрузки товара'
  } finally {
    loading.value = false
  }
}

onMounted(fetchProduct)
// если переходишь между деталями, но компонент не размонтируется — перезагрузим данные
watch(id, () => { fetchProduct() })

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