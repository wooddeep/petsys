<template>
	<view class="qiun-columns">
		<view class="qiun-bg-white qiun-title-bar qiun-common-mt"><view class="qiun-title-dot-light">基本柱状图</view></view>
		<view class="qiun-charts"><canvas canvas-id="canvasColumn" id="canvasColumn" class="charts" @touchstart="touchColumn"></canvas></view>

		<view class="qiun-bg-white qiun-title-bar qiun-common-mt"><view class="qiun-title-dot-light">基本折线图</view></view>
		<view class="qiun-charts">
			<canvas canvas-id="canvasLine" id="canvasLine" class="charts" @touchstart="touchLine" @touchmove="moveLine" @touchend="touchEndLine"></canvas>
		</view>
	</view>
</template>

<script>
import uCharts from '@/components/u-charts/u-charts.js';
import { isJSON } from '@/common/checker.js';
import { chartsTemplate } from '@/common/charDataTemplate.js';

var _self;
var canvaColumn = null;
var canvasLine=null;
var lastMoveTime=null;//最后执行移动的时间戳
export default {
	data() {
		return {
			cWidth: '',
			cHeight: '',
			pixelRatio: 1
		};
	},
	onLoad() {
		_self = this;
		this.cWidth = uni.upx2px(750);
		this.cHeight = uni.upx2px(500);
		this.getServerData();
	},
	methods: {
		getServerData() {
			uni.request({
				url: this.websiteUrl + '/petsys/food/tend',
				method: 'POST',
				data: {
					type: 'day'
				},
				success: function(res) {
					console.log(res.data.data);
					let foodData = res.data.data;
					let d = '';
					foodData.feed.categories.forEach((item, index, array) => {
						d = new Date(item);
						if (d.getMinutes() < 10) array[index] = d.getHours().toString() + ':0' + d.getMinutes().toString();
						else array[index] = d.getHours().toString() + ':' + d.getMinutes().toString();
					});
					let chartsData = chartsTemplate;
					//这里我后台返回的是数组，所以用等于，如果您后台返回的是单条数据，需要push进去
					chartsData.categories = foodData.feed.categories.slice(0, 7);
					chartsData.series[0].data = foodData.feed.data.slice(0, 7);
					chartsData.series[0].name = 'day';
					_self.showColumn('canvasColumn', chartsData);
					
					//折线图
					foodData.eat.categories.forEach((item, index, array) => {
						d = new Date(item);
						if (d.getMinutes() < 10) array[index] = d.getHours().toString() + ':0' + d.getMinutes().toString();
						else array[index] = d.getHours().toString() + ':' + d.getMinutes().toString();
					});
					chartsData = chartsTemplate;
					//这里我后台返回的是数组，所以用等于，如果您后台返回的是单条数据，需要push进去
					chartsData.categories = foodData.eat.categories.slice(0, 7);
					chartsData.series[0].data = foodData.eat.data.slice(0, 7);
					chartsData.series[0].name = 'day';
					_self.showLine('canvasLine', chartsData);
				},
				fail: () => {
					_self.tips = '网络错误，小程序端请检查合法域名';
				}
			});
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
							position: 'right',
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
.qiun-charts {
	width: 750upx;
	height: 500upx;
	background-color: #ffffff;
}

.charts {
	width: 750upx;
	height: 500upx;
	background-color: #ffffff;
}
</style>
