<template>
  <section class="assortment">
    <h1>Ассортимент</h1>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-else-if="loading" class="muted">Загрузка…</p>

    <div v-else class="grid">
      <UnitGoods
        v-for="item in goods"
        :key="item.id"
        :id="item.id"
        :title="item.title"
        :price="item.price"
        :image="item.image"
        :detailsRoute="{ name: 'product', params: { id: item.id } }" />
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import UnitGoods from '@/components/UnitGoods.vue'

const API_BASE =
  (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_API_BASE) ||
  (typeof process !== 'undefined' && process.env && process.env.VUE_APP_API_BASE) ||
  'http://localhost:8000'
const apiUrl = (path) => `${API_BASE}${path}`

const goods = ref([])
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  loading.value = true
  try {
    const res = await axios.get(apiUrl('/goods/all'), { withCredentials: true })
    goods.value = Array.isArray(res.data) ? res.data : []
  } catch (e) {
    error.value = e?.response?.data?.detail || e?.message || 'Не удалось загрузить товары'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.assortment { max-width: 1100px; margin: 0 auto; padding: 16px; }
h1 { margin-bottom: 16px; font-size: 1.5rem; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
.muted { color: #666; }
.error { color: #b91c1c; }
</style>
