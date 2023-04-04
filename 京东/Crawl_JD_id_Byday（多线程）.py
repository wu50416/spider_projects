# -*- coding: utf-8 -*-
import json
import time
import math
import requests
import random
import threading
from datetime import datetime, timedelta
from wbh_word.spider import Get_ip
from wbh_word.manage_data import manage_mysql
from wbh_word.manage_data.manage_redis import RedisPool
from loguru import logger

# 每日运行一次

logger.add("D:/yj_pj/法拍/BLZC/JD/logger/get_num_data.log", filter=lambda record: record["extra"]["name"] == "List_get_num_data")
logger.add("D:/yj_pj/法拍/BLZC/JD/logger/warning.log", filter=lambda record: record["extra"]["name"] == "List_warning")
logger_num_data = logger.bind(name="List_get_num_data")
logger_warning = logger.bind(name="List_warning")

table = 'wbh_JD_id'      # 存入Mysql       # 这里最终要替换为wbh_JD_id
redis_table = 'jd_fp_ids'       # redis缓存 用来判断是否已存在该数据

# ----------------多线程重写----------------------
class MyThread(threading.Thread):
    def __init__(self, func, args):
        """
        :param func: run方法中的函数名
        :param args: func函数所需的参数
        """
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        print('当前子线程:{}启动'.format(threading.current_thread().name))
        self.result = self.func(self.args)
        return self.func

    def get_result(self):  # 获取返回值
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except:
            return None




redis_pool = RedisPool()

def get_headers():
    headers = {
        'Host': 'api.m.jd.com',
        # 'Connection': 'keep-alive',
        'Connection': 'close',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'script',
        'Referer': 'https://auction.jd.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Cookie': '__jda=122270672.1657003436722516907276.1657003437.1657003437.1657003437.1; __jdc=122270672; __jdv=122270672|direct|-|none|-|1657003436723; __jdu=1657003436722516907276; areaId=19; ipLoc-djd=19-1607-0-0; __jdb=122270672.3.1657003436722516907276|1.1657003437; 3AB9D23F7A4B3C9B=KLSD5FML7GAEOJX37D5SFZ6TR5SGHX3JOKK25JBIP6X7YPE2UJZ4UA6ISM6ATVL2YO54MCNKSJ2A56U22PDBX245JA',
    }
    return headers

def get_params(page,city_id,searchCategory_id,searchLabel_id,s_time='',e_time=''):
    # searchCategory_id = '101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123'   # 标的物类型
    # searchLabel_id = '0,1027,1028,1029,1030,1039,1031,1032,1033'    # 所有性质id
    # cityId 为空时 即 所有城市
    params = {
        'appid': 'paimai',
        'functionId': 'paimai_unifiedSearch',
        'body': '{"investmentType":"","apiType":12,"page":' + str(page) + ',"pageSize":40,"keyword":"","provinceId":19,"cityId":"'+ str(city_id) +'","countyId":"","multiPaimaiStatus":"","multiDisplayStatus":"","multiPaimaiTimes":"","childrenCateId":"' + str(searchCategory_id) + '","currentPriceRangeStart":"","currentPriceRangeEnd":"","timeRangeTime":"endTime","timeRangeStart":"' + str(s_time) + '","timeRangeEnd":"' + str(e_time) + '","loan":"","purchaseRestriction":"","orgId":"","orgType":"","sortField":8,"projectType":1,"reqSource":0,"labelSet":"' + str(searchLabel_id) + '","publishSource":""}'
    }
    return params

