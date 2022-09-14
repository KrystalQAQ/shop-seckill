import configparser
import os
import sys

import requests
from prettytable import PrettyTable

# import only system from os
from os import system, name

# import sleep to show output for some time period
from time import sleep

x = requests.Session()  # 实例化requests.Session对象
url = "https://wx7.jzapp.fkw.com/28359275"
productNameList = []
orderStausNameList = []
idList = []
productList = []


def clear():
    # for windows
    # print(name)
    # if name == 'nt':
    _ = system('cls')


# for mac and linux(here, os.name is 'posix')
# else:
#     _ = system('clear')

# print out some text


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
    idList = []
    productNameList = []
    orderStausNameList = []
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
        a = idList[i]
        b = productNameList[i]
        c = orderStausNameList[i]
        table.add_row([a, b, c])
    print(table)


def delOrder(id):
    data = {
        'id': id,
        'status': 25,
        'isFromUser': "true"
    }
    re = x.post(url + "/0/order_h.jsp?cmd=setStatus", headers=head, data=data)
    # print(re.json())
    return re.json()['success']


def getProduct(head, pid):
    data = {
        'pid': pid,
        'isFromPd': 'true',
        'isFromCart': 'false'
    }
    re = x.post(url + "/0/api/guest/product/getProductPageBasicInfo?", headers=head, data=data)
    # print(re.json()['pinfo'])
    # print(re.json()['pinfo']['sales'])
    # print(re.json()['pinfo']['productTimedAddTimeStr'])
    return re.json()['pinfo']


def allproduct(head, num):
    data = {
        'sortName': 'createTime',
        'isDesc': 'false',
        'pageNo': 0,
        'keywords': '',
        'libId': 0,
        'propValueInfo': {},
        'selfTakeId': 0,
        'merchantId': 0,
        'groupid': num,
        'addrInfo': {"prc": "", "cic": "", "coc": ""},
        'isWxApp': 'true'

    }
    re = x.post('https://wx7.jzapp.fkw.com/28359275/0/wxmallapp_h.jsp?cmd=getProductFilterPage', headers=head,
                data=data)
    # print(re.json()['rtData']['productList'])
    productList = re.json()['rtData']['productList']
    return productList
    # for i in re.json()['rtData']['productList']:
    #     print(i)


def showproduct(productList, head):
    table = PrettyTable(['ID', '产品', '销量', "时间"])
    for i in productList:
        a = i['id']
        b = i['name']
        c = i['sales']
        d = getProduct(head, i['id'])['productTimedAddTimeStr1']
        table.add_row([a, b, c, d])
    # table.align["时间"] = 'r'
    # table.align["产品"] = 'r'
    # table.align["销量"] = 'l'
    # table.set_style(pt.RANDOM)
    # table.align["时间"] = 'l'
    table.padding_width = 1
    # table.align["销量"] = 'l'
    # table.align["值"] = 'l'
    print(table)

def person(head):


    data={
        'cmd' : 'getMemberProp'
    }
    re = x.post('https://wx7.jzapp.fkw.com/28359275/0/wxmallapp_h.jsp?cmd=getMemberProp', headers=head,data=data)
    # print(re.json()['rtData']['memberInfo'])
    return re.json()['rtData']['memberInfo']




def sort(head):
    data = {
        'cmd': 'getModuleDataFromColV2',
        'colId': 301,
        # 'addrInfo': {"prc": "", "cic": "", "coc": ""},
        # 'merchantId': 0,
        # 'lat': '',
        # 'lng': '',
        # 'selfTakeId': 0
    }
    re = x.get("https://wx7.jzapp.fkw.com/28359275/0/wxmallapp_h.jsp?cmd=getModuleDataFromColV2&colId=301&lng=&lat=&addrInfo={%22prc%22:%22%22,%22cic%22:%22%22,%22coc%22:%22%22}&merchantId=0&selfTakeId=0", headers=head, data=data)
    return re.json()['moduleList'][0]['content']['pcl']


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
    # getOrder(head)
    #
    # while True:
    #     a = input("输入要删除的订单：")
    #     if delOrder(a):
    #         print("删除成功")
    #         getOrder(head)
    #     else:
    #         print("删除失败，请重试")
    #         getOrder(head)
    # getProduct(head,19)
    # productList=allproduct(head,1)
    # showproduct(productList,head)

    person(head)
        # c=allproduct(head, i['ci'])
    while True:
        clear()
        table = PrettyTable(['重庆明好医院后台系统'])
        table.add_row(["0.个人信息"])
        table.add_row(["1.疫苗查询"])
        table.add_row(["2.分类查询"])
        table.add_row(["3.订单管理"])

        table.padding_width = 10
        print(table)
        a=input("输入选项：")
        if (a=="0"):
            clear()
            p=person(head)
            n=getProduct(head,p_id)['name']
            table = PrettyTable(['ID', '名称','姓名','电话','身份证号码','秒杀商品','抢购时间'])
            table.add_row([p['id'], p['name'],name,tel,msg,n,buy_time[0:19]])
            print(table)

            input("回车返回")
        if(a=='1'):
            clear()
            c = allproduct(head, 1)
            showproduct(c, head)
            p_id=input("输入你要秒杀的id：")
            conf = configparser.ConfigParser()
            conf.read("user.ini", encoding='utf-8')
            conf.set("user", "p_id", p_id)
            conf.write(open('user.ini', "w", encoding='utf8'))
            input("回车退出")
            clear()

        if(a=='2'):

            b = sort(head)

            table = PrettyTable(['ID', '产品'])
            for i in b:
                # print(i)

                table.add_row([i['ci'], i['cn']])
            print(table)
            q = input("输入要查询的ID：")
            clear()
            list = allproduct(head, q)
            showproduct(list, head)
            input("回车返回上一级")

        if(a=='3'):
            clear()
            while True:
                getOrder(head)
                b = input("输入你要删除的订单：")
                c = delOrder(b)
                if c:
                    print("删除成功")
                    break
                else:
                    # print("重试")
                    input("删除失败，按任意键请重试")
                    break
                    clear()
    input("任意键返回")
