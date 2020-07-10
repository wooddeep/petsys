"""

A small Test application to show how to use Flask-MQTT.

"""

#
# 通过docker测试
# sudo docker run -it --rm --net=host -v /home/pet/mproxy:/home/pet/mproxy python:mqtt python /home/pet/mproxy/mproxy.py
#

# 
# docker 启动个容器
# sudo docker run -p 3306:3306  --restart=always  --privileged=true --name mysql -v /opt/mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD="123456" -d mysql:5.7
#

from __future__ import print_function

import json
import os
import time
from datetime import datetime

import eventlet
from flask import Flask, request
from flask_bootstrap import Bootstrap
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename

from httpclient import HttpsClient
from pool import MysqlPool
from proto import Protocol

from chart import add_chart_routes
from rank import add_rank_routes

eventlet.monkey_patch()

app = Flask(__name__)

add_chart_routes(app)
add_rank_routes(app)

app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = '47.108.65.95'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_CLEAN_SESSION'] = True

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
static = os.path.join(basedir, 'static')

# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

mqtt = Mqtt(app)
mqtt.subscribe("petdata")
socketio = SocketIO(app)
bootstrap = Bootstrap(app)

mp = MysqlPool()
proto = Protocol()

pool = eventlet.GreenPool(100)
pile = eventlet.GreenPile(pool)


# mqtt相关

#
# 插入宠物数据
#
def insert_device_data(lsb, msb, date, code):

    ## TODO 根据上一次数据的 计算 是吃 还是 填
    sql = 'select lsb from device_data where `device_id`=(select `id` from `device` where `code`="%s") order by date desc limit 0, 1;' % code

    result = mp.fetch_one(sql, {})
    prev_weight = result['lsb']
    if prev_weight == None:
        prev_weight = 0

    feed = 0
    eat = 0
    curr_weight = int(lsb)
    if curr_weight > prev_weight:
        feed = curr_weight - prev_weight
    else:
        eat = prev_weight - curr_weight

    sql = 'insert into `device_data` set `lsb`=%d, `msb`=%d, `date`="%s", feed=%d, eat=%d, `device_id`=(select `id` from `device` where `code`="%s")' % (
        lsb, msb, date, feed, eat, code)
    #print(sql)
    conn = mp.POOL.connection()
    cursor = conn.cursor()
    data = cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return data


#
# 插入用户
#
def insert_user(name, sex, icon_path, food_brand, phone, openid):
    try:
        sql = 'insert into `user` set `name`="%s", `sex`="%s", `icon_path`="%s", food_brand="%s", phone="%s", openid="%s"' % (
            name, sex, icon_path, food_brand, phone, openid)
        conn = mp.POOL.connection()
        cursor = conn.cursor()
        data = cursor.execute(sql)
        conn.commit()
        data = {"code": 0}
    except Exception as e:
        print(e)
        data = {"code": 1, "msg": "%s" % str(e)}
    finally:
        cursor.close()
        conn.close()
    return data

#
# 修改用户
#
def modify_user(name, sex, icon_path, food_brand, phone, openid):
    try:
        sql = 'update `user` set `name`="%s", `sex`="%s", `icon_path`="%s", `food_brand`="%s", `phone`="%s" where `openid`="%s"' % (
            name, sex, icon_path, food_brand, phone, openid)
        conn = mp.POOL.connection()
        cursor = conn.cursor()
        data = cursor.execute(sql)
        conn.commit()
        data = {"code": 0}
    except Exception as e:
        print(e)
        data = {"code": 1, "msg": "%s" % str(e)}
    finally:
        cursor.close()
        conn.close()
    return data

#
# 查询用户
#

def find_user(sql, arg):
    try:
        rec_list = mp.fetch_all(sql, arg)
        data = {"code": 0, "data": rec_list}
    except Exception as e:
        print(e)
        data = {"code": 1, "msg": "%s" % str(e)}

    return data


#
# http get handler
#
def http_get_handler(url, param={}):
    try:
        result = HttpsClient.https_get(url)
        data = json.loads(result)
        if 'errcode' in data:
            data['code'] = data['errcode']
        else:
            data['code'] = 0
        # print('&&&&&')
        # print(data)
    except Exception as e:
        print(e)
        data = {"code": 1, "msg": "%s" % str(e)}

    return data


@socketio.on('publish')
def handle_publish(json_str):
    print('i will subscribe')
    data = json.loads(json_str)
    mqtt.publish(data['topic'], data['message'])


@socketio.on('subscribe')
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt.subscribe(data['topic'])


@socketio.on('unsubscribe_all')
def handle_unsubscribe_all():
    mqtt.unsubscribe_all()


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    package = bytes(message.payload)

    if package[0] == 0xAA:
        lsb = proto.get_lsb(package)
        msb = proto.get_msb(package)
        dev_code = proto.get_dev_code(package)

        dt = datetime.now()
        date = dt.strftime('%Y-%m-%d %H:%M:%S')

        pile.spawn(insert_device_data, lsb, msb, date, dev_code)
    pass


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    # print(level, buf)
    pass


#
# 接口相关
#

# https://zhang-shengping.github.io/cosz3_blog/%E4%BD%BF%E7%94%A8%E6%80%BB%E7%BB%93%E8%AE%B0%E5%BD%95/2018/05/04/Python-eventlet-basics/
# https://www.jianshu.com/p/6d8e131f9f8a

