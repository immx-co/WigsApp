<template>
  <header class="site-header">
    <nav class="nav">
      <div class="left">
        <router-link class="logo" to="/">Главная</router-link>
        <router-link class="btn primary" :to="{ name: 'assortment' }">Ассортимент</router-link>
      </div>

      <div class="right">
        <router-link class="btn" :to="{ name: 'cart' }">
          Корзина
          <span v-if="cartCount && cartCount > 0" class="badge">{{ cartCount }}</span>
        </router-link>
        <router-link class="btn" :to="{ name: 'account' }">Личный кабинет</router-link>

        <!-- Кнопки авторизации -->
        <template v-if="isLogged">
          <button class="btn" type="button" @click="logout">Выйти</button>
        </template>
        <template v-else>
          <button class="btn solid" type="button" @click="openLogin">Войти</button>
          <button class="btn solid" type="button" @click="openRegister">Зарегистрироваться</button>
        </template>
      </div>
    </nav>
  </header>

  <!-- Login Modal -->
  <div v-if="loginOpen" class="overlay" @click.self="closeLogin" @keydown.esc="closeLogin" tabindex="-1">
    <div class="modal" role="dialog" aria-modal="true" aria-labelledby="login-title">
      <button class="close" aria-label="Закрыть" @click="closeLogin">×</button>
      <h2 id="login-title">Вход</h2>
      <form autocomplete="off" @submit.prevent="submitLogin">
        <label class="field">
          <span>Логин</span>
          <input
            ref="loginInput"
            v-model.trim="login"
            type="text"
            name="login"
            autocomplete="off"
            required
          />
        </label>
        <label class="field">
          <span>Пароль</span>
          <input
            v-model="password"
            type="password"
            name="pass"
            autocomplete="new-password"
            required
          />
        </label>
        <p v-if="error" class="error">{{ error }}</p>
        <div class="actions">
          <button type="button" class="btn" @click="closeLogin">Отмена</button>
          <button type="submit" class="btn solid">Войти</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Register Modal -->
  <div v-if="registerOpen" class="overlay" @click.self="closeRegister" @keydown.esc="closeRegister" tabindex="-1">
    <div class="modal" role="dialog" aria-modal="true" aria-labelledby="register-title">
      <button class="close" aria-label="Закрыть" @click="closeRegister">×</button>
      <h2 id="register-title">Регистрация</h2>
      <form autocomplete="off" @submit.prevent="submitRegister">
        <label class="field">
          <span>Логин</span>
          <input
            ref="registerLoginInput"
            v-model.trim="regLogin"
            type="text"
            name="login"
            autocomplete="off"
            required
          />
        </label>
        <label class="field">
          <span>Пароль</span>
          <input
            v-model="regPassword"
            type="password"
            name="pass"
            autocomplete="new-password"
            required
          />
        </label>
        <p v-if="regError" class="error">{{ regError }}</p>
        <div class="actions">
          <button type="button" class="btn" @click="closeRegister">Отмена</button>
          <button type="submit" class="btn solid">Зарегистрироваться</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Toast -->
  <div v-if="toast.show" class="toast" :class="toast.kind" role="status" aria-live="polite">
    {{ toast.text }}
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onBeforeUnmount, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router';

const router = useRouter()

function goHome() {
    try { router.push({ name: 'home' }) }
    catch { try { router.push('/') } catch {} }
}

defineProps({
  cartCount: { type: [Number, Object], default: 0 }
})

// API base URL (Vite / Vue CLI / fallback)
const API_BASE =
  (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_API_BASE) ||
  (typeof process !== 'undefined' && process.env && process.env.VUE_APP_API_BASE) ||
  'http://localhost:8000'
const apiUrl = (path) => `${API_BASE}${path}`

// ===== Текущий пользователь (через localStorage + событие) =====
const USER_KEY = 'current_user'
const currentUser = ref('default')
const isLogged = computed(() => !!currentUser.value && currentUser.value !== 'default')

function setCurrentUser(name) {
  try { localStorage.setItem(USER_KEY, name || 'default') } catch {}
  document.dispatchEvent(new CustomEvent('auth:user-changed', { detail: { username: name || 'default' } }))
  currentUser.value = name || 'default'
}
function loadCurrentUser() {
  try {
    const v = localStorage.getItem(USER_KEY)
    currentUser.value = v || 'default'
  } catch {
    currentUser.value = 'default'
  }
}
let userChangedHandler = null
onMounted(() => {
  loadCurrentUser()
  userChangedHandler = (e) => {
    currentUser.value = (e?.detail?.username) ?? 'default'
  }
  document.addEventListener('auth:user-changed', userChangedHandler)
})
onBeforeUnmount(() => {
  if (userChangedHandler) document.removeEventListener('auth:user-changed', userChangedHandler)
})

// ===== Login modal =====
const loginOpen = ref(false)
const login = ref('')
const password = ref('')
const error = ref('')
const loginInput = ref(null)

// ===== Register modal =====
const registerOpen = ref(false)
const regLogin = ref('')
const regPassword = ref('')
const regError = ref('')
const registerLoginInput = ref(null)

// ===== Toast =====
const toast = ref({ show: false, text: '', kind: 'info' })
let toastTimer = null
function showToast(text, kind='info', timeout=2500) {
  toast.value = { show: true, text, kind }
  if (toastTimer) clearTimeout(toastTimer)
  toastTimer = setTimeout(() => { toast.value.show = false }, timeout)
}

