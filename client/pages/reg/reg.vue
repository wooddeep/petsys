<template>
	<view>
		<view class="uni-padding-wrap uni-common-mt">
			<form @submit="formSubmit" @reset="formReset">
				<view class="avatar" @tap="avatarChoose">
					<view class="imgAvatar"><view class="iavatar" :style="'background: url(' + avatarUrl + ') no-repeat center/cover #eeeeee;'"></view></view>
					<text v-if="avatarUrl">修改头像</text>
				</view>
				<view class="uni-form-item uni-row">
					<view class="title">姓名</view>
					<input class="uni-input" name="username" placeholder="请输入姓名" />
				</view>
				<view class="uni-form-item uni-row">
					<view class="title">性别</view>
					<radio-group name="sex" class="uni-input">
						<label>
							<radio value="male" /><text>男</text>
						</label>
						<label>
							<radio value="female" /><text>女</text>
						</label>
					</radio-group>
				</view>
				<view class="uni-form-item uni-row">
					<view class="title">食物品牌</view>
					<input class="uni-input" name="food_brand" placeholder="请输入食物品牌" />
				</view>
				<view class="uni-form-item uni-row">
					<view class="title">联系电话</view>
					<input class="uni-input" name="phone" placeholder="请输入电话" />
				</view>
				<view class="uni-form-item uni-row">
					<view class="title">验证码</view>
					<input class="uni-input" name="vcode" placeholder="验证码" />
					<view class="verifyCode" @tap="changeCode"><image :mode="aspectFill" :src="avatarUrl" @error="imageError"> </image></view>
				</view>
				<view class="button-sp-area">
					<button form-type="submit">提交</button>
					<button type="default" form-type="reset">重置</button>
				</view>
			</form>
		</view>
	</view>
</template>
<script>
	import { mapState, mapMutations } from 'vuex';
	var  graceChecker = require("../../common/graceChecker.js");
	export default {
		computed: mapState(['avatarUrl', 'openId']),
		data() {
			return {
				
			}
		},
		methods: {
			...mapMutations(['setAvatarUrl']),
			formSubmit: function(e) {
				let that = this;
				console.log('form发生了submit事件，携带数据为：' + JSON.stringify(e.detail.value))
                //定义表单规则
                var rule = [
                    {name:"username", checkType : "string", checkRule:"1,3",  errorMsg:"姓名应为1-3个字符"}, //rule 拼接处正则字符串进行匹配
                    {name:"sex", checkType : "in", checkRule:"male,female",  errorMsg:"请选择性别"}/* ,
                    {name:"vcode", checkType : "int", checkRule:"",  errorMsg:"请输入正确的验证码"} */
                ];
                //进行表单检查
                var formData = e.detail.value;
                var checkRes = graceChecker.check(formData, rule);
                if(checkRes){
                    uni.showToast({title:"验证通过!", icon:"none"});
					formData.openid = that.openId;
					formData.icon_path = that.avatarUrl;
					console.log(formData);
					uni.request({
						url: 'http://192.168.147.112:8080/petsys/user/add',
						method: 'POST',
						data: formData,
						success: (res) => {
							console.log(res);
							uni.reLaunch({
								url: '../main/main'
							})
						}
					})
                }else{
                    uni.showToast({ title: graceChecker.error, icon: "none" });
                }
			},
			formReset: function(e) {
				console.log('清空数据')
			},
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
					url: 'http://192.168.147.112:8080/petsys/upload?openid=' + that.openId, //需传后台图片上传接口
					filePath: file[0],
					name: 'file',
					success: function(res) {
						var data = JSON.parse(res.data);
						//data = data.data;
						console.log(data);
						that.setAvatarUrl('http://192.168.147.112:8080' + data.data.filename);
						console.log(that.avatarUrl);
					},
					fail: function(error) {
						console.log(error);
					}
				});
			},
			changeCode() {
				console.log('change code!');
			}
		}
	}
</script>

<style>
	.uni-form-item .title {
		padding: 20rpx 0;
	}
	button {
	    margin-top: 30rpx;
	    margin-bottom: 30rpx;
	}
	
	.uni-form-item .verifyCode {
		padding: 20rpx 0;
	}
	
	image {
		width: 80px; 
		height: 20px; 
		background-color: #FFFFFF; 
		text-align: left;
		padding: 0rpx 20rpx;
	}
	
	.avatar {
		width: 100%;
		text-align: left;
		padding: 20rpx 0;
		border-bottom: solid 1px #f2f2f2;
		position: relative;
	}
	
	.avatar	.imgAvatar {
		width: 140rpx;
		height: 140rpx;
		border-radius: 50%;
		display: inline-block;
		vertical-align: middle;
		overflow: hidden;
	}
	.avatar	.iavatar {
		width: 100%;
		height: 100%;
		display: block;
	}
	
	.avatar	text {
		display: inline-block;
		vertical-align: middle;
		color: #8e8e93;
		font-size: 28rpx;
		margin-left: 40rpx;
	}
	
	.avatar::after {
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
</style>
