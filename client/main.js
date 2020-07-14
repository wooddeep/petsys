import Vue from 'vue'
import App from './App'

import store from './store'
// 注册全局组件
import MescrollBody from "@/components/mescroll-uni/mescroll-body.vue"
import MescrollUni from "@/components/mescroll-uni/mescroll-uni.vue"
Vue.component('mescroll-body', MescrollBody)
Vue.component('mescroll-uni', MescrollUni)

Vue.config.productionTip = false

Vue.prototype.$store = store

Vue.prototype.websiteUrl = 'http://192.168.141.171:8080';

App.mpType = 'app'

const app = new Vue({
	store,
	...App
})
app.$mount()
