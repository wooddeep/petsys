<template>
	<view>
		<view class="ui-all">
			<view class="ui-list"><button @tap="goToUserInfo">个人信息</button></view>
			<view class="uni-padding-wrap uni-common-mt"><button type="primary" @tap="mLogout">退出登录</button></view>
		</view>
	</view>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
export default {
	data() {
		return {};
	},
	methods: {
		...mapMutations(['logout']),
		mLogout() {
			this.logout();
			uni.reLaunch({
				url: '../main/main'
			});
		},
		goToUserInfo() {
			uni.navigateTo({
				url: '../user/user'
			});
		}
	}
};
</script>

<style lang="less">
.ui-all {
	padding: 20rpx 40rpx;

	.avatar {
		width: 100%;
		text-align: left;
		padding: 20rpx 0;
		border-bottom: solid 1px #f2f2f2;
		position: relative;

		.imgAvatar {
			width: 140rpx;
			height: 140rpx;
			border-radius: 50%;
			display: inline-block;
			vertical-align: middle;
			overflow: hidden;

			.iavatar {
				width: 100%;
				height: 100%;
				display: block;
			}
		}

		text {
			display: inline-block;
			vertical-align: middle;
			color: #8e8e93;
			font-size: 28rpx;
			margin-left: 40rpx;
		}

		&:after {
			content: ' ';
			width: 20rpx;
			height: 20rpx;
			border-top: solid 1px #030303;
			border-right: solid 1px #030303;
			transform: rotate(45deg);
			-ms-transform: rotate(45deg);
			/* IE 9 */
			-moz-transform: rotate(45deg);
			/* Firefox */
			-webkit-transform: rotate(45deg);
			/* Safari 和 Chrome */
			-o-transform: rotate(45deg);
			position: absolute;
			top: 85rpx;
			right: 0;
		}
	}
}

.ui-list {
	width: 100%;
	text-align: left;
	padding: 20rpx 0;
	border-bottom: solid 1px #f2f2f2;
	position: relative;

	text {
		color: #4a4a4a;
		font-size: 28rpx;
		display: inline-block;
		vertical-align: middle;
		min-width: 150rpx;
	}

	input {
		color: #030303;
		font-size: 30rpx;
		display: inline-block;
		vertical-align: middle;
	}
	button {
		color: #030303;
		font-size: 30rpx;
		display: inline-block;
		vertical-align: middle;
		background: none;
		margin: 0;
		padding: 0;
		&::after {
			display: none;
		}
	}
	picker {
		width: 90%;
		color: #030303;
		font-size: 30rpx;
		display: inline-block;
		vertical-align: middle;
		position: absolute;
		top: 30rpx;
		left: 150rpx;
	}

	textarea {
		color: #030303;
		font-size: 30rpx;
		vertical-align: middle;
		height: 150rpx;
		width: 100%;
		margin-top: 50rpx;
	}

	.place {
		color: #999999;
		font-size: 28rpx;
	}
}
</style>
