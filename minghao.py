import datetime
import json
import threading
import time
import requests
import os
import sys
import configparser




x = requests.Session()  # 实例化requests.Session对象
url = "https://wx7.jzapp.fkw.com/28359275"
preid = []



def get_preid(head,proxy):
    data = {
        'pdInfoList': "[]",
        'marketingType': 0,
        'marketingId': 0,
        'marketingDetailId': 0,
        'fromDetail': 'true',
        'optionList': "[]",
        'amount': 1,
        'productId': p_id

    }
    re = x.post(url=url + "/0/mstl_h.jsp?cmd\u003dsetWafCk_addImmePreOrder", headers=head, data=data,proxies=proxy)
    print("######get_preid######"+name)
    print(re.text)

    if (re.json()['success']):
        preid.append(re.json()['preOrderId'])



def submit_order(head, preOrderId,proxy):

    data = {
        'preOrderId': preOrderId,
        'orderProp': '',
        'settleTicket': ''
    }
    re = x.post(url=url + "/0/mstl_h.jsp?cmd\u003dsetWafCk_settleOrder", headers=head, data=data,proxies=proxy)
    print("######submit_order######" + str(preOrderId)+name)
    print(re.text)
    return re.json()['success']


def add_message(head, preOrderId,proxy):
    data = {
        'preOrderId': preOrderId,
        'mctI': 0,
        'remark': msg
    }
    re = x.post(url=url + "/0/mstl_h.jsp?cmd\u003dsetWafCk_setRemarkService", headers=head, data=data,proxies=proxy)
    print("######add_message######"+name)
    print(re.text)
    return re.json()['success']



def add_form(head, preOrderId,proxy):

    sz = [{
        "preOrderId": preOrderId,
        "mctId": 0,
        "selfRaisingMemberInfo": {
            "prop0": name,
            "prop1": tel
        },
        "shipType": "",
        "shipSort": 8,
        "deliveryStyle": 2,
        "selfRaisingPoint": {
            "id": 1,
            "name": "重庆明好医院",
            "rai": {"prc": "500000",
                    "cic": "500100",
                    "coc": "500107",
                    "sta": "重庆明好医院"},
            "ais": "重庆重庆市九龙坡区重庆明好医院",
            "phone": "19112280053",
            "pp": {
                "lng": 106.260422,
                "lat": 29.289093, "pt": 1},
            "mai": 1,
            "idm": 'false',
            "distance": 41438,
            "distanceKilometer": 41.4
        },
        "errorMessage": ""}]
    data = {
        'preOrderId': preOrderId,
        'batchDeliveryList': json.dumps(sz)

    }
    re = x.post(url=url + "/0/mstl_h.jsp?cmd\u003dsetWafCk_batchSetDeliveryService", headers=head, data=data,proxies=proxy)

    print("######add_form######"+name)
    print(re.json())
    return re.json()['success']





def miao(head,proxy):
    preOrderId = 0
    time4 = time.time()
    while (len(preid)==0):
        multi_thread(head,2,proxy)

    while True:
        f=add_message(head,preid[0],proxy)
        if(f):
            break
    while True:
        f=add_form(head,preid[0],proxy)
        if(f):
            break
    while True:
        f=submit_order(head,preid[0],proxy)
        if(f):
            print("###秒杀成功###")
            print("姓名："+name)
            print("电话："+tel)
            print("身份证："+msg)
            time5 = time.time()
            print("耗时："+str(time5-time4))
            end = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            print('结束时间:%s' % end)
            # input("success!")
            break

    return True


def multi_thread(head,n,proxy):

    t = []
    for page in range(0, n):
    # while True:
        t.append(
            threading.Thread(target=get_preid, args=(head,proxy))
        )
    for thread in t:
        thread.start()
    for thread in t:
        thread.join()


def mmain(proxy,item):

    global p_id
    global buy_time
    global tel
    global name
    global msg
    global cookie
    user=[]
    for i in item:

        user.append(i[1])



    p_id=user[0]
    buy_time=user[1]
    tel=user[2]
    name=user[3]
    msg=user[4]
    cookie=user[5]
    head = {
        "Host": "wx7.jzapp.fkw.com",
        "Connection": "keep-alive",
        "Content-Length": "124",
        "charset": "utf-8",
        "cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2006J10C Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/3972 MicroMessenger/8.0.27.2220(0x28001B37) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "Referer": "https://servicewechat.com/wx8e237ddfbc2c3e99/3/page-frame.html"
    }
    dtime = datetime.datetime.now()
    datetime_obj = datetime.datetime.strptime(buy_time, "%Y-%m-%d %H:%M:%S%f")  # 格式化为datetime类型
    timestamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
    print(name+"#####running.....")
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        time1 = time.time()
        if int(round(time1 * 1000)) >= timestamp:
            print("#####################开始抢购####################")
            result = miao(head,proxy)
            break