def get_city_dict():
    '''
    return : {'广州市': 1601, '深圳市': 1607, '珠海市': 1609, '汕头市': 1611, '韶关市': 1617, '河源市': 1627, '梅州市': 1634, '惠州市': 1643, '汕尾市': 1650, '东莞市': 1655, '中山市': 1657, '江门市': 1659, '佛山市': 1666, '阳江市': 1672, '湛江市': 1677, '茂名市': 1684, '肇庆市': 1690, '云浮市': 1698, '清远市': 1704, '潮州市': 1705, '揭阳市': 1709}
    '''
    # {"cod":False,"id":1601,"name":"广州市"},{"cod":False,"id":1607,"name":"深圳市"},{"cod":False,"id":1609,"name":"珠海市"},{"cod":False,"id":1611,"name":"汕头市"},{"cod":False,"id":1617,"name":"韶关市"},{"cod":False,"id":1627,"name":"河源市"},{"cod":False,"id":1634,"name":"梅州市"},{"cod":False,"id":1643,"name":"惠州市"},{"cod":False,"id":1650,"name":"汕尾市"},{"cod":False,"id":1655,"name":"东莞市"},{"cod":False,"id":1657,"name":"中山市"},{"cod":False,"id":1659,"name":"江门市"},{"cod":False,"id":1666,"name":"佛山市"},{"cod":False,"id":1672,"name":"阳江市"},{"cod":False,"id":1677,"name":"湛江市"},{"cod":False,"id":1684,"name":"茂名市"},{"cod":False,"id":1690,"name":"肇庆市"},{"cod":False,"id":1698,"name":"云浮市"},{"cod":False,"id":1704,"name":"清远市"},{"cod":False,"id":1705,"name":"潮州市"},{"cod":False,"id":1709,"name":"揭阳市"}
    # GD_city = [{"cod":False,"id":1601,"name":"广州市"},{"cod":False,"id":1607,"name":"深圳市"},{"cod":False,"id":1609,"name":"珠海市"},{"cod":False,"id":1611,"name":"汕头市"},{"cod":False,"id":1617,"name":"韶关市"},{"cod":False,"id":1627,"name":"河源市"},{"cod":False,"id":1634,"name":"梅州市"},{"cod":False,"id":1643,"name":"惠州市"},{"cod":False,"id":1650,"name":"汕尾市"},{"cod":False,"id":1655,"name":"东莞市"},{"cod":False,"id":1657,"name":"中山市"},{"cod":False,"id":1659,"name":"江门市"},{"cod":False,"id":1666,"name":"佛山市"},{"cod":False,"id":1672,"name":"阳江市"},{"cod":False,"id":1677,"name":"湛江市"},{"cod":False,"id":1684,"name":"茂名市"},{"cod":False,"id":1690,"name":"肇庆市"},{"cod":False,"id":1698,"name":"云浮市"},{"cod":False,"id":1704,"name":"清远市"},{"cod":False,"id":1705,"name":"潮州市"},{"cod":False,"id":1709,"name":"揭阳市"}]
    # city_dict = {}
    # for city in GD_city:
    #     city_name = city['name']
    #     city_id = city['id']
    #     city_dict[city_name] = city_id
    city_dict = {'广州市': 1601, '深圳市': 1607, '珠海市': 1609, '汕头市': 1611, '韶关市': 1617, '河源市': 1627, '梅州市': 1634, '惠州市': 1643, '汕尾市': 1650, '东莞市': 1655, '中山市': 1657, '江门市': 1659, '佛山市': 1666, '阳江市': 1672, '湛江市': 1677, '茂名市': 1684, '肇庆市': 1690, '云浮市': 1698, '清远市': 1704, '潮州市': 1705, '揭阳市': 1709}

    return city_dict

def get_searchLabel_dict():
    # 资产性质：   return : {'诉讼资产': 1027, '刑案资产': 1028, '破产资产': 1029, '海关罚没': 1030, '政府罚没': 1039, '国有资产': 1031, '商业资产': 1032, '金融资产': 1033}
    # searchLabel = {"labelId": 1027, "labelName": "诉讼资产"}, {"labelId": 1028, "labelName": "刑案资产"}, {"labelId": 1029,"labelName": "破产资产"}, {"labelId": 1030, "labelName": "海关罚没"}, {"labelId": 1039, "labelName": "政府罚没"}, {"labelId": 1031,"labelName": "国有资产"}, {"labelId": 1032, "labelName": "商业资产"}, {"labelId": 1033, "labelName": "金融资产"}
    # searchLabel_dict = {}
    # for publicSearchLabel in searchLabel:
    #     publicSearchLabel_name = publicSearchLabel['labelName']
    #     publicSearchLabel_id = publicSearchLabel['labelId']
    #     searchLabel_dict[publicSearchLabel_name] = publicSearchLabel_id
    searchLabel_dict = {'诉讼资产': 1027, '刑案资产': 1028, '破产资产': 1029, '海关罚没': 1030, '政府罚没': 1039, '国有资产': 1031, '商业资产': 1032, '金融资产': 1033}
    return searchLabel_dict