// ===== Modal handlers =====
function openLogin() {
  registerOpen.value = false
  error.value = ''
  loginOpen.value = true
  nextTick(() => loginInput.value && loginInput.value.focus())
}
function closeLogin() {
  loginOpen.value = false
  login.value = ''
  password.value = ''
  error.value = ''
}
function openRegister() {
  loginOpen.value = false
  regError.value = ''
  registerOpen.value = true
  nextTick(() => registerLoginInput.value && registerLoginInput.value.focus())
}
function closeRegister() {
  registerOpen.value = false
  regLogin.value = ''
  regPassword.value = ''
  regError.value = ''
}

// ===== Submit handlers =====
async function submitLogin() {
  try {
    if (!login.value || !password.value) {
      error.value = 'Введите логин и пароль'
      return
    }
    await axios.post(apiUrl('/person/verify'), {
      login: login.value,
      password: password.value
    }, {
      headers: { 'Content-Type': 'application/json' },
      withCredentials: true
    })
    showToast('Вход выполнен', 'success')
    setCurrentUser(login.value)
    closeLogin()
    goHome()
  } catch (e) {
    const status = e?.response?.status
    if (status === 404) {
      showToast('Пользователь не найден', 'warning')
      error.value = 'Пользователь не найден'
    } else if (status === 401) {
      showToast('Неверный пароль', 'error')
      error.value = 'Неверный пароль'
    } else {
      showToast('Ошибка подключения', 'error')
      error.value = e?.message || 'Ошибка входа'
    }
  }
}

async function submitRegister() {
  try {
    if (!regLogin.value || !regPassword.value) {
      regError.value = 'Введите логин и пароль'
      return
    }
    await axios.post(apiUrl('/person/add'), {
      login: regLogin.value,
      password: regPassword.value
    }, {
      headers: { 'Content-Type': 'application/json' },
      withCredentials: true
    })
    showToast('Регистрация успешна. Теперь войдите в аккаунт.', 'success')
    regLogin.value = ''
    regPassword.value = ''
    closeRegister()
    openLogin()
  } catch (e) {
    regError.value = (e?.response?.data?.detail) || e?.message || 'Ошибка регистрации'
    showToast(regError.value, 'error')
  }
}

async function logout() {
  const loginName = currentUser.value
  if (!loginName || loginName === 'default') {
    showToast('Сначала войдите', 'warning')
    return
  }
  try {
    await axios.post(apiUrl('/person/logout'), null, {
      params: { login: loginName },
      withCredentials: true
    })
    setCurrentUser('default')
    showToast('Вы вышли из аккаунта', 'success')
    goHome()
  } catch (e) {
    showToast(e?.response?.data?.detail || e?.message || 'Не удалось выйти', 'error')
  }
}
</script>

<style scoped>
.site-header { background: #ffffff; border-bottom: 1px solid #ececec; position: sticky; top: 0; z-index: 20; }
.nav { max-width: 1100px; margin: 0 auto; padding: 12px 16px; display: flex; align-items: center; justify-content: space-between; }
.left, .right { display: flex; align-items: center; gap: 12px; }
.logo { text-decoration: none; font-weight: 700; }
.btn { text-decoration: none; padding: 8px 12px; border-radius: 10px; border: 1px solid #e2e2e2; background: #fff; transition: .15s; font-weight: 500; cursor: pointer; }
.btn:hover { background-color: #f8f8f8; border-color: #d8d8d8; }
.btn.solid { background: #111827; color: #fff; border-color: #111827; }
.btn.solid:hover { opacity: .95; }
.primary { border-color: #3b82f6; }
.primary:hover { background-color: #eff6ff; border-color: #2563eb; }
.badge { display: inline-block; min-width: 20px; padding: 0 6px; margin-left: 6px; border-radius: 999px; background: #111827; color: #fff; font-size: 12px; line-height: 20px; text-align: center; }

/* Modal */
.overlay { position: fixed; inset: 0; background: rgba(0,0,0,.35); display: grid; place-items: center; padding: 16px; }
.modal { width: 100%; max-width: 420px; background: #fff; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,.15); padding: 20px; position: relative; }
.close { position: absolute; right: 10px; top: 10px; border: none; background: transparent; font-size: 22px; cursor: pointer; }
h2 { margin: 0 0 12px; }
.field { display: grid; gap: 6px; margin-bottom: 10px; }
.field input { padding: 10px 12px; border-radius: 10px; border: 1px solid #e2e2e2; }
.error { color: #b91c1c; margin: 6px 0; font-size: .95rem; }
.actions { display: flex; gap: 10px; justify-content: flex-end; margin-top: 10px; }

/* Toast */
.toast {
  position: fixed;
  right: 16px;
  bottom: 16px;
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid #e2e2e2;
  background: #fff;
  box-shadow: 0 8px 24px rgba(0,0,0,.12);
  z-index: 50;
  font-weight: 600;
}
.toast.success { border-color: #16a34a; color: #166534; background: #f0fdf4; }
.toast.error { border-color: #dc2626; color: #7f1d1d; background: #fef2f2; }
.toast.info { border-color: #2563eb; color: #1e3a8a; background: #eff6ff; }
.toast.warning { border-color: #f59e0b; color: #78350f; background: #fffbeb; }
</style>