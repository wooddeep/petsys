<template>
	<view class="container">
		<view class="ui-all">
			<form @submit="savaInfo">
				<view class="avatar" @tap="avatarChoose">
					<view class="imgAvatar"><view class="iavatar" :style="'background: url(' + avatarUrl + ') no-repeat center/cover #eeeeee;'"></view></view>
					<text v-if="avatarUrl">修改头像</text>
					<button v-if="!avatarUrl" open-type="getUserInfo" @getuserinfo="getUserInfo" class="getInfo"></button>
				</view>
				<view class="ui-list">
					<text>昵称</text>
					<input type="text" name="username" :placeholder="value" :value="foodBrand" placeholder-class="place" />
				</view>
				<view class="ui-list">
					<text>手机号</text>
					<input v-if="mobile" name="phone" type="tel" :placeholder="value" :value="mobile" placeholder-class="place" />
				</view>
				<view class="ui-list right">
					<text>性别</text>
					<picker name="sex" @change="bindPickerChange" mode="selector" range-key="name" :value="sexIndex" :range="sex">
						<view class="picker">{{ sex[sexIndex].name }}</view>
					</picker>
				</view>
				<view class="ui-list">
					<text>昵称</text>
					<input type="text" name="food_brand" :placeholder="value" :value="foodBrand" placeholder-class="place" />
				</view>
				<view class="ui-list">
					<text>绑定设备</text>
					<input type="tel" name="device" :placeholder="value" :value="deviceNumber" disabled placeholder-class="place" />
					<button  @tap="getDeviceNumber">扫一扫</button>
				</view>
				<view class="button-sp-area">
					<button class="save" form-type="submit">保存修改</button>
					<button class="logout" @tap="logout">退出登录</button>
				</view>
			</form>
		</view>
	</view>
</template>

<script>
import { mapState, mapMutations } from 'vuex';

export default {
	computed: {
		...mapState(['hasLogin', 'forcedLogin', 'avatarUrl', 'userName', 'mobile', 'sexIndex', 'userInfo'])
	},
	data() {
		return {
			value: '请填写',
			sex: [
				{
					id: 1,
					name: '男'
				},
				{
					id: 2,
					name: '女'
				}
			],
			description: '',
			url: '',
			headimg: '',
			deviceNumber: '',
			foodBrand: ''
		};
	},
	methods: {
		...mapMutations(['logout']),
		avatarChoose() {
			let that = this;
			uni.chooseImage({
				count: 1,
				sizeType: ['original', 'compressed'],
				sourceType: ['album', 'camera'],
				success(res) {
					// tempFilePath可以作为img标签的src属性显示图片
					that.imgUpload(res.tempFilePaths);
					const tempFilePaths = res.tempFilePaths;
				}
			});
		},
		imgUpload(file) {
			let that = this;
			uni.uploadFile({
				header: {
					Authorization: uni.getStorageSync('token')
				},
				url: that.websiteUrl + '/petsys/upload?openid=' + that.openId, //需传后台图片上传接口
				filePath: file[0],
				name: 'file',
				success: function(res) {
					var data = JSON.parse(res.data);
					//data = data.data;
					console.log(data);
					that.setAvatarUrl(that.websiteUrl + data.data.filename);
					console.log(that.avatarUrl);
				},
				fail: function(error) {
					console.log(error);
				}
			});
		},
		getDeviceNumber() {
			let that = this;
			// 允许从相机和相册扫码
			uni.scanCode({
			    success: function (res) {
			        console.log('条码类型：' + res.scanType);
			        console.log('条码内容：' + res.result);
					that.deviceNumber = res.result;
			    }
			});
		},
		savaInfo(e) {
			console.log(e.detail.value);
			uni.request({
				url: that.websiteUrl + '/petsys/user/modify',
				method: 'POST',
				data: {},
				success: (res) => {
					console.log(res);
				},
				fail: (err) => {
					console.error('网络连接失败：' + JSON.stringify(err));
					this.setUserInfo(JSON.stringify(err));
				}
				
			})
		}
	},
	onLoad() {
		console.log('onload =====');
		console.log(this.userInfo);
		this.foodBrand = this.userInfo;
	}
};
</script>

<style lang="less">
.container {
	display: block;
	width: 100%;
}

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

	.right:after {
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
		top: 40rpx;
		right: 0;
	}

	.save {
		background: #030303;
		border: none;
		color: #ffffff;
		margin-top: 40rpx;
		font-size: 28rpx;
	}
	
	.logout {
		background: #030303;
		border: none;
		color: #ffffff;
		margin-top: 40rpx;
		font-size: 28rpx;
	}
}
</style>
