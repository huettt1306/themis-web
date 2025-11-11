<template>
  <div class="box">
    <h2>Danh sách đề thi</h2>
    <p>Xin chào, {{ user }}</p>

    <ul v-if="problems.length">
      <li v-for="p in problems" :key="p">
        <router-link :to="`/problems/${encodeURIComponent(p.replace(/\.pdf$/i, ''))}`">
          {{ p }}
        </router-link>
      </li>
    </ul>

    <p v-else>Không có file PDF nào trong thư mục Downloads.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { API } from '@/config.js'

const problems = ref([])
const user = localStorage.getItem('user') || 'Khách'

onMounted(async () => {
  try {
    const { data } = await axios.get(API.PROBLEMS)
    problems.value = data.files
  } catch (err) {
    console.error('Lỗi tải danh sách đề thi:', err)
  }
})
</script>

<style scoped>
.box {
  max-width: 600px;
  margin: 20px auto;
}
li {
  margin: 6px 0;
}
</style>
    