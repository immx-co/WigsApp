<template>
  <section class="assortment">
    <h1>Ассортимент</h1>
    <div class="grid">
      <UnitGoods
        v-for="item in catalog.items"
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
import { inject } from 'vue'
import UnitGoods from '@/components/UnitGoods.vue'
const catalog = inject('catalog')
</script>

<style scoped>
.assortment { max-width: 1100px; margin: 0 auto; padding: 16px; }
h1 { margin-bottom: 16px; font-size: 1.5rem; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
</style>
