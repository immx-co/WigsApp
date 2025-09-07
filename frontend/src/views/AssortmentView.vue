<template>
  <section class="assortment">
    <h1>Ассортимент</h1>
    <div class="grid">
      <UnitGoods
        title="Парик 'Чёткий'"
        :price="799"
        image="https://news.store.rambler.ru/img/1b8141721f502dc7a2a71841eea8739e?img-1-resize=width%3A1280%2Cheight%3A960%2Cfit%3Acover&img-format=auto" />

      <UnitGoods
        title="Парик 'Хайповый'"
        :price="1499"
        image="https://eclida.ru/storage/files/EKyP0iokLS.webp" />

      <UnitGoods
        title="Парик 'Моднявый'"
        :price="3990"
        image="https://lv2.pigugroup.eu/colours/259/954/66/25995466/pelnruskites-paruka-blondine-a6f16_large.jpg" />
    </div>
  </section>
</template>

<script>
import UnitGoods from '@/components/UnitGoods.vue'

export default {
  name: 'AssortmentView',
  components: { UnitGoods }
}
</script>

<style scoped>
.assortment {
  max-width: 1100px;
  margin: 0 auto;
  padding: 16px;
}

h1 {
  margin-bottom: 16px;
  font-size: 1.5rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}
</style>