def get_searchCategory_dict():
    # 标的物类型：
    searchCategory_dict = {'住宅用房': 101, '商业用房': 102, '工业用房': 103, '其他用房': 104, '机动车': 105, '船舶': 106, '其他交通运输工具': 107,'股权': 108, '债权': 109, '矿权': 110, '林权': 111, '土地': 112, '工程': 113, '机械设备': 114, '无形资产': 115,'知识产权': 116, '租赁/经营权': 117, '奢侈品': 118, '生活物资': 119, '工业物资': 120, '库存物资': 121, '打包处置': 122,'其他财产': 123}
    return searchCategory_dict

def get_auctionStatus_name(auctionStatus_id):
    auctionStatus_dict = {0:'预告',1:'进行中',2:'已结束'}
    auctionStatus_name = auctionStatus_dict[auctionStatus_id]
    return auctionStatus_name

def get_displayStatus_name(displayStatus_id):
    displayStatus_dict = {1:'无异常',7:'已中止',5:'已撤回',6:'已暂缓'}
    displayStatus_name = displayStatus_dict[displayStatus_id]
    return displayStatus_name

def get_paimaiTimes_name(paimaiTimes_id):
    paimaiTimes_dict = {0:'无',1:'一拍',2:'二拍',4:'变卖',6:'破产'}
    paimaiTimes_name = paimaiTimes_dict[paimaiTimes_id]
    return paimaiTimes_name


def get_maxpage(proxies,params_page,headers):
    try:
        response_js = requests.get('https://api.m.jd.com/api', params=params_page,headers=headers,proxies=proxies,timeout=(3,5)).json()
        total = response_js['totalItem']
        allpage = int(math.ceil(total / 40))        # 向上取整
        # print('总数：{}，总页数：{}'.format(total, allpage))
        time.sleep(float(random.randint(200, 400)) / 1000)
    except Exception as e:
        proxies = Get_ip.ip_proxies()
        allpage,proxies = get_maxpage(proxies,params_page,headers)
    return allpage,proxies


def get_list_response(proxies,params_getdata,headers):
    try:
        # with eventlet.Timeout(10, False):        # 连接超时
        response = requests.get('https://api.m.jd.com/api', params=params_getdata,headers=headers,proxies=proxies,timeout=(3,5)).json()
        time.sleep(float(random.randint(200, 350)) / 1000)
    except Exception as e:
        if 'timed out' not in str(e):
            logger_warning.warning(f'线程：{threading.current_thread().getName()}--当前页错误！！！更换ip，重新访问当前页，错误为：{e}')
        proxies = Get_ip.ip_proxies()
        response,proxies = get_list_response(proxies,params_getdata,headers)

    return response,proxies



