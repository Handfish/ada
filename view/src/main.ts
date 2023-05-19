import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import { createMetaManager } from 'vue-meta'
import LayoutDefault from '@/layouts/default.vue'
import VueFusionCharts from 'vue-fusioncharts'

// import FusionCharts modules and resolve dependency
import FusionCharts from 'fusioncharts'
import Charts from 'fusioncharts/fusioncharts.charts'
import FusionTheme from 'fusioncharts/themes/fusioncharts.theme.fusion'
import piniaPluginPersistedState from 'pinia-plugin-persistedstate'

import router from './router'

import './assets/main.css'

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedState)
app.use(pinia)
app.use(router)
// eslint-disable-next-line vue/component-definition-name-casing
app.component('layout-default', LayoutDefault)
app.use(createMetaManager())
app.use(VueFusionCharts, FusionCharts, Charts, FusionTheme)
app.mount('#app')
