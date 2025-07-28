<template>
  <masonry-wall
    :items="items"
    :max-columns="6"
    :min-column-width="220"
    :min-columns="2"
    :gap="16"
  >
    <template #default="{ item }">
      <div>
        <img :src="apiurl(item.url)" style="width: 100%; display: block;" />
        <span>{{ item.filename }}</span>
      </div>
    </template>
  </masonry-wall>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { API_URL } from '../settings.js'

const apiurl = (path) => API_URL + path;
const items = ref([])

onMounted(async () => {
  const res = await fetch(apiurl('/images/'))
  const data = await res.json()
  items.value = data
})
</script>

<style lang="css" scoped>
  .masonry-wall {
    width: 100%;
    margin: 0 auto;
  }
</style>