<template>
  <div class="box">
    <section class="problems">
      <h3>Danh sách đề bài</h3>
      <ul v-if="problems.length">
        <li v-for="p in problems" :key="p">
          <a :href="`${BACKEND_URL}/problems/${encodeURIComponent(p)}`" target="_blank">{{ p }}</a>
        </li>
      </ul>
      <p v-else>Không có file PDF nào trong thư mục Downloads.</p>
    </section>

    <hr>

    <h2>Nộp bài</h2>

    <input v-model="student" placeholder="Mã thí sinh" />
    <input v-model="problem" placeholder="Tên bài thi" />
    <input type="file" @change="onFile" />
    <button @click="submit" :disabled="isSubmitting">Nộp</button>

    <div v-if="filename">Filename: {{ filename }}</div>
    <pre v-if="log">{{ log }}</pre>
    <div v-if="isSubmitting">Đang nộp...</div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// === Cấu hình backend ===
const BACKEND_URL = "http://192.168.1.26:8000" // đổi sang IP LAN nếu chạy mạng nội bộ

// === Biến lưu trạng thái ===
const problems = ref([])        // danh sách file PDF trong thư mục Downloads
const student = ref('')         // mã thí sinh
const problem = ref('')         // tên bài thi
const file = ref(null)          // file nộp
const filename = ref('')        // tên file gửi lên server
const log = ref('')             // kết quả chấm
const isSubmitting = ref(false) // trạng thái đang nộp bài

// === Khi component mount, tải danh sách PDF ===
onMounted(async () => {
  try {
    const { data } = await axios.get(`${BACKEND_URL}/problems`)
    problems.value = data.files
  } catch (err) {
    console.error("Lỗi tải danh sách đề bài:", err)
  }
})

// === Khi người dùng chọn file ===
function onFile(e) {
  file.value = e.target.files[0]
}

// === Khi người dùng chọn đề bài từ danh sách ===
function selectProblem(pdfName) {
  // bỏ phần .pdf để trùng với tên bài thi trong Themis
  problem.value = pdfName.replace(/\.pdf$/i, '')
}

// === Nộp bài ===
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
    const res = await axios.post(`${BACKEND_URL}/submit`, form)
    filename.value = res.data.filename
    pollResult(filename.value)
  } catch (err) {
    alert("Lỗi nộp: " + (err.response?.data?.detail || err.message))
    isSubmitting.value = false
  }
}

// === Kiểm tra kết quả chấm ===
async function pollResult(name) {
  log.value = "Chờ chấm..."
  for (let i = 0; i < 60; i++) { // Poll 2 phút
    try {
      const r = await axios.get(`${BACKEND_URL}/result/${encodeURIComponent(name)}`)
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
