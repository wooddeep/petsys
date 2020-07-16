export function getFoodTend(_self) {
	return new Promise((resolute, reject)=>{
		uni.request({
			url: _self.websiteUrl + '/petsys/food/tend',
			method: 'POST',
			data: {
				type: 'day',
				openid: _self.openId
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
				let cData = { categories: [], series: [{ name: '', data: [] }] };
				//这里我后台返回的是数组，所以用等于，如果您后台返回的是单条数据，需要push进去
				cData.categories = foodData.feed.categories.slice(0, 7);
				cData.series[0].data = foodData.feed.data.slice(0, 7);
				cData.series[0].name = 'day';
				console.log(cData);
				_self.showColumn('canvasColumn', cData);
		
				//折线图
				foodData.eat.categories.forEach((item, index, array) => {
					d = new Date(item);
					if (d.getMinutes() < 10) array[index] = d.getHours().toString() + ':0' + d.getMinutes().toString();
					else array[index] = d.getHours().toString() + ':' + d.getMinutes().toString();
				});
				let lData = { categories: [], series: [{ name: '', data: [] }] };
				//这里我后台返回的是数组，所以用等于，如果您后台返回的是单条数据，需要push进去
				lData.categories = foodData.eat.categories.slice(0, 7);
				lData.series[0].data = foodData.eat.data.slice(0, 7);
				lData.series[0].name = 'day11';
				console.log(lData);
				_self.showLine('canvasLine', lData);
				
				resolute('ok');
			},
			fail: () => {
				_self.tips = '网络错误，小程序端请检查合法域名';
				reject('failed');
			}
		});
	})
}

export function getFoodDesire(_self) {
	return new Promise((resolute, reject)=>{
		uni.request({
			url: _self.websiteUrl + '/petsys/food/desire',
			method: 'POST',
			data: {openid: _self.openId},
			success(res) {
				resolute(res);
			},
			fail(err) {
				reject(err);
			}
		})
	})
}