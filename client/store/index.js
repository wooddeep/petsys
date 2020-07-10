import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
	state: {
		/**
		 * 是否需要强制登录
		 */
		forcedLogin: true,
		hasLogin: false,
		openId: '',
		
		userInfo: '',
		userName: "",
		avatarUrl: "",
		mobile: "10086",
		sexIndex: 0
	},
	mutations: {
		login(state, userInfo) {
			state.userName = userInfo.nickName || '新用户';
			state.hasLogin = true;
			state.avatarUrl = userInfo.avatarUrl;
			state.sexIndex = userInfo.gender;
		},
		logout(state) {
			state.userName = "";
			state.hasLogin = false;
		},
		setUserInfo(state, info) {
			state.userInfo = info;
		},
		setOpenId(state, id) {
			state.openId = id;
		},
		setSex(state, sex) {
			state.sexIndex = sex;
		},
		setAvatarUrl(state, url) {
			state.avatarUrl = url;
		}
	}
})

export default store
