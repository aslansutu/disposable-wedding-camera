import './assets/main.css'
import '@mdi/font/css/materialdesignicons.css'


import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import MasonryWall from '@yeger/vue-masonry-wall'

const app = createApp(App)

app.use(router)
app.use(MasonryWall)

app.mount('#app')
