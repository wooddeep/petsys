<template>
	<view class="container" :style="'background: url(' + bg + ') no-repeat center/cover #eeeeee;'">
		<!-- logo图标 -->
		<view class="loading_logo">
			<image src="../../static/pet/logo.png"></image>
		</view>
		<!-- 小圆点 -->
		<view class="dian">
			<text class="dian_first"></text>
			<text></text>
			<text></text>
		</view>
		<view class="button-area">
			<button  @tap="goIndex">开启精彩之旅</button>
		</view>
	</view>
</template>

<script>
	import { weixinLogin } from '@/api/login.js'
	import { mapState, mapMutations } from 'vuex';
	
	var _self;
	
	export default {
		computed: {
			...mapState(['openId'])
		},
		data() {
			return {
				bg: '/../../static/pet/bg_loading.jpg',
				button_loading: '../../static/pet/button_loading.png'
			}
		},
		onLoad() {
			_self = this;
			weixinLogin(_self).then( err => {
				console.log("登录失败！");
			});
		},
		methods: {
			...mapMutations(['login', 'setUserInfo', 'setOpenId']),
			goIndex() {
				if (!_self.openId) {
					uni.showToast({
						icon: 'none',
						title: '正在登录'
					});
				} else {
					console.log('go to main!');
					console.log(_self.openId);
					uni.reLaunch({
						url: '../main/main'
					})
				}
			}
		}
	}
</script>

<style>
.container {
	width: 100%;
	height: 100%;
}
.button-area {
	width: 200rpx;
	margin:0 auto;
}
.button-area button {
	background-color: #4fcbbe; /* Green */
	width: 234rpx;
	height: 77rpx;
	line-height: 77rpx;
	border-radius: 8px;
	color: white;
	text-align: center;
	font-size: 14px;
	position: absolute;
	bottom: calc(100%/5);
	/* left: calc(100%/3); */
}
/* 图标 */
.loading_logo{
	margin: 230rpx auto;
	text-align: center;
	width: 100%;
	height: 400rpx;
	/* border: 1px solid red; */
}
.loading_logo image{
	width: 391rpx;
	height: 407rpx;
}
/* 小圆点 */
.dian{
	width: 100%;
	height: 80rpx;
	/* border: 1px solid red; */
	margin: -80rpx auto;
	text-align: center;
}
.dian text{
	display: inline-block;
	width: 14rpx;
	height: 14rpx;
	background-color: white;
	border-radius: 50%;
    margin: 0 4rpx;
}
.dian_first{
	width: 40rpx !important;
	height: 16rpx !important;
	background-color:#4fcbbe !important;
	border-radius: 9rpx 9rpx !important;
}
</style>
