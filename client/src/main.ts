

import { createApp } from 'vue'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import { createPinia } from 'pinia'
import '@mdi/font/css/materialdesignicons.css'
import { aliases, mdi } from 'vuetify/iconsets/mdi-svg'

import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// i18n
import { createI18n } from 'vue-i18n'
import it from "./locales/it.json"
import en from "./locales/en.json"

import App from './App.vue'
import router from './router'


const vuetify = createVuetify({
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
  components,
  directives,
})

const i18n = createI18n({
  locale: navigator.language,
  fallbackLocale: "en",
  messages: {it, en},
  legacy: false
})

const app = createApp(App)
const pinia = createPinia()

console.log(navigator.language)

app.use(i18n).use(router).use(vuetify).use(pinia)

app.mount('#app')
