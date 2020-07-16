import { isJSON } from '@/common/checker.js';

// 异步请求获取low rank data
export function weixinLogin(that) {
	return new Promise((resolute, reject)=>{
		if (!that.hasLogin) {
			uni.login({
				provider: 'weixin',
				success: res => {
					console.log(res); //包含code
					
					uni.request({
						url: that.websiteUrl + '/petsys/openid/get',
						data: { jscode: res.code },
						method: 'POST',
						success: openId_res => {
							console.log('get openid!');
							console.log(openId_res);
							if (isJSON(openId_res.data.data)) {
								that.setOpenId(openId_res.data.data.openid);
								console.log(openId_res.data.data.openid);
								uni.request({
									url: that.websiteUrl + '/petsys/user/check',
									data: { openid: openId_res.data.data.openid },
									method: 'POST',
									success: res => {
										console.log(res);
										if (res.data.code == 1) {
											uni.navigateTo({
												url: '../reg/reg'
											});
										} else { //已经注册，返回首页 接口返回用户信息
											console.log(res.data.data[0]);
											that.setUserInfo(res.data[0]);
										}
										resolute('ok');
									},
									fail: (err) => {
										uni.showToast({
											icon: 'none',
											title: '网络连接失败'
										});
										console.error('网络连接失败：' + JSON.stringify(err));
										reject('network error!');
									}
								});
							} else {
								console.log('is not json string!');
								reject('reply body not json!');
							}
						},
						fail: (err) => {
							uni.showToast({
								icon: 'none',
								title: '网络连接失败'
							});
							console.error('网络连接失败：' + JSON.stringify(err));
							reject(err);
						}
					});
					uni.getUserInfo({
						provider: 'weixin',
						withCredentials: false,
						success: infoRes => {
							console.log(infoRes);
							that.login(infoRes.userInfo);
						},
						fail() {
							uni.showToast({
								icon: 'none',
								title: '登陆失败'
							});
						}
					});
				},
				fail: err => {
					console.error('授权登录失败：' + JSON.stringify(err));
				}
			});
		}
	})
}