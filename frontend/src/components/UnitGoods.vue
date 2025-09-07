<template>
  <component :is="to ? 'router-link' : 'div'" :to="to" class="goods-card" :class="{ clickable: !!to }">
    <div class="thumb">
      <img :src="imageSrc" :alt="title" loading="lazy" />
    </div>
    <div class="body">
      <div class="title" :title="title">{{ title }}</div>
      <div class="price">{{ formattedPrice }}</div>
      <button class="add-btn" type="button" @click="handleAddToCart">В корзину</button>
      <slot />
    </div>
  </component>
</template>

<script>
import { inject } from 'vue'

export default {
  name: 'UnitGoods',
  props: {
    id: { type: [String, Number], default: null },
    title: { type: String, required: true },
    price: { type: [Number, String], required: true },
    image: { type: String, default: '' },
    /** Optional router target (string path or route object) */
    to: { type: [String, Object], default: null },
    /** Locale + currency ISO code are used for formatting */
    locale: { type: String, default: 'ru-RU' },
    currency: { type: String, default: 'RUB' }
  },
  setup(props) {
    const cart = inject('cart', null)
    function handleAddToCart() {
      if (!cart || !cart.addToCart) return
      cart.addToCart({ id: props.id, title: props.title, price: props.price, image: props.image }, 1)
    }
    return { cart, handleAddToCart }
  },
  computed: {
    formattedPrice() {
      const num = Number(this.price);
      if (Number.isFinite(num)) {
        try {
          return new Intl.NumberFormat(this.locale, { style: 'currency', currency: this.currency }).format(num);
        } catch (e) {
          // Fallback if currency code is invalid
          return new Intl.NumberFormat(this.locale).format(num) + ' ' + this.currency;
        }
      }
      return this.price;
    },
    imageSrc() {
      if (this.image) return this.image;
      // Lightweight SVG placeholder (gray box) as data URL
      const svg = encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400"><rect width="100%" height="100%" fill="#f2f2f2"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="#b3b3b3" font-family="Arial, Helvetica, sans-serif" font-size="20">Нет фото</text></svg>');
      return `data:image/svg+xml;charset=UTF-8,${svg}`;
    }
  }
}
</script>

<style scoped>
.goods-card {
  display: grid;
  grid-template-rows: auto 1fr;
  border: 1px solid #e6e6e6;
  border-radius: 12px;
  overflow: hidden;
  background: #fff;
  transition: transform .08s ease-in-out, box-shadow .15s ease-in-out, border-color .15s ease-in-out;
}

.goods-card.clickable {
  text-decoration: none;
  color: inherit;
  cursor: pointer;
}

.goods-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(0,0,0,.06);
  border-color: #dedede;
}

.thumb {
  width: 100%;
  aspect-ratio: 4 / 3;
  background: #fafafa;
  display: block;
  overflow: hidden;
}

.thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.body {
  padding: 12px;
  display: grid;
  gap: 8px;
}

.title {
  font-weight: 600;
  line-height: 1.25;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 2.5em;
}

.price {
  font-size: 1.1rem;
  font-weight: 700;
}

.add-btn {
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid #e2e2e2;
  background: #111827;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  transition: transform .05s ease-in-out, opacity .15s ease-in-out;
}
.add-btn:hover { transform: translateY(-1px); }
.add-btn:active { transform: translateY(0); opacity: .9; }
</style>
