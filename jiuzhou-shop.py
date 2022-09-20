import json
import time
import datetime

import requests


name="test"
tel="15310025888"
idnumber="500231200206355433"
goodsId=101121793149084
# goodsId=101122236149084 #九价
buy_time = "2022-09-09 11:27:00000000"
url = "https://xapi.weimob.com/api3/mall/trade"
token='a7342f027a112bae508c98cc0c52663dac094da5f51f61ac351c803640088ff7886800b3409b609b2a8f7dc7e9d58270'
header = {
    'Host': 'xapi.weimob.com',
    'content-length': '827',
    'weimob-bosid': '4020451669084',
    'charset': 'utf-8',
    'x-cmssdk-vidticket': '5504-1662905848.060-saas-w1-1128-55646148254',
    'cookie': 'rprm_cuid=2657269197ka15brvamg',
    'weimob-pid': 'N/A',
    'user-agent': 'Mozilla/5.0 (Linux; Android 12; M2006J10C Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/3972 MicroMessenger/8.0.27.2220(0x28001B37) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android',
    'accept-encoding': 'gzip,compress,br,deflate',
    'x-wx-token': token,
    'x-cms-sdk-request': '1.1.447',
    'x-component-is': 'ec_order/order__create',
    'wos-x-channel': '0:TITAN',
    'content-type': 'application/json',
    'x-page-route': 'ec_order/order__create',
    'referer': 'https://servicewechat.com/wx4005c81fa92cf8d9/25/page-frame.html'
}


def getskuId(goodsId):
    data = {"appid": "wx4005c81fa92cf8d9",
            "basicInfo": {"vid": 6015163145084, "vidType": 2, "bosId": 4020451669084, "productId": 145,
                          "productInstanceId": 1809820084, "productVersionId": "14010", "merchantId": 2000043390084,
                          "tcode": "weimob", "cid": 148482084},
            "extendInfo": {"refer": "ec-goods-detail", "wxTemplateId": 6257,
                           "childTemplateIds": [{"customId": 90004, "version": "crm@0.0.106"},
                                                {"customId": 90002, "version": "ec@0.5.31"},
                                                {"customId": 90006, "version": "hudong@0.0.119"},
                                                {"customId": 90008, "version": "cms@0.0.128"}],
                           "youshu": {"enable": 'false'},
                           "bosTemplateId": 1000000482, "source": 1, "channelsource": 5, "mpScene": 1089,
                           "deviceInfo": {"osType": 0}},
            "queryParameter": {"bizCode": "", "goodsId": goodsId, "activityId": 1033900, "activityType": 5,
                               "extParameter": {}}, "pid": "", "storeId": "", "bizVid": 6015163145084,
            "openid": "ouoie5SEw2p6eEOyWDWasXgXWlzI", "templateId": 4}


    re = requests.post("https://xapi.weimob.com/api3/mall/navigation/goods/v3/skuInfo", headers=header,
                       data=json.dumps(data))
    print("####getskuId####")
    print(re.json())
    return re.json()['data']['skuValueVos'][0]['id']


def getPreSubmitOrderResponse(confirmOrderKey):
    data = {
        "appid": "wx4005c81fa92cf8d9",
        "basicInfo": {
            "vid": 6015163145084,
            "vidType": 2,
            "bosId": 4020451669084,
            "productId": 145,
            "productInstanceId": 1809820084,
            "productVersionId": "14010",
            "merchantId": 2000043390084,
            "tcode": "weimob", "cid": 148482084
        },
        "extendInfo": {
            "refer": "ec-order-create",
            "wxTemplateId": 6257,
            "childTemplateIds": [
                {
                    "customId": 90004,
                    "version": "crm@0.0.106"
                },
                {"customId": 90002, "version": "ec@0.5.31"},
                {"customId": 90006, "version": "hudong@0.0.119"},
                {"customId": 90008, "version": "cms@0.0.128"}],
            "youshu": {
                "enable": "false"
            },
            "bosTemplateId": 1000000482,
            "source": 1,
            "channelsource": 5,
            "mpScene": 1089,
            "deviceInfo": {"osType": 0}}, "queryParameter": 'null', "pid": "", "storeId": "",
        "confirmOrderKey": confirmOrderKey, "channel": 1, "channelId": 10001,
        "channelScene": 1089,
        "$level": 1, "openid": "ouoie5SEw2p6eEOyWDWasXgXWlzI", "templateId": 4}
    re = requests.post(url + "/confirm/getPreSubmitOrderResponse", headers=header, data=json.dumps(data))
    print("####getPreSubmitOrderResponse####")
    print(re.json())


