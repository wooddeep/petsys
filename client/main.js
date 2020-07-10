import Vue from 'vue'
import App from './App'

import store from './store'

Vue.config.productionTip = false

Vue.prototype.$store = store

Vue.prototype.websiteUrl = 'http://192.168.141.171:8080';

App.mpType = 'app'

const app = new Vue({
	store,
	...App
})
app.$mount()
