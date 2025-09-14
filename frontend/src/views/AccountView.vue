<template>
  <section class="account">
    <h1>Личный кабинет</h1>
    <p>Текущий пользователь: <strong>{{ username }}</strong></p>
  </section>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const USER_KEY = 'current_user'
const username = ref('unknown')

function loadUser() {
  try {
    const v = localStorage.getItem(USER_KEY)
    username.value = v || 'default'
  } catch {
    username.value = 'default'
  }
}

let handler = null
onMounted(() => {
  loadUser()
  handler = (e) => {
    username.value = (e?.detail?.username) ?? 'default'
  }
  document.addEventListener('auth:user-changed', handler)
})

onBeforeUnmount(() => {
  if (handler) document.removeEventListener('auth:user-changed', handler)
})
</script>

<style scoped>
.account { max-width: 900px; margin: 0 auto; padding: 16px; }
</style>
