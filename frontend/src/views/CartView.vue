<template>
  <section class="cart">
    <h1>Корзина</h1>

    <div v-if="!cart.items.length" class="empty">
      В корзине пока пусто.
    </div>

    <ul v-else class="list">
      <li v-for="item in cart.items" :key="item.id" class="row">
        <img v-if="item.image" :src="item.image" :alt="item.title" class="thumb" />
        <div class="info">
          <div class="title">{{ item.title }}</div>
          <div class="meta">
            <span class="price">{{ formatPrice(item.price) }}</span>
          </div>
        </div>
        <div class="qtybox">
          <button class="btn" @click="cart.dec(item.id)" aria-label="Уменьшить">−</button>
          <input class="qty" type="number" min="1" :value="item.qty" @input="onInputQty($event, item)" />
          <button class="btn" @click="cart.inc(item.id)" aria-label="Увеличить">+</button>
        </div>
        <button class="remove" @click="cart.removeFromCart(item.id)">Убрать</button>
      </li>
    </ul>

    <div v-if="cart.items.length" class="summary">
      <div class="total">Итого: <strong>{{ formatPrice(total) }}</strong></div>
      <div class="actions">
        <button class="primary" :disabled="placing" @click="placeOrder">
          {{ placing ? 'Оформляем…' : 'Оформить заказ' }}
        </button>
        <button class="clear" @click="cart.clearCart()">Очистить корзину</button>
      </div>
    </div>

    <p v-if="notice" class="notice">{{ notice }}</p>
  </section>
</template>

<script setup>
import axios from 'axios'
import { inject, computed, ref } from 'vue'
const cart = inject('cart')

const API_BASE = (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_API_BASE) || (typeof process !== 'undefined' && process.env && process.env.VUE_APP_API_BASE) || 'http://localhost:8000'
const apiUrl = (p) => `${API_BASE}${p}`

const total = computed(() => cart?.total?.value ?? 0)
const placing = ref(false)
const notice = ref('')

const formatPrice = (v) => {
  const num = Number(v)
  if (Number.isFinite(num)) {
    try { return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(num) }
    catch { return new Intl.NumberFormat('ru-RU').format(num) + ' ₽' }
  }
  return v
}

function onInputQty(e, item) {
  const val = Math.max(1, Number(e.target.value) || 1)
  cart.setQty(item.id, val)
}

async function placeOrder() {
  if (!cart.items.length) return
  placing.value = true
  notice.value = ''
  try {
    const items = cart.items.map(i => ({ id: String(i.id), qty: Number(i.qty) || 1 }))
    const res = await axios.post(apiUrl('/order/place'), { items }, { withCredentials: true })
    cart.clearCart()
    const total = res?.data?.total
    notice.value = typeof total !== 'undefined'
      ? `Заказ оформлен! Сумма: ${formatPrice(total)}`
      : 'Заказ оформлен!'
  } catch (e) {
    notice.value = e?.response?.data?.detail || e?.message || 'Не удалось оформить заказ'
  } finally {
    placing.value = false
  }
}
</script>

<style scoped>
.cart { max-width: 900px; margin: 0 auto; padding: 16px; }
.list { list-style: none; padding: 0; margin: 0; display: grid; gap: 12px; }
.row { display: grid; grid-template-columns: 88px 1fr auto auto; gap: 12px; align-items: center; border: 1px solid #eee; border-radius: 10px; padding: 8px; background: #fff; }
.thumb { width: 88px; height: 66px; object-fit: cover; border-radius: 8px; background: #f3f3f3; }
.info { display: grid; gap: 6px; }
.title { font-weight: 600; }
.meta { color: #555; display: flex; gap: 8px; }
.price { font-weight: 600; }
.qtybox { display: inline-flex; align-items: center; gap: 6px; }
.btn { width: 32px; height: 32px; border-radius: 8px; border: 1px solid #e2e2e2; background: #fff; cursor: pointer; }
.qty { width: 52px; height: 32px; padding: 0 6px; text-align: center; border: 1px solid #e2e2e2; border-radius: 8px; }
.remove, .clear { padding: 8px 12px; border-radius: 10px; border: 1px solid #e2e2e2; background: #fff; cursor: pointer; }
.summary { display: flex; justify-content: space-between; align-items: center; margin-top: 16px; gap: 12px; flex-wrap: wrap; }
.total { font-size: 1.1rem; }
.actions { display: flex; gap: 10px; }
.primary {
  padding: 8px 12px;
  border-radius: 10px;
  border: 1px solid #111827;
  background: #111827;
  color: #fff;
  cursor: pointer;
}
.primary[disabled] { opacity: .7; cursor: default; }
.empty { color: #666; margin-top: 8px; }
.notice { margin-top: 12px; color: #166534; background: #f0fdf4; border: 1px solid #86efac; padding: 8px 10px; border-radius: 10px; }
</style>
