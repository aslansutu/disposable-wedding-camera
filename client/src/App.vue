<template>
  <v-app>
    <v-main>
      <CameraView />
    </v-main>
  </v-app>
</template>

<script setup>
import CameraView from './components/CameraView.vue'
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  overflow: hidden;
}
</style>