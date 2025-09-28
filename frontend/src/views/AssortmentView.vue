<template>
  <section class="assortment">
    <div class="head">
      <h1>Ассортимент</h1>

      <div class="filters">
        <label class="lbl">
          Категория:
          <select v-model="selected" @change="applyFilter" class="select">
            <option value="">Все</option>
            <option v-for="c in categories" :key="c" :value="c">
              {{ c }}
            </option>
          </select>
        </label>
      </div>
    </div>

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
        :detailsRoute="{ name: 'product', params: { id: item.id } }"
      />
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
const apiUrl = (p) => `${API_BASE}${p}`

const goods = ref([])
const categories = ref([])          // список строк из enum Category
const selected = ref('')            // '' = Все
const loading = ref(false)
const error = ref('')

async function loadCategories() {
  const res = await axios.get(apiUrl('/goods/categories/full'), { withCredentials: true })
  categories.value = Array.isArray(res.data) ? res.data : []
}

async function loadAllGoods() {
  const res = await axios.get(apiUrl('/goods/all'), { withCredentials: true })
  goods.value = Array.isArray(res.data) ? res.data : []
}

async function loadByCategory(cat) {
  const res = await axios.get(apiUrl(`/goods/by_category/${encodeURIComponent(cat)}`), { withCredentials: true })
  goods.value = Array.isArray(res.data) ? res.data : []
}

async function applyFilter() {
  loading.value = true
  error.value = ''
  try {
    if (!selected.value) await loadAllGoods()
    else await loadByCategory(selected.value)
  } catch (e) {
    error.value = e?.response?.data?.detail || e?.message || 'Не удалось загрузить товары'
    goods.value = []
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  loading.value = true
  error.value = ''
  try {
    await loadCategories()
    await loadAllGoods() // по умолчанию показываем все
  } catch (e) {
    error.value = e?.response?.data?.detail || e?.message || 'Не удалось загрузить товары'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.assortment { max-width: 1100px; margin: 0 auto; padding: 16px; }
.head { display: flex; gap: 16px; align-items: center; justify-content: space-between; margin-bottom: 12px; flex-wrap: wrap; }
.filters { display: flex; gap: 12px; align-items: center; }
.lbl { display: inline-flex; gap: 8px; align-items: center; font-weight: 500; }
.select {
  padding: 8px 10px;
  border-radius: 10px;
  border: 1px solid #e2e2e2;
  background: #fff;
  min-width: 220px;
}
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
.muted { color: #666; }
.error { color: #b91c1c; }
</style>