<template>
    <div class="camera-container">
      <video ref="video" autoplay playsinline></video>
      <v-btn
        color="primary"
        class="mt-4"
        @click="toggleCamera"
      >
        {{ isCameraOn ? 'Turn Off Camera' : 'Turn On Camera' }}
      </v-btn>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue'
  
  const video = ref(null)
  const stream = ref(null)
  const isCameraOn = ref(false)
  
  const startCamera = async () => {
    try {
      stream.value = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: 'environment',
          width: { ideal: 3840 },
          height: { ideal: 2160 },
          frameRate: { ideal: 60 },
          aspectRatio: { ideal: 16/9 }
        }
      })
      video.value.srcObject = stream.value
      isCameraOn.value = true
    } catch (error) {
      console.error('Error accessing camera:', error)
    }
  }
  
  const stopCamera = () => {
    if (stream.value) {
      stream.value.getTracks().forEach(track => track.stop())
      video.value.srcObject = null
      isCameraOn.value = false
    }
  }
  
  const toggleCamera = () => {
    if (isCameraOn.value) {
      stopCamera()
    } else {
      startCamera()
    }
  }
  
  onUnmounted(() => {
    stopCamera()
  })

  onMounted(() => {
    startCamera()
  })
  </script>
  
  <style scoped>
  .camera-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    height: 100vh;
    background-color: #000;
  }
  
  video {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .v-btn {
    position: absolute;
    bottom: 20px;
    z-index: 1;
  }
  </style>