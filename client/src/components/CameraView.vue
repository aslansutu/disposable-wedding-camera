<template>
  <div class="camera-container" :style="containerStyle">
    <video ref="video" autoplay playsinline></video>
    <div class="button-container" :style="buttonStyle">
      <v-btn color="primary" class="mr-2" @click="toggleCamera">
        {{ isCameraOn ? 'Turn Off Camera' : 'Turn On Camera' }}
      </v-btn>
      <v-btn v-if="isCameraOn" color="secondary" @click="flipCamera">
        <v-icon>{{ isFrontCamera ? 'mdi-camera-rear' : 'mdi-camera-front' }}</v-icon>
      </v-btn>
      <div>{{ orientation }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'

const video = ref(null)
const stream = ref(null)
const isCameraOn = ref(false)
const isFrontCamera = ref(false)
const orientation = ref(0)

const containerStyle = computed(() => ({
  transformOrigin: 'center center',
  width: orientation.value === 90 || orientation.value === 270 ? '100vh' : '100%',
  height: orientation.value === 90 || orientation.value === 270 ? '100vw' : '100%',
  position: 'fixed',
  top: '50%',
  left: '50%',
  transform: `translate(-50%, -50%) rotate(${orientation.value === 0 || orientation.value === 180 ? orientation.value : orientation.value - 180}deg)`
}))

const buttonStyle = computed(() => ({
  transform: `rotate(${orientation.value}deg)`,
  transformOrigin: 'center center'
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

const toggleCamera = () => {
  if (isCameraOn.value) {
    stopCamera()
  } else {
    startCamera(isFrontCamera.value)
  }
}

const flipCamera = async () => {
  stopCamera()
  await startCamera(!isFrontCamera.value)
}

onMounted(() => {
  startCamera()
  window.addEventListener('orientationchange', handleOrientation)
})

onUnmounted(() => {
  stopCamera()
  window.removeEventListener('orientationchange', handleOrientation)
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

video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  backface-visibility: hidden;
}

.button-container {
  position: absolute;
  bottom: 200px;
  z-index: 1000;
  display: flex;
  gap: 8px;
}
</style>