<template>
  <CameraLens />
  <div class="action-buttons">
    <button class="shutter-button">
      <CameraIcon class="icon" />
    </button>
    <button class="orbit-button">
      <OrbitVariant class="icon" />
    </button>
  </div>
</template>

<script setup>
import CameraLens from '../components/CameraLens.vue'
import CameraIcon from 'vue-material-design-icons/Camera.vue'
import OrbitVariant from 'vue-material-design-icons/OrbitVariant.vue'
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
</style>