# curl -X POST http://127.0.0.1:8080/petsys/user/add -d {"username":"lee", "sex":"male", "food_brand":"caffe", "phone":"13500000000", "openid":"openid", "icon_path":"null"}
@app.route('/petsys/user/add', methods=['POST'])
def user_add():
    data = request.get_data()
    try:
        json_data = json.loads(data.decode("utf-8"))
        print(json_data)
        # name, sex, icon_path, food_brand, phone, openid
        name = json_data['username']
        sex = json_data['sex']
        icon_path = json_data['icon_path']
        food_brand = json_data['food_brand']
        phone = json_data['phone']
        openid = json_data['openid']

        handler = eventlet.spawn(insert_user, name, sex, icon_path, food_brand, phone, openid)
        result = handler.wait()
        print(result)
        if result['code'] == 0:
            return '{"code": 0, "msg": "success!"}'
        else:
            return '{"code": 2, "msg": "%s"}' % result['msg']
    except Exception as e:
        print("# exception: %s" % e)
        return '{"code": 1, "msg": "body error!"}'

# curl -X POST http://127.0.0.1:8080/petsys/user/modify -d {"username":"lee", "sex":"male", "food_brand":"caffe", "phone":"13500000000", "openid":"openid", "icon_path":"null"}
@app.route('/petsys/user/modify', methods=['POST'])
def user_modify():
    data = request.get_data()
    try:
        json_data = json.loads(data.decode("utf-8"))
        print(json_data)
        # name, sex, icon_path, food_brand, phone, openid
        name = json_data['username']
        sex = json_data['sex']
        icon_path = json_data['icon_path']
        food_brand = json_data['food_brand']
        phone = json_data['phone']
        openid = json_data['openid']

        handler = eventlet.spawn(modify_user, name, sex, icon_path, food_brand, phone, openid)
        result = handler.wait()
        print(result)
        if result['code'] == 0:
            return '{"code": 0, "msg": "success!"}'
        else:
            return '{"code": 2, "msg": "%s"}' % result['msg']
    except Exception as e:
        print("# exception: %s" % e)
        return '{"code": 1, "msg": "body error!"}'


# curl -X POST http://127.0.0.1:8080/petsys/user/list -d {"openid":"openid"}
@app.route('/petsys/user/list', methods=['POST'])
def user_list():
    data = request.get_data()
    try:
        json_data = json.loads(data.decode("utf-8"))
        print(json_data)
        # name, sex, icon_path, food_brand, phone, openid
        name = json_data['username']
        sex = json_data['sex']
        icon_path = json_data['icon_path']
        food_brand = json_data['food_brand']
        phone = json_data['phone']
        openid = json_data['openid']

        handler = eventlet.spawn(modify_user, name, sex, icon_path, food_brand, phone, openid)
        result = handler.wait()
        print(result)
        if result['code'] == 0:
            return '{"code": 0, "msg": "success!"}'
        else:
            return '{"code": 2, "msg": "%s"}' % result['msg']
    except Exception as e:
        print("# exception: %s" % e)
        return '{"code": 1, "msg": "body error!"}'


# 用户注册判断
# curl -X POST http://127.0.0.1:8080/petsys/user/check -d {"openid":"123"}
@app.route('/petsys/user/check', methods=['POST'])
def user_check():
    data = request.get_data()
    try:
        json_data = json.loads(data.decode("utf-8"))
        openid = json_data['openid']

        handler = eventlet.spawn(find_user, "select * from user where openid=(%s)", openid)
        result = handler.wait()

        if result['code'] == 0:
            count = len(result['data'])
            if (count > 0):
                return {"code": 0, "msg": "success!", "data":result['data']}
            else:
                return {"code": 1, "msg": "not registered!"}
        else:
            return '{"code": 2, "msg": "%s"}' % result['msg']
    except Exception as e:
        print("# exception: %s" % e)
        return '{"code": 1, "msg": "body error!"}'


# appid secret  jscode
# https://api.weixin.qq.com/sns/jscode2session?appid=wx1a443836ab722a66&secret=0553c0fe17821d344e347c206f3ed4b1&js_code=0816w3Ek2MeXMA01t6Fk2n77Ek26w3Ek&grant_type=authorization_code
# curl -X POST http://192.168.141.171:8080/petsys/openid/get -d '{"jscode":"jscode"}'
@app.route('/petsys/openid/get', methods=['POST'])
def openid_get():
    data = request.get_data()
    try:
        json_data = json.loads(data.decode("utf-8"))
        appid = "wx1a443836ab722a66"
        secret = "0553c0fe17821d344e347c206f3ed4b1"
        jscode = json_data['jscode']
        query_url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code" % (
            appid, secret, jscode)
        handler = eventlet.spawn(http_get_handler, query_url)
        result = handler.wait()
        if result['code'] == 0:
            return {"code": 0, "msg": "success!", "data": result}
        else:
            result['code'] = 2
            return str(result)
    except Exception as e:
        print("# exception: %s" % e)
        return '{"code": 1, "msg": "body error!"}'


# 文件上传
@app.route('/petsys/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    openid = request.args.get("openid")

    print("openid = " + str(openid))

    file_dir = os.path.join(static, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    f = request.files['file']  # 从表单的file字段获取文件，myfile为该表单的name值
    fname = secure_filename(f.filename)
    ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
    unix_time = int(time.time())
    new_filename = str(openid) + "_" + str(unix_time) + '.' + ext  # 修改了上传的文件名
    print("###file dir: %s, file name %s" % (file_dir, new_filename))
    f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
    return {"code": 0, "msg": "上传成功", "data": {"filename": "/static/upload/" + new_filename}}


if __name__ == '__main__':
    # important: Do not use reloader because this will create two Flask instances.
    # Flask-MQTT only supports running with one instance
    socketio.run(app, host='0.0.0.0', port=8080, use_reloader=False, debug=False)