def save_response(city_dict,response,page,max_page,searchLabel_Name,searchCategory_Name):
    '''
        title：标题
        shopName: 拍卖方
        marketPriceCN： 评估价
        currentPriceCN： 当前价
        productAddress： 标的物地址
        auctionStatus: 拍卖物状态
        displayStatus: 异常状态
        paimaiTimes: 拍卖次数
        status: 是否入库（mongo）
    '''

    items = response['datas']


    data_list = []
    # city_dict = get_city_dict()     # 得到标的物地址后，获取id
    searchLabel_id = searchLabel_dict[searchLabel_Name]
    searchCategory_id = searchCategory_dict[searchCategory_Name]

    down_time = str(datetime.now())  # 首次入库时间
    update_time = str(datetime.now())  # 更新时间

    for item in items:
        item_id = item['id']
        shopName = item['shopName']     # 拍卖方
        title = item['title']           # 标题名称
        city_Name = item['city']        # 城市名称
        city_id = city_dict[city_Name]

        auctionStatus_id = int(item['auctionStatus'])       # 预告0/进行中1/已结束2 id
        auctionStatus_name = get_auctionStatus_name(auctionStatus_id)
        displayStatus_id = int(item['displayStatus'])       # 无异常：1 已终止：7 已撤回：5 已暂缓：6
        displayStatus_name = get_displayStatus_name(displayStatus_id)
        # paimaiTimes_id = int(item['paimaiTimes'])           # {1:'一拍',2:'二拍',4:'变卖'}

        paimaiTimes_id = item.get('paimaiTimes', 0)


        paimaiTimes_name = get_paimaiTimes_name(paimaiTimes_id)

        try:
            marketPriceCN = item['assessmentPriceStr'].replace(',', '')  # 评估价
        except:
            marketPriceCN = item['currentPriceStr'].replace(',', '')  # 评估价
        currentPriceCN = item['currentPriceStr'].replace(',', '')  # 当前价        # 后期用当前价搜索！！！！
        # productAddress = item['productAddress']
        productAddress = item.get('productAddress',title)       # 没有地址就改成名称


        startTimes = item['startTime'] / 1000
        endTimes = item['endTime'] / 1000
        startTimes1 = time.localtime(startTimes)
        endTimes1 = time.localtime(endTimes)
        startTime = time.strftime("%Y-%m-%d %H:%M:%S", startTimes1)
        endTime = time.strftime("%Y-%m-%d %H:%M:%S", endTimes1)



        data_dict = {'city_Name':city_Name,'city_id':city_id,'searchLabel_Name':searchLabel_Name,'searchLabel_id':searchLabel_id,'searchCategory_Name':searchCategory_Name
            ,'searchCategory_id':searchCategory_id,'s_time':startTime,'e_time':endTime, 'title': title,'item_id': item_id,'auctionStatus':auctionStatus_name,'auctionStatus_id':auctionStatus_id
            ,'displayStatus':displayStatus_name,'displayStatus_id':displayStatus_id,'paimaiTimes':paimaiTimes_name,'paimaiTimes_id':paimaiTimes_id, 'shopName': shopName
            ,'marketPriceCN': marketPriceCN,'currentPriceCN': currentPriceCN,'productAddress':productAddress,'down_time':down_time,'update_time':update_time
            ,'status_Mongo':1,'status_Update':1}
        # {'city_Name': '广州市', 'city_id': 1601, 'searchLabel_Name': '诉讼资产', 'searchLabel_id': 1027, 'searchCategory_Name': '住宅用房', 'searchCategory_id': 101, 's_time': '2022-11-24 16:00:00', 'e_time': '2022-11-25 17:58:26', 'title': '广州市花都区新华街镜湖大道16号18栋303房产', 'id': 292142186, 'auctionStatus': '进行中', 'auctionStatus_id': 1, 'displayStatus': '无异常', 'displayStatus_id': 1, 'paimaiTimes': '变卖', 'paimaiTimes_id': 4, 'shopName': '广州市白云区人民法院', 'marketPriceCN': '2870761.00', 'currentPriceCN': '2066947.92', 'productAddress': '花都区新华街镜湖大道16号18栋303房', 'status_Mongo': 0}


        if redis_pool.redis_sismember(redis_table, item_id):           # 读取判断是否存在
            continue        # 有重复数据
        else:
            logger_num_data.info(f"item_id:{item_id},title: {title},'city_Name': {city_Name},searchLabel_Name: {searchLabel_Name},searchCategory_Name: {searchCategory_Name}")
            data_list.append(data_dict)
            redis_pool.redis_sadd(redis_table, item_id)     # 保存
    # print(data_list)
    if data_list:
        manage_mysql.save_data(table,data_list)


