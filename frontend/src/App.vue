<template>
  <div id="app">
    <AppHeader />
    <router-view />
  </div>
</template>

<script setup>
import { reactive, computed, provide, watch } from 'vue'
import AppHeader from '@/components/Header.vue'

const CART_KEY = 'cart_v1'

const state = reactive({
  items: (() => {
    try { return JSON.parse(localStorage.getItem(CART_KEY) || '[]') } catch { return [] }
  })()
})

watch(() => state.items, (val) => {
  try { localStorage.setItem(CART_KEY, JSON.stringify(val)) } catch {}
}, { deep: true })

function addToCart(product, qty = 1) {
  const id = product.id ?? (product.title + '|' + (product.image || ''))
  const price = Number(product.price)
  const normalized = {
    id,
    title: product.title,
    price: Number.isFinite(price) ? price : product.price,
    image: product.image || '',
  }
  const existing = state.items.find(i => i.id === id)
  if (existing) {
    existing.qty += qty
    if (existing.qty <= 0) {
      const idx = state.items.findIndex(i => i.id === id)
      if (idx !== -1) state.items.splice(idx, 1)
    }
  } else if (qty > 0) {
    state.items.push({ ...normalized, qty })
  }
}

function inc(id) {
  const item = state.items.find(i => i.id === id)
  if (item) item.qty += 1
}

function dec(id) {
  const item = state.items.find(i => i.id === id)
  if (!item) return
  item.qty -= 1
  if (item.qty <= 0) {
    const idx = state.items.findIndex(i => i.id === id)
    if (idx !== -1) state.items.splice(idx, 1)
  }
}

function setQty(id, qty) {
  qty = Math.max(0, Number(qty) || 0)
  const item = state.items.find(i => i.id === id)
  if (!item) return
  if (qty === 0) {
    const idx = state.items.findIndex(i => i.id === id)
    if (idx !== -1) state.items.splice(idx, 1)
  } else {
    item.qty = qty
  }
}

function removeFromCart(id) {
  const idx = state.items.findIndex(i => i.id === id)
  if (idx !== -1) state.items.splice(idx, 1)
}

function clearCart() {
  state.items.splice(0, state.items.length)
}

const total = computed(() => state.items.reduce((s, i) => s + (Number(i.price) || 0) * i.qty, 0))

provide('cart', {
  items: state.items,
  addToCart,
  removeFromCart,
  clearCart,
  inc,
  dec,
  setQty,
  total
})
</script>

<style>
#app { min-height: 100vh; }
</style>
