<template>
  <div class="box">
    <h2>Nộp bài</h2>
    <input v-model="student" placeholder="Mã thí sinh" />
    <input v-model="problem" placeholder="Tên bài" />
    <input type="file" @change="onFile" />
    <button @click="submit" :disabled="isSubmitting">Nộp</button>

    <div v-if="filename">Filename: {{ filename }}</div>
    <pre v-if="log">{{ log }}</pre>
    <div v-if="isSubmitting">Đang nộp...</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const student = ref('')
const problem = ref('')
const file = ref(null)
const filename = ref('')
const log = ref('')
const isSubmitting = ref(false)

function onFile(e) {
  file.value = e.target.files[0]
}

async function submit() {
  if (!student.value || !problem.value || !file.value) {
    alert("Nhập mã thí sinh, tên bài và chọn file")
    return
  }
  isSubmitting.value = true
  const form = new FormData()
  form.append('student', student.value)
  form.append('problem', problem.value)
  form.append('file', file.value)
  try {
    const res = await axios.post('http://localhost:8000/submit', form)
    filename.value = res.data.filename
    pollResult(filename.value)
  } catch (err) {
    alert("Lỗi nộp: " + (err.response?.data?.detail || err.message))
    isSubmitting.value = false
  }
}

async function pollResult(name) {
  log.value = "Chờ chấm..."
  for (let i = 0; i < 60; i++) { // poll tối đa 60 lần (~2 phút)
    try {
      const r = await axios.get(`http://localhost:8000/result/${encodeURIComponent(name)}`)
      if (r.data.ready) {
        log.value = r.data.content
        isSubmitting.value = false
        return
      }
    } catch (err) {
      console.error(err)
    }
    await new Promise(r => setTimeout(r, 2000))
  }
  log.value = "Hết thời gian chờ. Chưa có log."
  isSubmitting.value = false
}
</script>

<style scoped>
.box { max-width:600px; margin:20px auto; }
input { display:block; margin:8px 0; width:100%; padding:6px; }
button { padding:8px 12px; }
pre { background:#f4f4f4; padding:10px; white-space:pre-wrap; }
</style>
