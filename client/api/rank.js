
// 异步请求获取common rank data
export function getCommonRankData(obj, pageNum, pageSize) {
	let that = obj;
	return new Promise((resolute, reject)=>{
		uni.request({
			url: that.websiteUrl + '/petsys/desire/rank/com',
			method: 'POST',
			data: {
				start: 1
			},
			success: (res) => {
				console.log(res);
				let data = res.data.data;
				let list = [];
				for (let i = 0; i < data.total; i++) {
					let item = {device_id: 0, icon_path:'', name:'', rate: 0};
					item.device_id = data.device_id[i];
					item.icon_path = data.icon_path[i];
					item.name = data.name[i];
					item.rate = data.rate[i];
					list.push(item);
				}
				
				resolute(list);
			},
			fail: (err) => {
				uni.showToast({
					icon: 'none',
					title: '网络连接失败'
				});
				console.error('网络连接失败：' + JSON.stringify(err));
				reject(err)
			}
		})
	})
}

// 异步请求获取low rank data
export function getLowRankData(obj, pageNum, pageSize) {
	let that = obj;
	return new Promise((resolute, reject)=>{
		uni.request({
			url: that.websiteUrl + '/petsys/desire/rank/low',
			method: 'POST',
			data: {
				start: 1
			},
			success: (res) => {
				console.log(res);
				let data = res.data.data;
				let list = [];
				for (let i = 0; i < data.total; i++) {
					let item = {device_id: 0, icon_path:'', name:'', rate: 0};
					item.device_id = data.device_id[i];
					item.icon_path = data.icon_path[i];
					item.name = data.name[i];
					item.rate = data.rate[i];
					list.push(item);
				}
				
				resolute(list);
			},
			fail: (err) => {
				uni.showToast({
					icon: 'none',
					title: '网络连接失败'
				});
				console.error('网络连接失败：' + JSON.stringify(err));
				reject(err)
			}
		})
	})
}