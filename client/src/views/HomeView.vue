<script setup>
import PictureWall from '@/components/PictureWall.vue';
import MainInfo from '@/components/MainInfo.vue';
import CameraIcon from 'vue-material-design-icons/Camera.vue'


</script>

<template>
  <MainInfo/>
  <PictureWall/>
  
  <div class="camera-navigator">
    <button class="camera-btn" @click="$router.push('/camera')">
      <CameraIcon class="icon" />
    </button>
  </div>
</template>

<style lang="css" scoped>
.camera-navigator {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100dvw;
  height: 90px;
  z-index: 10;
  display: flex;
  justify-content: center;
  align-items: flex-end;
  pointer-events: none;
}
.camera-navigator::before {
  content: "";
  position: absolute;
  left: 0; right: 0; bottom: 0; top: 0;
  background: linear-gradient(to top, rgba(30,30,30,0.85) 70%, rgba(30,30,30,0.0) 100%);
  z-index: 0;
  pointer-events: none;
}
.camera-btn {
  position: relative;
  z-index: 1;
  pointer-events: auto;
  background: linear-gradient(135deg, #ffb347 0%, #ffcc80 100%);
  border: none;
  border-radius: 50%;
  width: 64px;
  height: 64px;
  bottom: 10px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.15s;
  cursor: pointer;
}
.camera-btn:hover {
  transform: scale(1.08);
  box-shadow: 0 6px 32px rgba(0,0,0,0.35);
}
.icon {
  width: 32px;
  height: 32px;
  color: #333;
}
</style>