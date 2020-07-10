#
# @description: 图标相关路由
#

from __future__ import print_function

import json

import eventlet
from flask import request

from pool import MysqlPool


def add_chart_routes(app):
    #  修改列类型
    #  alter table device_data alter column feed set default 0;

    # 当前时刻点 往前推12个小时, 按个时段聚合 查询 数据
    query_feed_eat_oneday = \
        '''
        select date_format(date, "%%Y-%%m-%%d %%H:00:00") time, sum(feed) feed, sum(eat) eat 
        from device_data
        where date < now() 
        group by date_format(date, "%%Y-%%m-%%d %%H") 
        order by date  
        limit 12;
        '''

    query_feed_eat_oneweek = \
        '''
        select date_format(date, "%%Y-%%m-%%d") time, sum(feed) feed, sum(eat) eat 
        from device_data 
        where date <= now() 
        group by date_format(date, "%%Y-%%m-%%d") 
        order by date  
        limit 7;
        '''

    query_feed_eat_onemonth = \
        '''
        select date_format(date, "%%Y-%%m-%%d") time, sum(feed) feed, sum(eat) eat 
        from device_data 
        where date <= now() 
        group by date_format(date, "%%Y-%%m-%%d") 
        order by date  
        limit 30;
        '''

    # 查询本月数据中前10天的数据，并且按顺序， 取中间值(非平均数) & 获取当前数据
    eat_desire_list = \
    '''
    select day, eat from 
        (select date_format(date, "%%Y-%%m-%%d") `day`, sum(eat) eat 
            from device_data  
            where date_format(date, "%%Y-%%m") = date_format(now(), "%%Y-%%m") 
            group by date_format(date, "%%Y-%%m-%%d") 
            order by date limit 10
        ) a 
    order by eat;
    '''

    eat_desire_today = \
    '''
    select date_format(date, "%%Y-%%m-%%d") `day`, sum(eat) eat from device_data  where date_format(date, "%%Y-%%m-%%d") = date_format(now(), "%%Y-%%m-%%d");
    '''

    mp = MysqlPool()

    def find_food_info(sql, arg):
        try:
            rec_list = mp.fetch_all(sql, arg)
            data = {"code": 0, "data": rec_list}
            #print(data)
        except Exception as e:
            print(e)
            data = {"code": 1, "msg": "%s" % str(e)}

        return data

    # curl -X POST http://127.0.0.1:8080/petsys/feed/tend -d {"type":"day"} # "day", "week", "month"
    @app.route("/petsys/food/tend", methods=['POST'])
    def food_info():
        data = request.get_data()
        try:
            json_data = json.loads(data.decode("utf-8"))
            type = json_data['type']
            sql_map = {"day": query_feed_eat_oneday, "week": query_feed_eat_oneweek, "month":query_feed_eat_onemonth}

            handler = eventlet.spawn(find_food_info, sql_map[type], {})
            result = handler.wait()
            raw_data = result['data']
            if result['code'] == 0:
                data = []
                for onedata in raw_data:
                    cell = {}
                    cell['time'] = onedata['time']
                    cell['feed'] = int(onedata['feed'])
                    cell['eat'] = int(onedata['eat'])
                    data.append(cell)
                return {"code": 0, "msg": "success!", "data": data}
            else:
                return '{"code": 2, "msg": "%s"}' % result['msg']
        except Exception as e:
            print("# exception: %s" % e)
            return '{"code": 1, "msg": "body error!"}'

    # curl -X POST http://127.0.0.1:8080/petsys/feed/desire
    @app.route("/petsys/food/desire", methods=['POST'])
    def desire_info():
        #data = request.get_data()
        try:
            handler = eventlet.spawn(find_food_info, eat_desire_list, {})
            result = handler.wait()
            desire_list = result['data']
            desire_avg = int(desire_list[int(len(desire_list) / 2)]['eat'])
            print("desire_avg = %d" %  desire_avg)
            handler = eventlet.spawn(find_food_info, eat_desire_today, {})
            result = handler.wait()
            desire_today = result['data'][0]['eat']
            print("today = %d" % desire_today)

            if result['code'] == 0:
                return {"code": 0, "msg": "success!", "data": '%.2f%%' % float(desire_today * 100 / desire_avg)}
            else:
                return '{"code": 2, "msg": "%s"}' % result['msg']
        except Exception as e:
            print("# exception: %s" % e)
            return '{"code": 1, "msg": "body error!"}'