<template>
    <CameraLens />
    <button>
        CLICK
    </button>
</template>

<script setup>
import CameraLens from '../components/CameraLens.vue'
</script>

<style scoped>
button {
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 1000;
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
</style>