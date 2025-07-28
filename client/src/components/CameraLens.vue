<template>
  <div class="camera-container" :style="containerStyle">
    <video ref="video" autoplay playsinline :style="videoStyle"></video>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'

const video = ref(null)
const stream = ref(null)
const isCameraOn = ref(false)
const isFrontCamera = ref(false)
const orientation = ref(0)
const hasFlash = ref(false)
const videoTrack = ref(null)
const debug = ref(null)

const containerStyle = computed(() => ({
  transformOrigin: 'center center',
  width: orientation.value === 90 || orientation.value === 270 ? '100vh' : '100%',
  height: orientation.value === 90 || orientation.value === 270 ? '100vw' : '100%',
  position: 'fixed',
  top: '50%',
  left: '50%',
  transform: `translate(-50%, -50%) rotate(${orientation.value === 0 || orientation.value === 180 ? orientation.value : orientation.value - 180}deg)`
}))

const startCamera = async (useFrontCamera = false) => {
  try {
    stream.value = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: useFrontCamera ? 'user' : 'environment',
        width: { ideal: 3840 },
        height: { ideal: 2160 },
        frameRate: { ideal: 60 },
        aspectRatio: { ideal: 16 / 9 }
      }
    })
    video.value.srcObject = stream.value
    isCameraOn.value = true
    isFrontCamera.value = useFrontCamera

    // Check if device has flash
    videoTrack.value = stream.value.getVideoTracks()[0]
    const capabilities = videoTrack.value.getCapabilities()
    console.log('Camera capabilities:', capabilities)
    debug.value = capabilities
    hasFlash.value = capabilities.torch || false
  } catch (error) {
    console.error('Error accessing camera:', error)
  }
}

const handleOrientation = () => {
  orientation.value = screen.orientation?.angle || 0
}

const stopCamera = () => {
  if (stream.value) {
    stream.value.getTracks().forEach(track => track.stop())
    video.value.srcObject = null
    isCameraOn.value = false
  }
}

const flipCamera = async () => {
  stopCamera()
  await startCamera(!isFrontCamera.value)
}
 
const videoStyle = computed(() => ({
  transform: isFrontCamera.value ? 'scaleX(-1)' : 'none',
  width: '100%',
  height: '100%',
  objectFit: 'cover',
  backfaceVisibility: 'hidden',
}))

const handleVisibilityChange = () => {
  if (document.hidden) {
    stopCamera()
  } else {
    startCamera(isFrontCamera.value)
  }
}

const captureFrame = () => {
  const canvas = document.createElement('canvas')
  const videoElement = video.value
  if (!videoElement) return null

  canvas.width = videoElement.videoWidth
  canvas.height = videoElement.videoHeight
  const ctx = canvas.getContext('2d')
  
  if (isFrontCamera.value) {
    // Mirror for front camera
    ctx.translate(canvas.width, 0)
    ctx.scale(-1, 1)
  }

  ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height)
  return canvas.toDataURL('image/png') // base64 image
}

onMounted(() => {
  startCamera()
  window.addEventListener('orientationchange', handleOrientation)
  document.addEventListener('visibilitychange', handleVisibilityChange)
})

onUnmounted(() => {
  stopCamera()
  window.removeEventListener('orientationchange', handleOrientation)
  document.removeEventListener('visibilitychange', handleVisibilityChange)
})

const pausePreview = () => video.value?.pause()
const resumePreview = () => video.value?.play()

defineExpose({
  flipCamera,
  captureFrame,
  pausePreview,
  resumePreview
})
</script>

<style scoped>
.camera-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #000;
  overflow: hidden;
}

.button-container {
  position: absolute;
  bottom: 200px;
  z-index: 1000;
  display: flex;
  gap: 8px;
}
</style>