import configparser
import os
import sys
import threading
import multiprocessing as mp
import requests

import  minghao

list=[]
def getp(k):
    # 发送给服务器的标识
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/532.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    # 代理api，，从网站后台-HTTP代理-API生成中获取
    proxyUrl = "http://http1.9vps.com/getip.asp?username=15310025854&pwd=36311740522562779b2b539691e8c384&geshi=1&fenge=1&fengefu=&Contenttype=1&getnum="+str(k)+"&setcity=&operate=all"
    # 请求代理url，获取代理ip
    outPutProxy = getProxy(proxyUrl, userAgent)
    return outPutProxy
def requestGet(url, userAgent, proxy):
    headers = {
        "User-Agent": userAgent
    }
    response = None
    if (proxy):
        # 有代理的时候走这个
        response = requests.get(url, headers=headers, timeout=5, proxies=proxy)
    else:
        # 没有代理走这个
        response = requests.get(url, headers=headers, timeout=5)
    # 设置编码，防止乱码
    # requests 库会帮我们自动分析这个网页的字符编码
    response.encoding = response.apparent_encoding
    return response.text

def getProxy(proxyUrl, userAgent):
    proxyIps = ""
    outPutProxy = []
    try:
        proxyIps = requestGet(proxyUrl, userAgent, None)
        print(proxyIps)
        # {"code":3002,"data":[],"msg":"error!用户名或密码错误","success":false}
        if "{" in proxyIps:
            raise Exception("[错误]" + proxyIps)
        outPutProxy = proxyIps.split("\n")

    except Exception as e:
        print(e)
    print("总共获取了" + str(len(outPutProxy)) + "个代理")
    return outPutProxy
# minghao.mmain()

def file_config():  # 初始化配置文件
    # global p_id
    # global buy_time
    # global tel
    # global name
    # global msg
    # global cookie
    cf = configparser.RawConfigParser()
    # cf.read("user.ini", encoding='utf-8')
    # print(cf.sections())
    # print(cf.sections())
    if (os.path.exists('user.ini')):
        try:
            cf.read("user.ini", encoding='utf-8')
            for i in cf.sections():
                list.append(cf.items(i))
        except Exception as e:
            print("配置文件错误", e)
            input('')
            sys.exit(0)
    else:
        print("user.ini配置文件不存在当前文件夹下。")
        input('')
        sys.exit(0)
# minghao.mmain(proxy=None)
if __name__ == '__main__':

    file_config()


    proxy=None

    for i in list:

        new_process = mp.Process(target=minghao.mmain, args=(proxy,i))
        new_process.start()

     