headers = get_headers()
def get_total_response(city_dict,city_Name,searchCategory_Name,searchLabel_Name,s_time,e_time,proxies):
    '''
    请求列表页获取id等
    city_id ： 城市id
    city_Name ： 城市名称
    searchLabel_id ： 性质id
    searchLabel_Name ： 资产性质名称
    searchCategory_id ： 类型id
    searchCategory_Name ： 类型名称
    '''
    ip_usenum = 0

    city_id = city_dict[city_Name]
    searchLabel_id = searchLabel_dict[searchLabel_Name]
    searchCategory_id = searchCategory_dict[searchCategory_Name]

    params_page = get_params(1,city_id, searchCategory_id, searchLabel_id,s_time,e_time)      # 请求第一页，获取页数信息
    max_page,proxies = get_maxpage(proxies,params_page,headers)
    ip_usenum += 1

    logger_num_data.info(f'线程：{threading.current_thread().getName()}-时间：{s_time}~~~{e_time} --- 城市名称:{city_Name},资产性质名称:{searchLabel_Name},类型名称:{searchCategory_Name},共有：{max_page}页数据，')

    if max_page>250:
        logger_warning.error(f'线程：{threading.current_thread().getName()}-- 城市名称:{city_Name},资产性质名称:{searchLabel_Name},类型名称:{searchCategory_Name},共有：{max_page}页数据')

    for page in range(1,max_page+1):        # 不会出现超过250页
        if ip_usenum > 20:      # 判断ip
            proxies = Get_ip.ip_proxies()
            ip_usenum = 0
        ip_usenum += 1
        params_getdata = get_params(page,city_id, searchCategory_id, searchLabel_id,s_time,e_time)
        list_response,proxies = get_list_response(proxies,params_getdata,headers)
        # print('list_response:   ',list_response)
        save_response(city_dict,list_response,page,max_page,searchLabel_Name,searchCategory_Name)
    return proxies

def get_id_list(city_dict):
    print(city_dict)

    now_time = datetime.now()
    t1 = datetime(now_time.year,now_time.month,now_time.day)
    s_time = str(t1 - timedelta(days=1))[:10]     # 当日的前一天
    e_time = str(t1 + timedelta(days=1))[:10]     # 当日的后一天（共三天）


    # s_time = datetime(2022,11,8)
    # e_time = datetime(2022,11,29)

    proxies = Get_ip.ip_proxies()       # 初始化ip
    for city in city_dict:  # 城市
        city_Name = city
        # city_id = city_dict[city]  # 城市id
        for searchLabel in searchLabel_dict:      # 资产性质
            searchLabel_Name = searchLabel       # 资产性质名称
            # searchLabel_id = searchLabel_dict[searchLabel]   # 该资产性质的id
            for searchCategory in searchCategory_dict:
                searchCategory_Name = searchCategory  # 类型名称
                # searchCategory_id = searchCategory_dict[searchCategory]  # 类型id

                proxies = get_total_response(city_dict,city_Name,searchCategory_Name,searchLabel_Name,s_time,e_time,proxies)      # 更新ip

    logger_num_data.info(f'线程：{threading.current_thread().getName()} --- 运行结束！！！')

if __name__ == '__main__':

    # {'广州市': 1601, '深圳市': 1607, '珠海市': 1609, '汕头市': 1611, '韶关市': 1617, '河源市': 1627, '梅州市': 1634, '惠州市': 1643, '汕尾市': 1650, '东莞市': 1655, '中山市': 1657, '江门市': 1659, '佛山市': 1666, '阳江市': 1672, '湛江市': 1677, '茂名市': 1684, '肇庆市': 1690, '云浮市': 1698, '清远市': 1704, '潮州市': 1705, '揭阳市': 1709}

    city_dict_list = [{'广州市': 1601, '深圳市': 1607, '珠海市': 1609, '汕头市': 1611},
                      {'韶关市': 1617, '河源市': 1627, '梅州市': 1634, '惠州市': 1643},
                      {'汕尾市': 1650, '东莞市': 1655, '中山市': 1657, '江门市': 1659},
                      {'佛山市': 1666, '阳江市': 1672, '湛江市': 1677, '茂名市': 1684},
                      {'肇庆市': 1690, '云浮市': 1698, '清远市': 1704, '潮州市': 1705, '揭阳市': 1709}]

    # city_dict_list = [{'汕尾市': 1650,'东莞市': 1655},
    #                   {'潮州市': 1705, '揭阳市': 1709}]
    # city_dict_list = [{'东莞市': 1655}]

    # city_dict = get_city_dict()
    searchLabel_dict = get_searchLabel_dict()  # 资产性质
    searchCategory_dict = get_searchCategory_dict()  # 标的物类型
    # get_id_list(city_dict)

    thread_list = []
    for city_dict in city_dict_list:
        t = MyThread(func=get_id_list, args=city_dict)
        thread_list.append(t)
    for t in thread_list:       # 批量启动线程
        t.start()
    for t in thread_list:       # 主线程等待子线程
        t.join()
    logger_warning.info("所有进程运行结束！！！")




