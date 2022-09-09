import datetime
import json
import time
import requests
from cffi.backend_ctypes import long

##################配置 ################

p_id = 'xxx' #商品id
buy_time = "2022-09-09 11:27:00000000"     #购买时间
tel="xxxx"  #电话
name="xxx" #姓名
msg="xxxx" #买家留言
cookie='xxx'


##################配置 ################

x = requests.Session()  # 实例化requests.Session对象
url = "https://wx7.jzapp.fkw.com/28359275"



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
    a = 0
    try:
        a = re.json()['preOrderId']
        print("生成的订单号是：%d"%a)
    except Exception as err:
        print('An exception happened: ' + str(err))
    return a


def submit_order(head, preOrderId):
    data = {
        'preOrderId': preOrderId,
        'orderProp': '',
        'settleTicket': ''
    }
    re = x.post(url=url + "/0/mstl_h.jsp?cmd\u003dsetWafCk_settleOrder", headers=head, data=data)
    print("######submit_order######")
    print(re.text)

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



def add_form(head, preOrderId):
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



def miao(head):
    # 生成订单id
    preOrderId = get_preid(head)
    print("preOrderId=%d" % preOrderId)
    # 填写订单留言
    add_message(head, preOrderId)
    # 填写表单
    add_form(head, preOrderId)
    # 提交订单
    result = submit_order(head, preOrderId)
    return result


if __name__ == '__main__':
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
        if int(round(time1 * 1000)) >= timestamp :

            start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            print("#####################开始抢购####################")
            # break
            result = miao(head)
            if result:
                print("###秒杀成功###")
                time3 = time.time()
                endtime = int(round(time3 * 1000))
                # print('标准时间戳:%d' % timestamp)
                # print('结束时间戳:%d' % endtime)
                # time2 = time.time()
                end= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                print('开始时间:%s' % start_time)
                print('结束时间:%s' % end)
                print("耗时：%d " % (endtime - timestamp))
                break
            else:
                print("秒杀失败")
                time.sleep(0.1)
