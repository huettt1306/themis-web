<template>
  <div class="box" v-if="problemName">
    <h2>{{ problemName }}</h2>
    <a
      :href="`${API.PROBLEMS}/${encodeURIComponent(problemName)}`"
      target="_blank"
    >
      Tải file PDF
    </a>

    <hr />
    <h3>Nộp bài</h3>
    <input v-model="student" placeholder="Mã thí sinh" />
    <input type="file" @change="onFile" />
    <button @click="submit" :disabled="isSubmitting">Nộp</button>

    <div v-if="filename">Đã gửi: {{ filename }}</div>
    <pre v-if="log">{{ log }}</pre>
    <div v-if="isSubmitting">Đang nộp...</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { API, POLL_INTERVAL, POLL_RETRY } from '@/config.js'

const route = useRoute()

const problemName = decodeURIComponent(route.params.filename || '')
const student = ref(localStorage.getItem('user') || '')
const file = ref(null)
const filename = ref('')
const log = ref('')
const isSubmitting = ref(false)

function onFile(e) {
  file.value = e.target.files[0]
}

async function submit() {
  if (!student.value || !file.value) {
    alert('Nhập mã thí sinh và chọn file.')
    return
  }

  isSubmitting.value = true
  const form = new FormData()
  form.append('student', student.value)
  form.append('problem', problemName.replace(/\.pdf$/i, ''))
  form.append('file', file.value)

  try {
    const res = await axios.post(API.SUBMIT, form)
    filename.value = res.data.filename
    pollResult(filename.value)
  } catch (err) {
    alert('Lỗi nộp: ' + (err.response?.data?.detail || err.message))
    isSubmitting.value = false
  }
}

async function pollResult(name) {
  log.value = 'Chờ chấm...'
  for (let i = 0; i < POLL_RETRY; i++) {
    try {
      const r = await axios.get(`${API.RESULT}/${encodeURIComponent(name)}`)
      if (r.data.ready) {
        log.value = r.data.content
        isSubmitting.value = false
        return
      }
    } catch {
      // bỏ qua lỗi tạm thời
    }
    await new Promise((r) => setTimeout(r, POLL_INTERVAL))
  }
  log.value = 'Hết thời gian chờ. Chưa có log.'
  isSubmitting.value = false
}
</script>

<style scoped>
.box {
  max-width: 600px;
  margin: 20px auto;
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
pre {
  background: #f4f4f4;
  padding: 10px;
  white-space: pre-wrap;
}
</style>
