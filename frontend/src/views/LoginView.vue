<template>
  <div class="login-box">
    <h2>Đăng nhập</h2>
    <input v-model="username" placeholder="Tên đăng nhập" />
    <input v-model="password" type="password" placeholder="Mật khẩu" />
    <button @click="login">Đăng nhập</button>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { API } from '@/config.js'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')

async function login() {
  if (!username.value || !password.value) {
    error.value = 'Nhập tên đăng nhập và mật khẩu'
    return
  }

  try {
    const res = await axios.post(API.LOGIN, {
      username: username.value,
      password: password.value
    })
    localStorage.setItem('user', res.data.user)
    router.push('/problems')
  } catch (err) {
    error.value = 'Sai tên đăng nhập hoặc mật khẩu'
  }
}
</script>

<style scoped>
.login-box {
  max-width: 400px;
  margin: 80px auto;
}
input {
  display: block;
  width: 100%;
  margin: 8px 0;
  padding: 6px;
}
button {
  padding: 8px 12px;
}
.error {
  color: red;
}
</style>
