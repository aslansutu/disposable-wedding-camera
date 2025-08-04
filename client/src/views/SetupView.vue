<template>
  <form @submit.prevent="submitForm" class="setup-form">
    <label>
      Title:
      <input v-model="title" required />
    </label>
    <label>
      Event Name:
      <input v-model="event_name" required />
    </label>
    <label>
      Description:
      <textarea v-model="description" required />
    </label>
    <label>
      Event Image:
      <input type="file" accept="image/*" @change="onFileChange" required />
    </label>
    <button type="submit">Submit</button>
    <div v-if="success" class="success-msg">Event info saved!</div>
  </form>

  <section class="control-section">
    <h2>Controls</h2>
    <button @click="resetImages" :disabled="loading">Clear All Pictures</button>
    <input type="number" v-model.number="demoNum" min="1" style="width:60px;" />
    <button @click="getDemoImages" :disabled="loading || demoNum < 1">Get Demo Pictures</button>
    <div v-if="controlMsg" class="control-msg">{{ controlMsg }}</div>
  </section>
</template>

<script setup>
// This is a disposable camera application. Please take press the camera button to take a photo. All taken pictures will be uploaded to the server and will be available for everyone to see and download. Once you press the shutter button to take a picture, it will automatically be uploaded and cannot be deleted or cancelled.
import { ref } from 'vue'
import { API_URL } from '../settings.js'
import { useRouter } from 'vue-router'

const apiurl = (path) => API_URL + path;

const title = ref('')
const event_name = ref('')
const description = ref('')
const image = ref(null)
const success = ref(false)
const router = useRouter()
const loading = ref(false)
const demoNum = ref(5)
const controlMsg = ref('')

async function reset() {
  await fetch(apiurl('/reset'), {
    method: 'GET'
  })
}

function onFileChange(e) {
  image.value = e.target.files[0]
}

async function submitForm() {
  const formData = new FormData()
  formData.append('title', title.value)
  formData.append('event_name', event_name.value)
  formData.append('description', description.value)
  formData.append('image', image.value)
  const res = await fetch(apiurl('/info'), {
    method: 'POST',
    body: formData
  })
  if (res.ok) {
    success.value = true
    setTimeout(() => {
      router.push('/')
    }, 2000) // Redirect after 2 seconds
  }
}

async function resetImages() {
  loading.value = true
  controlMsg.value = ''
  try {
    const res = await fetch(apiurl('/reset'))
    if (res.ok) {
      controlMsg.value = 'All pictures cleared!'
    } else {
      controlMsg.value = 'Failed to clear pictures.'
    }
  } finally {
    loading.value = false
  }
}

async function getDemoImages() {
  loading.value = true
  controlMsg.value = ''
  try {
    const res = await fetch(apiurl(`/demo/${demoNum.value}`))
    if (res.ok) {
      controlMsg.value = `Fetched ${demoNum.value} demo pictures!`
    } else {
      controlMsg.value = 'Failed to fetch demo pictures.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.setup-form {
  max-width: 420px;
  margin: 40px auto;
  padding: 2rem 2rem 1.5rem 2rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.04);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.setup-form label {
  font-size: 1rem;
  color: #222;
  margin-bottom: 6px;
  font-weight: 500;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.setup-form input,
.setup-form textarea {
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 10px 12px;
  font-size: 1rem;
  background: #f8f9fa;
  transition: border-color 0.2s;
  outline: none;
}

.setup-form input:focus,
.setup-form textarea:focus {
  border-color: #7998c7;
  background: #fff;
}

.setup-form button[type="submit"] {
  background: #7998c7;
  color: #fff;
  border: none;
  padding: 12px 0;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(0,0,0,0.07);
  transition: background 0.2s;
}

.setup-form button[type="submit"]:hover {
  background: #4e6fae;
}

.success-msg {
  color: #2ecc40;
  margin-top: 10px;
  font-weight: 500;
  text-align: center;
}

button {
  background: #e0e4ea;
  color: #222;
  border: none;
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  margin-top: 18px;
  transition: background 0.2s;
}

button:hover {
  background: #7998c7;
  color: #fff;
}

.control-section {
  margin: 40px auto;
  max-width: 420px;
  padding: 1.5rem 2rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.04);
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.control-section h2 {
  font-size: 1.2rem;
  color: #222;
  margin-bottom: 8px;
  font-weight: 600;
}

.control-section button {
  margin-right: 10px;
  margin-top: 0;
}

.control-section input[type="number"] {
  width: 80px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 8px 10px;
  font-size: 1rem;
  background: #f8f9fa;
  margin-right: 10px;
}

.control-msg {
  margin-top: 10px;
  color: #4e6fae;
  font-weight: 500;
  text-align: center;
}
</style>