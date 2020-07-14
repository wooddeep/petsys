#
# @description: 排名相关路由
#


from __future__ import print_function

import json

import eventlet
from flask import request

from pool import MysqlPool

def add_rank_routes(app):

    mp = MysqlPool()

    # 通过 本月的 均值 来求排行
    query_rank_by_avg = \
    '''
    select sum_table.device_id, today * divider_table.count / sum_table.sum rate from 
    (
        select device_id, sum(eat) `sum` from device_data 
        where date_format(date, "%%Y-%%m") = date_format(now(), "%%Y-%%m") 
        group by device_id
    ) sum_table
    left join
    (
        select device_id, count(device_id) `count` from 
        (
            select device_id, date_format(date, "%%Y-%%m-%%d") 
            from device_data where date_format(date, "%%Y-%%m") = date_format(now(), "%%Y-%%m") 
            group by device_id, date_format(date, "%%Y-%%m-%%d")
        ) a
        group by device_id
    ) divider_table
    on sum_table.device_id = divider_table.device_id
    left join
    (
        select device_id, sum(eat) today from device_data 
        where date_format(date, "%%Y-%%m-%%d") = date_format(now(), "%%Y-%%m-%%d") 
        group by device_id
    ) today_table
    on sum_table.device_id = today_table.device_id
    order by rate desc;
    '''

    # 低食欲 总数
    query_low_desire_count = \
    '''
    select count(mid_data.device_id) `count` from 
    (
        select device_id, group_concat(date) date_group, group_concat(`sum`) sum_group from
        (
            select id, device_id, date_format(date, "%%Y-%%m-%%d") date, sum(eat) `sum` from device_data 
            where date_format(date, "%%Y-%%m") = date_format(now(), "%%Y-%%m") 
            group by device_id, date_format(date, "%%Y-%%m-%%d")
        ) temp
        group by device_id
    ) mid_data
    left join (
        select id, device_id, date_format(date, "%%Y-%%m-%%d") date, sum(eat) `sum` from device_data 
        where date_format(date, "%%Y-%%m-%%d") = date_format(now(), "%%Y-%%m-%%d") 
        group by device_id, date_format(date, "%%Y-%%m-%%d")
    ) today_data
    on mid_data.device_id = today_data.device_id
    where today_data.sum / GET_MIDDLE_DATA(sum_group) < 0.5
    '''

    # 普通食欲 总数
    query_com_desire_count = \
    '''
    select count(mid_data.device_id) `count` from 
    (
        select device_id, group_concat(date) date_group, group_concat(`sum`) sum_group from
        (
            select id, device_id, date_format(date, "%%Y-%%m-%%d") date, sum(eat) `sum` from device_data 
            where date_format(date, "%%Y-%%m") = date_format(now(), "%%Y-%%m") 
            group by device_id, date_format(date, "%%Y-%%m-%%d")
        ) temp
        group by device_id
    ) mid_data
    left join (
        select id, device_id, date_format(date, "%%Y-%%m-%%d") date, sum(eat) `sum` from device_data 
        where date_format(date, "%%Y-%%m-%%d") = date_format(now(), "%%Y-%%m-%%d") 
        group by device_id, date_format(date, "%%Y-%%m-%%d")
    ) today_data
    on mid_data.device_id = today_data.device_id
    where today_data.sum / GET_MIDDLE_DATA(sum_group) >= 0.5
    '''

    # 食欲低于 50% 的 排行
    query_low_desire_rank_by_mid = \
    '''
    select page_date.device_id, page_date.rate, user.name from 
    (
        select device_id, rate from (
            select mid_data.device_id, sum_group, GET_MIDDLE_DATA(sum_group) `mid`, today_data.sum today, 
            today_data.sum / GET_MIDDLE_DATA(sum_group) rate from 
            (
                select device_id, group_concat(date) date_group, group_concat(`sum`) sum_group from
                (
                    select id, device_id, date_format(date, "%%Y-%%m-%%d") date, sum(eat) `sum` from device_data 
                    where date_format(date, "%%Y-%%m") = date_format(now(), "%%Y-%%m") 
                    group by device_id, date_format(date, "%%Y-%%m-%%d")
                ) temp
                group by device_id
            ) mid_data
            left join (
                select id, device_id, date_format(date, "%%Y-%%m-%%d") date, sum(eat) `sum` from device_data 
                where date_format(date, "%%Y-%%m-%%d") = date_format(now(), "%%Y-%%m-%%d") 
                group by device_id, date_format(date, "%%Y-%%m-%%d")
            ) today_data
            on mid_data.device_id = today_data.device_id
            where today_data.sum / GET_MIDDLE_DATA(sum_group) < 0.5
        ) temp
        order by rate
        limit %s, 10
    ) page_date
    left join user 
    on  page_date.device_id = user.device_id
    ;
    '''

    # 食欲低于 50% 的 排行
    query_com_desire_rank_by_mid = \
    '''
    select page_date.device_id, page_date.rate, user.name from 
    (
        select device_id, rate from (
            select mid_data.device_id, sum_group, GET_MIDDLE_DATA(sum_group) `mid`, today_data.sum today, 
            today_data.sum / GET_MIDDLE_DATA(sum_group) rate from 
            (
                select device_id, group_concat(date) date_group, group_concat(`sum`) sum_group from
                (
                    select id, device_id, date_format(date, "%%Y-%%m-%%d") date, sum(eat) `sum` from device_data 
                    where date_format(date, "%%Y-%%m") = date_format(now(), "%%Y-%%m") 
                    group by device_id, date_format(date, "%%Y-%%m-%%d")
                ) temp
                group by device_id
            ) mid_data
            left join (
                select id, device_id, date_format(date, "%%Y-%%m-%%d") date, sum(eat) `sum` from device_data 
                where date_format(date, "%%Y-%%m-%%d") = date_format(now(), "%%Y-%%m-%%d") 
                group by device_id, date_format(date, "%%Y-%%m-%%d")
            ) today_data
            on mid_data.device_id = today_data.device_id
            where today_data.sum / GET_MIDDLE_DATA(sum_group) >= 0.5
        ) temp
        order by rate
        limit %s, 10
    ) page_date
    left join user 
    on  page_date.device_id = user.device_id
    ;
    '''


    query_user_list = \
    '''
        select * from user 
    '''

    query_eat_rank = \
    '''
    select a.eat, b.name from (
        select device_id, sum(eat) eat from device_data 
        where date_format(date, "%%Y-%%m-%%d") = date_format(now(), "%%Y-%%m-%%d") 
        group by device_id 
        order by eat desc
        limit %s, 10
    ) a
    left join user b on a.device_id = b.device_id;
    '''

    query_desire_rank = \
    '''
    select a.eat, b.name from (
        select device_id, sum(eat) eat from device_data 
        where date_format(date, "%%Y-%%m-%%d") = date_format(now(), "%%Y-%%m-%%d") 
        group by device_id 
        order by eat desc
        limit %s, 10
    ) a
    left join user b on a.device_id = b.device_id;
    '''

    def friend_operate(sql, arg):
        try:
            #print(sql)
            rec_list = mp.fetch_all(sql,  arg)
            data = {"code": 0, "data": rec_list}
            #print(data)
        except Exception as e:
            print(e)
            data = {"code": 1, "msg": "%s" % str(e)}

        return data

    @app.route("/pysys/friend/add")
    def friend_add():
        pass

    # 查询好友, 过滤出自己
    @app.route("/pysys/friend/query")
    def friend_query():
        pass

    # 查询所有用户，作为推荐好友
    # curl -X POST http://127.0.0.1:8080/petsys/user/list -d {"type":"day"} # "day", "week", "month"
    @app.route("/petsys/user/list", methods=['POST'])
    def friend_list():
        data = request.get_data()
        try:
            json_data = json.loads(data.decode("utf-8"))

            handler = eventlet.spawn(friend_operate, query_user_list, {})
            result = handler.wait()
            raw_data = result['data']
            if result['code'] == 0:
                out = {}
                categories = []
                feed = []
                eat = []
                for onedata in raw_data:
                    categories.append(onedata['time'])
                    feed.append(int(onedata['feed']))
                    eat.append(int(onedata['eat']))
                out["feed"] = {"categories": categories, "data": feed}
                out["eat"] = {"categories": categories, "data": eat}
                return {"code": 0, "msg": "success!", "data": out}
            else:
                return '{"code": 2, "msg": "%s"}' % result['msg']
        except Exception as e:
            print("# exception: %s" % e)
            return '{"code": 1, "msg": "body error!"}'

    # 查询所有用户，作为推荐好友
    # curl -X POST http://127.0.0.1:8080/petsys/friend/rank -d {"type":"eat"} # "eat", "desire"
    @app.route("/petsys/friend/rank", methods=['POST'])
    def friend_rank():
        data = request.get_data()
        try:
            json_data = json.loads(data.decode("utf-8"))
            type = json_data['type']
            sql_map = {"eat": query_eat_rank, "desire": query_low_desire_rank_by_mid}

            handler = eventlet.spawn(friend_operate, sql_map[type], 0)
            result = handler.wait()
            raw_data = result['data']

            if result['code'] == 0:
                out = {}
                name = []
                rate = []
                for onedata in raw_data:
                    name.append(onedata['name'])
                    rate.append(int(onedata['eat']))
                out["name"] = name
                out["rate"] = rate

                return {"code": 0, "msg": "success!", "data": out}
            else:
                return '{"code": 2, "msg": "%s"}' % result['msg']

        except Exception as e:
            print("# exception: %s" % e)
            return '{"code": 1, "msg": "body error!"}'

    # 查询所有用户，作为推荐好友
    # curl -X POST http://127.0.0.1:8080/petsys/desire/rank/low -d {"start": 1}
    @app.route("/petsys/desire/rank/low", methods=['POST'])
    def desire_low_rank():
        data = request.get_data()
        try:
            json_data = json.loads(data.decode("utf-8"))
            start = int(json_data['start'])
            handler = eventlet.spawn(friend_operate, query_low_desire_count, {})  # 食欲 < 0.5
            result = handler.wait()
            low_data = result['data']
            if len(low_data) <= 0:
                return {"code": 0, "msg": "success!", "data": {}}
            pass
            total = int(low_data[0]["count"])

            handler = eventlet.spawn(friend_operate, query_low_desire_rank_by_mid, start) # 食欲 < 0.5
            result = handler.wait()
            low_data = result['data']
            if result['code'] == 0:
                low = {}
                device_id = []
                rate = []
                name = []
                for onedata in low_data:
                    device_id.append(int(onedata['device_id']))
                    rate.append(float(onedata['rate']))
                    name.append(onedata['name'])
                low["device_id"] = device_id
                low["rate"] = rate
                low["name"] = name
                low['total'] = total
                return {"code": 0, "msg": "success!", "data": low}
            else:
                return '{"code": 2, "msg": "%s"}' % result['msg']
            pass
        except Exception as e:
            print("# exception: %s" % e)
            return '{"code": 1, "msg": "body error!"}'


    # 查询所有用户，作为推荐好友
    # curl -X POST http://127.0.0.1:8080/petsys/desire/rank/com -d {"start": 1} # "eat", "desire"
    @app.route("/petsys/desire/rank/com", methods=['POST'])
    def desire_com_rank():
        data = request.get_data()
        try:
            json_data = json.loads(data.decode("utf-8"))
            start = int(json_data['start'])
            handler = eventlet.spawn(friend_operate, query_com_desire_count, {})  # 食欲 < 0.5
            result = handler.wait()
            low_data = result['data']
            if len(low_data) <= 0:
                return {"code": 0, "msg": "success!", "data": {}}
            pass
            total = int(low_data[0]["count"])

            handler = eventlet.spawn(friend_operate, query_com_desire_rank_by_mid, start) # 食欲 >= 0.5
            result = handler.wait()
            com_data = result['data']
            if result['code'] == 0:
                com = {}
                device_id = []
                rate = []
                name = []
                for onedata in com_data:
                    device_id.append(int(onedata['device_id']))
                    rate.append(float(onedata['rate']))
                    name.append(onedata['name'])
                com["device_id"] = device_id
                com["rate"] = rate
                com["name"] = name
                com['total'] = total
                return {"code": 0, "msg": "success!", "data": com}
            else:
                return '{"code": 2, "msg": "%s"}' % result['msg']
            pass

            return {"code": 0, "msg": "success!", "data": out}
        except Exception as e:
            print("# exception: %s" % e)
            return '{"code": 1, "msg": "body error!"}'