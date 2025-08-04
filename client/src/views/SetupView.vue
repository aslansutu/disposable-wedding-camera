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
  <button @click="reset">Reset</button>
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
</script>

<style scoped>
.setup-form {
  max-width: 400px;
  margin: 40px auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.success-msg {
  color: green;
  margin-top: 10px;
}
</style>