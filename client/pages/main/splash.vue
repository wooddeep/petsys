<template>
	<view class="uni-margin-wrap">
		<swiper class="swiper" acceleration="true" :autoplay="autoplay"   :interval="interval" :duration="duration">
			<swiper-item  class="swiper-item">
				<image class="swiper-img" :src="bg" mode="aspectFill"></image>
			</swiper-item>
		</swiper>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				background: ['color1', 'color2', 'color3'],
				indicatorDots: true,
				autoplay: false,
				interval: 2000,
				duration: 500,
				bg: '/../../static/pet/bg_loading.jpg'
			}
		},
		methods: {
			
		}
	}
</script>

<style>
	.uni-margin-wrap {
		width: 100%;
	}
	.swiper {
		width: 100%;
		height: 100%;
	}
	.swiper-item {
		display: block;
		height: 100%;
		line-height: 300rpx;
		text-align: center;
	}
	.swiper-img{
		width: 100%;
		height: 100%;
	}
</style>
