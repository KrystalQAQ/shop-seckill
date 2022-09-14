import configparser
import os
import sys

import requests
from prettytable import PrettyTable



x = requests.Session()  # 实例化requests.Session对象
url = "https://wx7.jzapp.fkw.com/28359275"
productNameList = []
orderStausNameList = []
idList = []
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


def getOrder(head):
    idList=[]
    productNameList=[]
    orderStausNameList=[]
    data = {
        'page': 0,
        'orderStatusList': [0]
    }
    re = x.post(url + "/0/wxmallapp_h.jsp?cmd=getOrderList", headers=head, data=data)
    for i in re.json()['rtData'].get('orderList'):
        # print(i['productList'][0]['productName'])
        productNameList.append(i['productList'][0]['productName'])
        orderStausNameList.append(i['orderStausName'])
        idList.append(i['id'])
    table = PrettyTable(['ID', '产品', '状态'])
    for i in range(len(productNameList)):
        a=idList[i]
        b=productNameList[i]
        c=orderStausNameList[i]
        table.add_row([a, b, c])
    print(table)


def delOrder(id):
    data={
        'id':id,
        'status':25,
        'isFromUser':"true"
    }
    re=x.post(url+"/0/order_h.jsp?cmd=setStatus",headers=head,data=data)
    # print(re.json())
    return re.json()['success']


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
    getOrder(head)




    while True:
        a=input("输入要删除的订单：")
        if delOrder(a):
            print("删除成功")
            getOrder(head)
        else:
            print("删除失败，请重试")
            getOrder(head)



