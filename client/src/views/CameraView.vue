<template>
  <CameraLens ref="cameraLensRef"/>
  <div class="scanner"></div>
  <div class="action-buttons">
    <button class="shutter-button" @click="handleShutter">
      <CameraIcon class="icon" />
    </button>
    <button class="orbit-button" @click="handleFlipCamera">
      <OrbitVariant class="icon" />
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CameraLens from '../components/CameraLens.vue'
import CameraIcon from 'vue-material-design-icons/Camera.vue'
import OrbitVariant from 'vue-material-design-icons/OrbitVariant.vue'
import { API_URL } from '../settings.js'


const cameraLensRef = ref(null)
const apiurl = (path) => API_URL + path;


const handleFlipCamera = () => {
  cameraLensRef.value?.flipCamera()
}

const scanner = (status) => {
  const scannerElement = document.querySelector('.scanner')
  if (status) {
    scannerElement.style.display = 'block'
  } else {
    scannerElement.style.display = 'none'
  }
}

const handleShutter = async () => {
  cameraLensRef.value?.pausePreview()
  scanner(true)

  const imageDataUrl = cameraLensRef.value?.captureFrame()
  if (!imageDataUrl) return

  const blob = await (await fetch(imageDataUrl)).blob()
  const formData = new FormData()
  formData.append('file', blob, 'snapshot.png')

  const delay = new Promise(resolve => setTimeout(resolve, 2000)) // At least 2 seconds

  try {
    await Promise.all([
      fetch(apiurl('/upload'), {
        method: 'POST',
        body: formData,
      }),
      delay
    ])
    console.log('Image uploaded and delay complete')
  } catch (error) {
    console.error('Upload failed', error)
  }

  scanner(false)
  cameraLensRef.value?.resumePreview()

  // Todo: If adding text to fujifilm filter
  window.location.href = '/'
}

</script>

<style scoped>
.action-buttons {
  position: fixed;
  bottom: 5dvh;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  pointer-events: none; /* Optional: pass clicks through if needed */
}

.shutter-button,
.orbit-button {
  pointer-events: all;
  z-index: 1000;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transform: scale(1.5);
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 20px;
}

/* Position orbit-button to the far right */
.orbit-button {
  position: absolute;
  right: 5%;
  bottom: 0;
}

/* Icon size */
.icon {
  width: 24px;
  height: 24px;
}

.scanner {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 8px;
  background: linear-gradient(
    to bottom,
    rgba(0, 255, 255, 0.8),
    rgba(0, 255, 255, 0.1)
  );
  box-shadow: 0 0 12px rgba(0, 255, 255, 0.7),
              0 0 24px rgba(0, 255, 255, 0.5);
  z-index: 2;
  animation: scan 2s cubic-bezier(0.65, 0.05, 0.36, 1) infinite;
  display: none;
}

@keyframes scan {
  0% {
    transform: translateY(0%);
  }
  50% {
    transform: translateY(100vh); /* full screen height */
  }
  100% {
    transform: translateY(0%);
  }
}

</style>
