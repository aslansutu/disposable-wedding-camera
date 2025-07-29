<template>
  <div class="main-info-container">
    <h2>
        {{ title }}
    </h2>
    <h2>for</h2>
    <h1>
        {{ event_name }}
    </h1>
    <img :src="url" alt="Event Image" style="width: auto; height: auto; max-height: 40dvh; display: block; margin-bottom: 16px;" />
    <p>
        {{ description }}
    </p>
  </div>
</template>

<script>
import { API_URL } from '../settings.js'

const apiurl = (path) => API_URL + path;

export default {
    name: 'MainInfo',
    data() {
        return {
            title: 'Disposable Camera',
            event_name: 'Hanife & Atakan\'s Wedding',
            description: 'This is a disposable camera application. Please take press the camera button to take a photo. All taken pictures will be uploaded to the server and will be available for everyone to see and download. Once you press the shutter button to take a picture, it will automatically be uploaded and cannot be deleted or cancelled.',
            url: 'https://www.sample-videos.com/img/Sample-png-image-500kb.png'
        }
    },
    async mounted() {
        try {
            const res = await fetch(apiurl('/info'))
            if (res.ok) {
                const info = await res.json()
                this.title = info.title
                this.event_name = info.event_name
                this.description = info.description
                this.url = apiurl(info.image)
            }
        } catch (e) {
            // ignore if not found
            console.log(e, 'Defaulting to premade values')
        }
    },
    methods: {

    }
}
</script>

<style scoped>
.main-info-container {
    max-width: 60dvw;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}
h1, h2, img {
    text-align: center;
}
</style>