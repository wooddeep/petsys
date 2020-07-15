<template>
	<view class="qiun-columns" :style="'background: url(' + bg + ') no-repeat center/cover #eeeeee;'">
		<!-- 1.头像 昵称 -->
		<view class="top_self">
			<!-- 用户头像 -->
			<view class="both useAvatar" :style="'background: url(' + avatarUrl + ') no-repeat center/cover #eeeeee;'" ></view>
			<!-- 用户昵称性别 -->
			<view class="both sex"><image src="../../static/pet/female.png"></image></view>
			<view class="both nickName">
				<text>哦卡哇伊阔多</text>
				<text>Natural Balance</text>
			</view>
			<view class="both fork"><image src="../../static/pet/close.png"></image></view>
		</view>
		<!-- 2.肉 -->
		<view class="meat">
			<image src="../../static/pet/meat1.png" class="meatwai"></image>
			<image src="../../static/pet/meat.png" class="meatnei"></image>
		</view>
		<!-- 3.图表 -->
		
		<view class="charts-container">
			<!-- <image src="/../../static/pet/bg_zhu.png"></image> -->
			<view class=".charts-container-2">
				<view class="charts-item">
					<view class="charts-item-title">
						<text class="yuan"></text>
						喂食信息表
						<button class="seeMore">查看更多</button>
					</view>
					<canvas canvas-id="canvasColumn" id="canvasColumn" class="charts" @touchstart="touchColumn"></canvas>
				</view>
				
				<!-- <view class=" qiun-title-bar qiun-common-mt">
					
				</view> -->
				<view class="charts-item">
					<view class="charts-item-title qiun-common-mt">
						<text class="yuan"></text>
						饮食情况
						<button class="seeMore">查看更多</button>
					</view>
					<canvas canvas-id="canvasLine" id="canvasLine" class="charts" @touchstart="touchLine" @touchmove="moveLine" @touchend="touchEndLine"></canvas>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
import uCharts from '@/components/u-charts/u-charts.js';
import { isJSON } from '@/common/checker.js';
import { mapState } from 'vuex';
import { getFoodTend } from '@/api/foodTend.js'

var _self;
var canvaColumn = null;
var canvasLine = null;
var lastMoveTime = null; //最后执行移动的时间戳
export default {
	computed: {
		...mapState(['openId', 'avatarUrl'])
	},
	data() {
		return {
			cWidth: '',
			cHeight: '',
			pixelRatio: 1,
			bg: '/../../static/pet/bg_petinfo.png',
			seximg: '/../../static/pet/female.png',
			meat: '/../../static/pet/meat1.png'
		};
	},
	onLoad() {
		_self = this;
		const { windowWidth, windowHeight } = uni.getSystemInfoSync();
		this.cWidth = windowWidth * 0.9;
		this.cHeight = windowHeight * 0.21;
		this.getServerData();
	},
	methods: {
		getServerData() {
			getFoodTend(_self);
		},
		showColumn(canvasId, chartData) {
			canvaColumn = new uCharts({
				$this: _self,
				canvasId: canvasId,
				type: 'column',
				padding: [15, 5, 0, 15],
				legend: {
					show: false,
					padding: 5,
					lineHeight: 11,
					margin: 0
				},
				fontSize: 11,
				background: '#FFFFFF',
				pixelRatio: _self.pixelRatio,
				animation: true,
				categories: chartData.categories,
				series: chartData.series,
				xAxis: {
					disableGrid: true
				},
				yAxis: {
					data: [
						{
							position: 'left',
							axisLine: false,
							format: val => {
								return val.toFixed(0) + 'g';
							}
						}
					]
				},
				dataLabel: false,
				width: _self.cWidth * _self.pixelRatio,
				height: _self.cHeight * _self.pixelRatio,
				extra: {
					column: {
						type: 'group',
						width: (_self.cWidth * _self.pixelRatio * 0.45) / chartData.categories.length
					}
				}
			});
		},
		touchColumn(e) {
			canvaColumn.showToolTip(e, {
				format: function(item, category) {
					if (typeof item.data === 'object') {
						return category + ' ' + item.name + ':' + item.data.value;
					} else {
						return category + ' ' + item.name + ':' + item.data;
					}
				}
			});
			canvaColumn.touchLegend(e, { animation: true });
		},
		showLine(canvasId, chartData) {
			canvasLine = new uCharts({
				$this: _self,
				canvasId: canvasId,
				type: 'line',
				colors: ['#facc14', '#f04864', '#8543e0', '#90ed7d'],
				fontSize: 11,
				padding: [15, 15, 0, 15],
				legend: {
					show: false,
					padding: 5,
					lineHeight: 11,
					margin: 0
				},
				dataLabel: false,
				dataPointShape: true,
				background: '#FFFFFF',
				pixelRatio: _self.pixelRatio,
				categories: chartData.categories,
				series: chartData.series,
				animation: true,
				xAxis: {
					type: 'grid',
					gridColor: '#CCCCCC',
					gridType: 'dash',
					dashLength: 8
					//disableGrid:true
				},
				yAxis: {
					gridType: 'dash',
					gridColor: '#CCCCCC',
					dashLength: 8
				},
				width: _self.cWidth * _self.pixelRatio,
				height: _self.cHeight * _self.pixelRatio,
				extra: {
					line: {
						type: 'straight'
					}
				}
			});
		},
		touchLine(e) {
			lastMoveTime = Date.now();
		},
		moveLine(e) {
			let currMoveTime = Date.now();
			let duration = currMoveTime - lastMoveTime;
			if (duration < Math.floor(1000 / 60)) return; //每秒60帧
			lastMoveTime = currMoveTime;

			let currIndex = canvasLine.getCurrentDataIndex(e);
			if (currIndex > -1 && currIndex < canvasLine.opts.categories.length) {
				let riqi = canvasLine.opts.categories[currIndex];
				let leibie = canvasLine.opts.series[0].name;
				let shuju = canvasLine.opts.series[0].data[currIndex];
				this.Interactive = leibie + ':' + riqi + '-' + shuju + '元';
			}
			canvasLine.showToolTip(e, {
				format: function(item, category) {
					return category + ' ' + item.name + ':' + item.data;
				}
			});
		},
		touchEndLine(e) {
			let currIndex = canvasLine.getCurrentDataIndex(e);
			if (currIndex > -1 && currIndex < canvasLine.opts.categories.length) {
				let riqi = canvasLine.opts.categories[currIndex];
				let leibie = canvasLine.opts.series[0].name;
				let shuju = canvasLine.opts.series[0].data[currIndex];
				this.Interactive = leibie + ':' + riqi + '-' + shuju + '元';
			}
			canvasLine.touchLegend(e);
			canvasLine.showToolTip(e, {
				format: function(item, category) {
					return category + ' ' + item.name + ':' + item.data;
				}
			});
		}
	}
};
</script>

