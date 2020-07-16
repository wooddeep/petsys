<template>
	<view>
		<view :style="{'top':top}" class="download-tip">排行榜</view>
		
		<mescroll-body ref="mescrollRef" @init="mescrollInit" top="100" bottom="100" :down="downOption" @down="downCallback" @up="upCallback">		
			<!-- rank data -->
			<view class="rank-li" v-for="item in rankDataList" :key="news.id">
				<view>{{item.icon_path}}</view>
				<view>{{item.name}}  {{item.rate}}  {{item.device_id}}</view>
			</view>
		</mescroll-body>
	</view>
</template>

<script>
	import MescrollMixin from "@/components/mescroll-uni/mescroll-mixins.js";
	import {getCommonRankData, getLowRankData} from "@/api/rank.js"
	
	export default {
		mixins: [MescrollMixin], // 使用mixin (在main.js注册全局组件)
		
		data() {
			return {
				downOption:{
					auto:false,//是否在初始化完毕之后自动执行下拉回调callback; 默认true
				},
				rankDataList: [], // 数据列表
				top: 0 //提示,到顶部的距离
			}
		},
		methods: {
			/*下拉刷新的回调 */
			downCallback(){
				getCommonRankData(this, 1, 10).then(curPageData=>{
					console.log(curPageData);
					//联网成功的回调,隐藏下拉刷新和上拉加载的状态;
					this.mescroll.endSuccess(curPageData.length);
					
					//追加新数据
					this.rankDataList=this.rankDataList.concat(curPageData);
					console.log(this.rankDataList);
				}).catch(()=>{
					console.log('error req!');
					this.mescroll.endErr();
				});
			},
			/*上拉加载的回调: 其中page.num:当前页 从1开始, page.size:每页数据条数,默认10 */
			upCallback(page) {
				getLowRankData(this, page.num, page.size).then(curPageData=>{
					console.log(curPageData);
					if (curPageData.length > 0) {
						//联网成功的回调,隐藏下拉刷新和上拉加载的状态;
						this.mescroll.endSuccess(curPageData.length);
						
						//追加新数据
						this.rankDataList=this.rankDataList.concat(curPageData);
						console.log(this.rankDataList);
					} else {
						getCommonRankData(this, page.num, page.size).then(data=>{
							//联网成功的回调,隐藏下拉刷新和上拉加载的状态;
							this.mescroll.endSuccess(data.length);
							
							//追加新数据
							this.rankDataList=this.rankDataList.concat(data);
							console.log(this.data);
						})
					}
				}).catch(()=>{
					console.log('error req!');
					this.mescroll.endErr();
				});
			}
		}
	}
</script>

<style>
	image{width: 100%;vertical-align: bottom;height:auto}
	.header{z-index: 9900;position: fixed;top: --window-top;left: 0;height: 100upx;background: #fff;}
	.footer{z-index: 9900;position: fixed;bottom: 0;left: 0;height: 100upx;background: white;}
	
	.download-tip{
		z-index: 900;
		position: fixed;
		top: calc(var(--window-top) + 20upx);
		left: 0;
		width: 100%;
		height: 60upx;
		line-height: 60upx;
		font-size: 24upx;
		text-align: center;
		background-color: rgba(255,130,1,.7);
		color: white;
		-webkit-transition: top 300ms;
		transition: top 300ms;
	}
	
	/*展示上拉加载的数据列表*/
	.rank-li{
		padding: 32upx;
		border-bottom: 1upx solid #eee;
	}
</style>
