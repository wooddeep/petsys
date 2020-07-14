<template>
	<view class="container" :style="'background: url(' + bg + ') no-repeat center/cover #eeeeee;'">
		<view class="button-area">
			<button  @tap="goIndex">开启精彩之旅</button>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				bg: '/../../static/pet/bg_loading.jpg',
				button_loading: '../../static/pet/button_loading.png'
			}
		},
		methods: {
			goIndex() {
				console.log('go to main!');
				uni.reLaunch({
					url: '../rank/rank'
				})
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
	background-color: #00c691; /* Green */
	border-radius: 8px;
	color: white;
	text-align: center;
	font-size: 10px;
	position: absolute;
	bottom: calc(100%/5);
	/* left: calc(100%/3); */
}
</style>
