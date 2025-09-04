import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

// Import Tailwind CSS
import './assets/tailwind.css'

const app = createApp(App)

// Add Pinia for state management
app.use(createPinia())

// Add Vue Router
app.use(router)

app.mount('#app')