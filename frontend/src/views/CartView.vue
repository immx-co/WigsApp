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
      <div class="total">Итого: <strong>{{ formatPrice(cart.total) }}</strong></div>
      <button class="clear" @click="cart.clearCart()">Очистить корзину</button>
    </div>
  </section>
</template>

<script setup>
import { inject } from 'vue'
const cart = inject('cart')

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
</script>

<style scoped>
.cart { max-width: 900px; margin: 0 auto; padding: 16px; }
.list { list-style: none; padding: 0; margin: 0; display: grid; gap: 12px; }
.row {
  display: grid;
  grid-template-columns: 88px 1fr auto auto;
  gap: 12px;
  align-items: center;
  border: 1px solid #eee;
  border-radius: 10px;
  padding: 8px;
  background: #fff;
}
.thumb { width: 88px; height: 66px; object-fit: cover; border-radius: 8px; background: #f3f3f3; }
.info { display: grid; gap: 6px; }
.title { font-weight: 600; }
.meta { color: #555; display: flex; gap: 8px; }
.price { font-weight: 600; }
.qtybox { display: inline-flex; align-items: center; gap: 6px; }
.btn { width: 32px; height: 32px; border-radius: 8px; border: 1px solid #e2e2e2; background: #fff; cursor: pointer; }
.qty { width: 52px; height: 32px; padding: 0 6px; text-align: center; border: 1px solid #e2e2e2; border-radius: 8px; }
.remove, .clear {
  padding: 8px 12px;
  border-radius: 10px;
  border: 1px solid #e2e2e2;
  background: #fff;
  cursor: pointer;
}
.summary { display: flex; justify-content: space-between; align-items: center; margin-top: 16px; }
.total { font-size: 1.1rem; }
.empty { color: #666; margin-top: 8px; }
</style>
