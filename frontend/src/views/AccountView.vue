<template>
  <section class="account">
    <h1>Личный кабинет</h1>

    <div v-if="loading" class="muted">Загрузка…</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <template v-else>
      <div class="userbox">
        <div>Пользователь: <strong>{{ userLogin || 'default' }}</strong></div>
        <button v-if="userLogin" class="btn" @click="refresh">Обновить</button>
      </div>

      <div v-if="orders.length === 0" class="muted">Заказов пока нет.</div>

      <ul v-else class="orders">
        <li v-for="(order, idx) in orders" :key="idx" class="order">
          <div class="order-head">
            <div class="order-title">Заказ #{{ idx + 1 }}</div>
            <div class="order-total">Итого: <strong>{{ formatPrice(order.total) }}</strong></div>
          </div>
          <ul class="items">
            <li v-for="(it, i) in order.items" :key="i" class="item">
              <div class="title">{{ it.title }}</div>
              <div class="qty">× {{ it.quantity ?? it.qty }}</div>
              <div class="line">{{ formatPrice(it.line_total) }}</div>
            </li>
          </ul>
        </li>
      </ul>
    </template>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_BASE =
  (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_API_BASE) ||
  (typeof process !== 'undefined' && process.env && process.env.VUE_APP_API_BASE) ||
  'http://localhost:8000'
const apiUrl = (p) => `${API_BASE}${p}`

const userLogin = ref('')
const orders = ref([])
const loading = ref(false)
const error = ref('')

function formatPrice(v) {
  const num = Number(v)
  if (Number.isFinite(num)) {
    try { return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(num) }
    catch { return new Intl.NumberFormat('ru-RU').format(num) + ' ₽' }
  }
  return v
}

async function loadActiveUser() {
  const res = await axios.get(apiUrl('/person/active'), { withCredentials: true })
  userLogin.value = res.data || ''
  return userLogin.value
}

async function loadOrders(login) {
  const res = await axios.get(apiUrl(`/order/${encodeURIComponent(login)}`), { withCredentials: true })
  orders.value = Array.isArray(res.data) ? res.data : []
}

async function refresh() {
  loading.value = true
  error.value = ''
  try {
    const login = await loadActiveUser()
    if (login) {
      await loadOrders(login)
    } else {
      orders.value = []
    }
  } catch (e) {
    error.value = e?.response?.data?.detail || e?.message || 'Не удалось загрузить данные'
    orders.value = []
  } finally {
    loading.value = false
  }
}

onMounted(refresh)
</script>

<style scoped>
.account { max-width: 900px; margin: 0 auto; padding: 16px; }
h1 { margin-bottom: 12px; }
.muted { color: #6b7280; }
.error { color: #b91c1c; }
.userbox { display: flex; align-items: center; gap: 12px; margin: 8px 0 16px; }
.btn { padding: 6px 10px; border-radius: 10px; border: 1px solid #e2e2e2; background: #fff; cursor: pointer; }
.orders { list-style: none; padding: 0; margin: 0; display: grid; gap: 14px; }
.order { border: 1px solid #eee; border-radius: 12px; padding: 12px; background: #fff; }
.order-head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px; }
.order-title { font-weight: 700; }
.order-total { font-weight: 600; }
.items { list-style: none; padding: 0; margin: 0; display: grid; gap: 8px; }
.item { display: grid; grid-template-columns: 1fr auto auto; gap: 8px; align-items: center; }
.item .title { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.item .qty { color: #6b7280; }
.item .line { font-weight: 600; }
</style>