import datetime
import json
import threading
import time
import requests
import os
import sys
import configparser


def file_config():  # 初始化配置文件
    global p_id
    global buy_time
    global tel
    global name
    global msg
    global cookie
    cf = configparser.RawConfigParser()
    if (os.path.exists('user.ini')):
        try:
            cf.read("user.ini", encoding='utf-8')
            cookie = cf.get("user", "cookie")
            msg = cf.get("user", "msg")
            name = cf.get("user", "name")
            p_id = cf.get("user", "p_id")
            tel = cf.get("user", "tel")
            buy_time = cf.get("user", "buy_time")
            # print(cookie)
        except Exception as e:
            print("配置文件错误", e)
            input('')
            sys.exit(0)
    else:
        print("user.ini配置文件不存在当前文件夹下。")
        input('')
        sys.exit(0)


x = requests.Session()  # 实例化requests.Session对象
url = "https://wx7.jzapp.fkw.com/28359275"
preid = []
fflag = True


def get_preid(head):
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
    re = x.post(url=url + "/0/mstl_h.jsp?cmd\u003dsetWafCk_addImmePreOrder", headers=head, data=data)
    print("######get_preid######")
    print(re.text)

    if (re.json()['success']):
        preid.append(re.json()['preOrderId'])



def submit_order(head, preOrderId):
    # while True:
    data = {
        'preOrderId': preOrderId,
        'orderProp': '',
        'settleTicket': ''
    }
    re = x.post(url=url + "/0/mstl_h.jsp?cmd\u003dsetWafCk_settleOrder", headers=head, data=data)
    print("######submit_order######" + str(preOrderId))
    print(re.text)
    if(re.json()['success']):
       print(time.time())
       print("success!")
       os._exit(0)

    return re.json()['success']


def add_message(head, preOrderId):
    data = {
        'preOrderId': preOrderId,
        'mctI': 0,
        'remark': msg
    }
    re = x.post(url=url + "/0/mstl_h.jsp?cmd\u003dsetWafCk_setRemarkService", headers=head, data=data)
    print("######add_message######")
    print(re.text)
    return re.json()['success']
    # print(re.json()['success'])
    # return re.json()['success']


def add_form(head, preOrderId):
    while True:
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
        re = x.post(url=url + "/0/mstl_h.jsp?cmd\u003dsetWafCk_batchSetDeliveryService", headers=head, data=data)

        print("######add_form######")
        print(re.json())
        if(re.json()['success']):
            break
    return re.json()['success']





def miao(head):
    preOrderId = 0
    flag = False
    time4 = time.time()
    print(time4)



    while (len(preid)==0):
        multi_thread(head,2)


    ts1 = {}
    ts2 = {}

    for i in range(1):
        t = threading.Thread(target = add_message,args=(head,preid[0]))#target参数填函数名 不要用括号
        t.start()
        ts1[i] = t  #全新的线程

    for i in range(3):
        t = threading.Thread(target = add_form,args=(head,preid[0]))#target参数填函数名 不要用括号
        t.start()
        ts1[i] = t  #全新的线程

    time.sleep(0.24)
    while True:

        for i in range(4):
            t = threading.Thread(target = submit_order,args=(head,preid[0]))#target参数填函数名 不要用括号
            t.start()
            ts2[i] = t  #全新的线程
        time.sleep(0.20)
    return True


def multi_thread(head,n):

    t = []
    for page in range(0, n):
    # while True:
        t.append(
            threading.Thread(target=get_preid, args=(head,))
        )
    for thread in t:
        thread.start()
    for thread in t:
        thread.join()


if __name__ == '__main__':

    file_config()
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
    # un_time = time.mktime(dtime.timetuple())
    # now= datetime.datetime.fromtimestamp(buy_time)
    # t = time.time()
    # print(int(round(t * 1000)))
    # print(timestamp)
    print("running.....")
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        time1 = time.time()

        # 判断是否到达抢购时间
        if int(round(time1 * 1000)) >= timestamp:

            #     aaa=1
            #
            # else:
            # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

            print("#####################开始抢购####################")
            # break
            time4 = time.time()
            end_time = int(round(time4 * 1000))
            result = miao(head)
            time3 = time.time()
            endtime = int(round(time3 * 1000))
            print("result" + str(result))
            if result:
                print("###秒杀成功###")

                # print('标准时间戳:%d' % timestamp)
                # print('开始时间戳:%d' % end_time)
                # print('结束时间戳:%d' % endtime)
                # time2 = time.time()
                end = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                # print('开始时间:%s' % start_time)
                print('结束时间:%s' % end)
                print("耗时：%f s" % (int(endtime - end_time) / 1000))
                # print("耗时：%d " % (end - start_time))
                break
            else:
                print("秒杀失败")
                time.sleep(0.1)
    # input("ok")

# if __name__ == '__main__':
#
#
#     p = mp.Pool(1)
#     p.map(task)  # range(0,1000) if you want to replicate your example
#     p.close()
#     p.join()
