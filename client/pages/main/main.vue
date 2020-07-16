<template>
	<view>
		<view v-if="hasLogin" class="hello">
			<uni-section title="基础卡片" type="line"></uni-section>
			<view class="main-body">
				<view v-for="item in list" :key="item.id" class="card-box">
					<uni-card :title="item.title" :is-shadow="item.shadow" :note="item.note" :extra="item.extra" :thumbnail="item.thumbnail" @click="clickCard">
						<text class="content-box-text">{{ item.content }}</text>
					</uni-card>
				</view>
			</view>
		</view>
		<view v-if="!hasLogin" class="hello">
			<view class="title">您好 游客。</view>
			<view class="ul">
				<view>这是 uni-app 带登录模板的示例App首页。</view>
				<view>在 “我的” 中点击 “登录” 可以 “登录您的账户”</view>
			</view>
		</view>
	</view>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
import uniCard from '@/components/uni-card/uni-card.vue';
import { isJSON } from '@/common/checker.js';
import { weixinLogin } from '@/api/login.js'

export default {
	components: {
		uniCard
	},
	computed: mapState(['forcedLogin', 'hasLogin', 'avatarUrl']),
	data() {
		return {
			list: [
				{
					id: 0,
					title: '标题文字',
					content: '这是一个完整配置的基础卡片示例。内容样式可自定义。',
					shadow: true,
					note: 'Tips',
					extra: '额外信息',
					thumbnail: 'https://img-cdn-qiniu.dcloud.net.cn/new-page/uni.png'
				}
			],
			Tips: ['喜欢', '评论', '分享']
		};
	},
	methods: {
		...mapMutations(['login', 'setOpenId', 'setUserInfo']),
		clickCard() {
			if (!this.hasLogin){
				uni.showToast({
					title: '未登录',
					icon: 'none'
				});
				weixinLogin(this);
			}
			uni.navigateTo({
				url: '../user/petInfo'
			});
		}
	},
	onLoad() {
		if (!this.hasLogin) {
			// 未登录
			console.log('not login!');
			weixinLogin(this);
		}
	}
};
</script>

<style>
.hello {
	display: flex;
	flex: 1;
	flex-direction: column;
}

.title {
	color: #8f8f94;
	margin-top: 25px;
}

.ul {
	font-size: 15px;
	color: #8f8f94;
	margin-top: 25px;
}

.ul > view {
	line-height: 25px;
}

.main-body {
	flex-direction: row;
	flex-wrap: wrap;
	justify-content: center;
	padding: 0;
	font-size: 14rpx;
	background-color: #ffffff;
}

.main-body {
	flex-direction: column;
	padding: 30rpx;
	background-color: #ffffff;
}

.main-body {
	padding: 20rpx 0;
	padding-bottom: 0;
}

.card-box {
	/* margin-bottom: 30rpx;
	*/
}

.content-box-text {
	font-size: 30rpx;
}
</style>
