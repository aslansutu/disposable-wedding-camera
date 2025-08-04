<template>
  <div class="main-info-container">
    <h2>
        {{ title }}
    </h2>
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
            title: 'Title',
            event_name: 'Event Name',
            description: 'Description of event',
            url: 'https://picsum.photos/200/300'
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