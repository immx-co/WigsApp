<template>
  <div id="app">
    <AppHeader :cart-count="cartCount" />
    <router-view />
  </div>
</template>

<script setup>
import { reactive, computed, provide, watch } from 'vue'
import AppHeader from '@/components/Header.vue'

const catalog = reactive({
  items: [
    {
      id: 'mug',
      title: "Парик 'Моднявый'",
      price: 799,
      image: 'https://lv2.pigugroup.eu/colours/259/954/66/25995466/pelnruskites-paruka-blondine-a6f16_large.jpg',
      description: 'Ебейший паричок, на каждый день.'
    },
    {
      id: 'tee',
      title: "Парик 'Четкий'",
      price: 1499,
      image: 'https://news.store.rambler.ru/img/1b8141721f502dc7a2a71841eea8739e?img-1-resize=width%3A1280%2Cheight%3A960%2Cfit%3Acover&img-format=auto',
      description: 'Подойдет для мужичков 40+ (сокращенно "скуфчик").'
    },
    {
      id: 'bag',
      title: "Парик 'Хайповый'",
      price: 3990,
      image: 'https://eclida.ru/storage/files/EKyP0iokLS.webp',
      description: 'Будешь самой модной на районе чиксой.'
    }
  ]
})
provide('catalog', catalog)

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
const cartCount = computed(() => state.items.reduce((s, i) => s + i.qty, 0))

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