def initConfirmOrder(goodsId,skuId):
    data = {"appid": "wx4005c81fa92cf8d9",
            "basicInfo": {"vid": 6015163145084, "vidType": 2, "bosId": 4020451669084, "productId": 145,
                          "productInstanceId": 1809820084, "productVersionId": "14010", "merchantId": 2000043390084,
                          "tcode": "weimob", "cid": 148482084},
            "extendInfo": {"refer": "ec-goods-detail", "wxTemplateId": 6257,
                           "childTemplateIds": [{"customId": 90004, "version": "crm@0.0.106"},
                                                {"customId": 90002, "version": "ec@0.5.31"},
                                                {"customId": 90006, "version": "hudong@0.0.119"},
                                                {"customId": 90008, "version": "cms@0.0.128"}],
                           "youshu": {"enable": 'false'}, "bosTemplateId": 1000000482, "source": 1, "channelsource": 5,
                           "mpScene": 1089, "deviceInfo": {"osType": 0}}, "queryParameter": 'null', "pid": "",
            "storeId": "", "channelScene": 1089, "goodsList": [
            {"bosId": 4020451669084, "vid": 6015163145084, "goodsId": goodsId, "skuId": skuId,
             "buyNum": 1, "inputDiscount": [], "goodsAbility": {},
             "labelList": [{"labelType": "scene_xcx", "attachment": {}, "attachId": 1089}]}], "channelType": 1,
            "orderPageSource": 1, "bizCode": "", "openid": "ouoie5SEw2p6eEOyWDWasXgXWlzI", "templateId": 4}
    re = requests.post(url + "/confirm/initConfirmOrder", headers=header, data=json.dumps(data))
    print("####initConfirmOrder####")
    print(re.json())

    return re.json()


def commitOrder(confirmOrderKey, tradeTrackId):
    data = {"appid": "wx4005c81fa92cf8d9",
            "basicInfo": {"vid": 6015163145084, "vidType": 2, "bosId": 4020451669084, "productId": 145,
                          "productInstanceId": 1809820084, "productVersionId": "14010", "merchantId": 2000043390084,
                          "tcode": "weimob", "cid": 148482084},
            "extendInfo": {"refer": "ec-order-create", "wxTemplateId": 6257,
                           "childTemplateIds": [{"customId": 90004, "version": "crm@0.0.106"},
                                                {"customId": 90002, "version": "ec@0.5.31"},
                                                {"customId": 90006, "version": "hudong@0.0.119"},
                                                {"customId": 90008, "version": "cms@0.0.128"}],
                           "youshu": {"enable": "false"}, "bosTemplateId": 1000000482, "source": 1, "channelsource": 5,
                           "mpScene": 1089, "deviceInfo": {"osType": 0}}, "queryParameter": "null", "pid": "",
            "storeId": "", "confirmOrderKey": confirmOrderKey,
            "tradeTrackId": tradeTrackId, "channelScene": 1089,
            "deliveryCustomFieldList": [{"selfPickupMobile": tel, "selfPickupUserName": name},
                                        {"affectedOrderIndexList": [20001], "orderIndex": 20001, "selfPickupTime": ""}],
            "itemMessageList": [], "customFieldListData": [{"affectedOrderIndexList": [20001], "orderIndex": 20001,
                                                            "customFieldList": [
                                                                {"componentType": "text", "key": "10000000981",
                                                                 "name": "身份证", "required": "false",
                                                                 "readOnly": "false",
                                                                 "disabled": "true", "sort": 10,
                                                                 "customOptionBaseInfo": {},
                                                                 "customFieldValidationList": [{"validType": "idCard",
                                                                                                "validRule": "(^\\d{15}$)|(^\\d{18}$)|(^\\d{17}(\\d|X|x)$)"}],
                                                                 "dimensionInfoVoList": [{"dimensionType": 1,
                                                                                          "dimensionValueList": [10002,
                                                                                                                 10001]}],
                                                                 "needSelfValidator": 'true',
                                                                 "extStyle": "padding: 12rpx 28rpx;min-height: 68rpx;margin-bottom: 12rpx;",
                                                                 "value": idnumber}]}],
            "remarkList": [{"remark": "出去耍", "orderIndex": 20001, "affectedOrderIndexList": [20001]}],
            "channelId": 10001, "openid": "ouoie5SEw2p6eEOyWDWasXgXWlzI", "templateId": 4}
    re = requests.post(url + "/settlement/commitOrder", headers=header, data=json.dumps(data))
    print("####commitOrder####")
    print(re.json())
    return re.json()



def miao():
    # 生成订单id

    skuId=getskuId(goodsId)
    if skuId:
        re=initConfirmOrder(goodsId, skuId)
        if re['errcode'] !='0':
            print("while1")
            while True:
                if initConfirmOrder(goodsId,skuId)['errcode'] ==0:
                    print("while2")
                    break
        elif re['errcode'] =='0':
            confirmOrderKey = re['data']['confirmOrderKey']
            tradeTrackId = re['data']['tradeTrackId']
            print(confirmOrderKey)
            print(tradeTrackId)
            # getPreSubmitOrderResponse(confirmOrderKey)
            result=commitOrder(confirmOrderKey, tradeTrackId)
            # print(result)
            if result['errcode']=='0':
                # print("抢购成功！")
                return True
            else:
                # print("抢购失败！")
                return False
        else:
            print("####initConfirmOrder阶段异常####")
            return False


if __name__ == '__main__':
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
            start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            time4 = time.time()
            end_time = int(round(time4 * 1000))

            print("#####################开始抢购####################")
            # break
            result = miao()
            # print(result)
            if result:
                print("###秒杀成功###")
                time3 = time.time()
                endtime = int(round(time3 * 1000))
                # print('标准时间戳:%d' % timestamp)
                # print('开始时间戳:%d' % end_time)
                # print('结束时间戳:%d' % endtime)
                # time2 = time.time()
                end = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                print('开始时间:%s' % start_time)
                print('结束时间:%s' % end)
                print("耗时：%f s" % (int(endtime - end_time) / 1000))
                # print("耗时：%d " % (end - start_time))
                break
            else:
                print("秒杀失败")
                time.sleep(0.1)