<style>
/*样式的width和height一定要与定义的cWidth和cHeight相对应*/
.charts-container {
	width: 90%;
	height: 60%;
	display: flex;
	flex-direction: column !important;
	margin: 5% 5%;
	border-radius: 30rpx 30rpx;
	background-color: #FFFFFF;
}

.charts-container-2 {
	width: 90%%;
	height: 90%;
	display: flex;
	flex-direction: column !important;
	border-radius: 20rpx 20rpx;
}

.charts-container-2 .charts-item {
	width: 90%%;
	height: 42%;
	margin: 5% 5%;
	border-radius: 20rpx 20rpx;
	background-color: #B2B2B2;
}

.charts {
	width: 100%;
	height: 100%;
	border-radius: 20rpx 20rpx;
	background-color: #B2B2B2;
}

.charts-item-title {
	height: 10%;
	width: 90%;
	padding: 12upx 3%;
	flex-wrap: nowrap;
}

/* 头像昵称 */
.top_self {
	margin: 40rpx 30rpx 10rpx 30rpx;
	height: 10%;
	/* border: 1px solid red; */
	display: flex;
	justify-content: flex-start;
}
.both {
	/* border: 1px solid green; */
}
.useAvatar {
	width: 114rpx !important;
	height: 114rpx;
	background: rgb(238, 238, 238);
	border-radius: 50%;
}
.sex {
	width: 80rpx;
	line-height: 50rpx;
	align-self: center;
	text-align: center;
}
.sex image {
	width: 50rpx;
	height: 50rpx;
}
.nickName {
	display: flex;
	flex-direction: column;
	flex: 1;
	justify-content: center;
}
.nickName text {
	font-size: 25rpx;
}
.fork {
	flex: 1;
	display: flex;
	justify-content: flex-end;
}
.fork image {
	width: 40rpx;
	height: 40rpx;
}
/* 肉 */
.meat {
	width: 260rpx;
	height: 20%;
	/* border: 1px solid red; */
	margin: 0 auto;
	position: relative;
}
.meat .meatwai {
	width: 100%;
	height: 100%;
}
.meatnei {
	position: relative;
	z-index: 3;
	width: 120rpx;
	height: 120rpx;
	top: -210rpx;
	left: 68rpx;
}

/* 图表 */

.yuan {
	display: inline-block;
	width: 20rpx;
	height: 20rpx;
	background-color: #f08519;
	border-radius: 50%;
	margin: 0 10rpx;
}
.seeMore {
	display: inline-block;
	line-height: 50rpx;
	position: relative;
	top: 15rpx;
	float: right;
	/* width: 80rpx; */
	height: 50rpx;
	border: 1px solid black;
	/* font-size: 15rpx; */
	background-color: rgba(0, 0, 0, 0.4);
}
</style>
