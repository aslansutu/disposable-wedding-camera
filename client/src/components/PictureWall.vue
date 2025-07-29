<template>
  <masonry-wall
    :items="items"
    :max-columns="6"
    :min-column-width="220"
    :min-columns="2"
    :gap="16"
  >
    <template #default="{ item, index }">
      <div
        class="image-container"
        @mouseenter="activeIndex = index"
        @mouseleave="activeIndex = null"
        @click="activeIndex = index"
        style="position: relative;"
      >
        <img :src="apiurl(item.url)" style="width: 100%; display: block;" />
        <span>{{ item.filename }}</span>
        <div
          v-if="activeIndex === index"
          class="overlay"
          @click.stop
        >
          <button class="download-btn" @click="downloadImage(item)">Download</button>
        </div>
      </div>
    </template>
  </masonry-wall>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { API_URL } from '../settings.js'

const apiurl = (path) => API_URL + path;
const items = ref([])
const activeIndex = ref(null)

onMounted(async () => {
  const res = await fetch(apiurl('/images/'))
  const data = await res.json()
  items.value = data
})

async function downloadImage(item) {
  const imageUrl = apiurl(item.url);
  const filename = item.filename;

  try {
    const response = await fetch(imageUrl, { mode: 'cors' }); // Make sure CORS is enabled on server
    const blob = await response.blob();
    const blobUrl = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = blobUrl;
    link.download = filename;

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // Revoke blob URL after download
    URL.revokeObjectURL(blobUrl);
  } catch (err) {
    console.error("Download failed:", err);
  }
}

</script>

<style lang="css" scoped>
.masonry-wall {
  width: 100%;
  margin: 0 auto;
}
.image-container {
  position: relative;
  cursor: pointer;
}
.overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
}
.download-btn {
  background: #7998c7;
  color: #eee;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.download-btn:hover {
  background: #eee;
  color:#7998c7
}
</style>