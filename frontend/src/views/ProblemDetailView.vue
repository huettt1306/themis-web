<template>
  <div class="container" v-if="problemName">
    <!-- Cột trái: PDF -->
    <div class="left">
      <vue-pdf-embed
        :source="`${API.PROBLEMS}/${encodeURIComponent(problemName)}`"
        class="pdf-view"
      />
    </div>

    <!-- Cột phải: Form nộp bài -->
    <div class="right">
      <h3>Nộp bài</h3>

      <p><strong>Mã thí sinh:</strong> {{ student }}</p>

      <input type="file" @change="onFile" />
      <button @click="submit" :disabled="isSubmitting">Nộp</button>

      <pre v-if="log">{{ log }}</pre>
      <div v-if="isSubmitting">Đang nộp...</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import VuePdfEmbed from 'vue-pdf-embed'
import { API, POLL_INTERVAL, POLL_RETRY } from '@/config.js'

const route = useRoute()

const problemName = decodeURIComponent(route.params.filename || '')
const student = ref(localStorage.getItem('user') || 'Chưa đăng nhập')
const file = ref(null)
const filename = ref('')
const log = ref('')
const isSubmitting = ref(false)

function onFile(e) {
  file.value = e.target.files[0]
}

async function submit() {
  if (!file.value) {
    alert('Hãy chọn file cần nộp.')
    return
  }
  if (student.value === 'Chưa đăng nhập') {
    alert('Bạn chưa đăng nhập.')
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
    } catch {}
    await new Promise((r) => setTimeout(r, POLL_INTERVAL))
  }
  log.value = 'Hết thời gian chờ. Chưa có log.'
  isSubmitting.value = false
}
</script>

<script>
export default {
  components: { VuePdfEmbed }
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 20px;
  margin: 20px;
}

/* PDF bên trái */
.left {
  flex: 7;
  display: flex;              /* bật flex cho cột trái */
  justify-content: center;    /* căn giữa ngang */
  align-items: flex-start;    /* đầu trên (có thể đổi thành center nếu muốn giữa dọc) */
}

/* Form bên phải */
.right {
  flex: 3;
  border: 1px solid #ccc;
  padding: 15px;
  border-radius: 6px;
  background: #fafafa;
  height: fit-content;
}

.pdf-view {
  width: 96%;
  height: 90vh;
  border: 1px solid #ccc;
}

input[type="file"] {
  display: block;
  width: 100%;
  margin: 8px 0;
  padding: 6px;
}

button {
  padding: 8px 12px;
  width: 100%;
}

pre {
  background: #f4f4f4;
  padding: 10px;
  white-space: pre-wrap;
  max-height: 300px;
  overflow-y: auto;
}
</style>
