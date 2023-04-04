# -*- coding: UTF-8 -*-
'''
@Project ：法拍 
@File ：SF_get_id.py
@Author ：hao
@Date ：2022/12/5 11:02 
'''
import sys
sys.path.append("..")
import time
from datetime import datetime
import requests
from loguru import logger
from wbh_word.spider import Get_ip
from wbh_word.manage_data import manage_mysql
from wbh_word.Dispose_data import Dispose_time
import random

'''
    url = https://sf.caa123.org.cn/pages/lots.html
    中国拍卖行业协会 下的 中拍平台 -> 司法
'''

logger.add("/home/wangdong/fp_spider/ZGPMXH_Script/logger/IDlist_get_data.log", filter=lambda record: record["extra"]["name"] == "IDlist_get_data")
# logger.add("D:/yj_pj/法拍/BLZC/FP/ZGPMXH/logger/IDlist_warning_data.log", filter=lambda record: record["extra"]["name"] == "IDlist_warning_data")
logger_get_data = logger.bind(name="IDlist_get_data")
# logger_warning_data = logger.bind(name="IDlist_warning_data")

def get_headers():
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        # 'Cookie': '__root_domain_v=.caa123.org.cn; _qddaz=QD.826467981949210; sec_tc=AQAAAKyLWVDK/AoA2hG7L+4Ip8P/Qp8I; Hm_lvt_a601ba8a951181d36d7e8543a7f59135=1669883701,1670206617; Hm_lpvt_a601ba8a951181d36d7e8543a7f59135=1670208084',
        'Referer': 'https://sf.caa123.org.cn/pages/lots.html?&province=%E5%B9%BF%E4%B8%9C%E7%9C%81&lotStatus=&canLoan=&isRestricted=&num=1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    return headers

def get_params(page):
    '''
        start -》 page 0 1 2 3 4 5 6...
        count -》 一页显示 x 个（最多20）默认为 12
        province -》 省份
    '''
    params = {
        'name': '',
        'start': str(page),
        'count': '20',
        'sortname': '',
        'sortorder': '',
        'lotStatus': '',
        'province': '广东省',
        'city': '',
        'priceBegin': '',
        'priceEnd': '',
        'lotMode': '',
        'times': '',
        'isRestricted': '',
        'canLoan': '',
        'standardType': '',
        'secondaryType': '',
        # '_': '1670209379646',
    }
    return params

headers = get_headers()
def get_response(url,params,proxies):
    try:
        response = requests.get(url=url,headers=headers,params=params,proxies=proxies,timeout=5).json()
        time.sleep(float(random.randint(200, 400)) / 1000)
    except Exception as e:
        proxies = Get_ip.ip_proxies()
        time.sleep(float(random.randint(200, 400)) / 1000)
        response,proxies = get_response(url,params,proxies)
    return response,proxies

def get_max_page(url,proxies):
    page_params = get_params(0)
    response,proxies = get_response(url,page_params,proxies)
    try:
        # 无数据时此处为 0
        max_page = int(response['totalPages'])
        return max_page,response,proxies
    except Exception as e:
        print(f"错误！！！：{e}")

def manage_response(resposne):
    '''
        standardType : 一级标签
        secondaryType : 二级标签
        name : 标的物名称
        id
        startPrice : 开始价格
        startTime : 开始时间   1670119200000
        assessPrice ： 评估价
        status_Mongo : 待存入mongo  未存入1 ，存入0
        status_Update : 待更新     待更新1 ，结束0
    '''
    table = 'wbh_ZGPM_SF_id'
    down_time = str(datetime.now())  # 首次入库时间
    update_time = str(datetime.now())  # 更新时间
    items = resposne['items']
    data_list = []
    save_num = 0
    # page_bool = True  # 是否翻页 ，， 若当前页出现数据重复，则后面数据都是重复数据，即取消翻页  page_bool -> False
    for item in items:
        item_name = item['name']
        item_id = item['id']
        standardType = item['standardType']     # 一级标签
        secondaryType = item['secondaryType']   # 二级标签
        startPrice = item['startPrice']
        startTime = int(item['startTime'])
        endTime = int(item['endTime'])
        s_time = Dispose_time.get_time_data(startTime)
        e_time = Dispose_time.get_time_data((endTime))
        assessPrice = item['assessPrice']
        nowPrice = item["nowPrice"]

        data_dict = {"item_name":item_name,"item_id":item_id,"standardType":standardType,"secondaryType":secondaryType,"startPrice":startPrice,"nowPrice":nowPrice
            ,"assessPrice":assessPrice,"s_time":s_time,"e_time":e_time,'down_time': down_time, 'update_time': update_time,"status_Mongo":1,"status_Update":1}

        return_data_list = ['item_id']      # 查询后返回的字段
        where_list = [{"item_id": item_id}]
        where_data = manage_mysql.read_where_data(table,return_data_list,where_list)
        if where_data:      # 查询数据表中是否有数据，有就退出，没有就插入
            logger_get_data.warning(f"item_name：{item_name} - item_id：{item_id} - 数据重复 跳过！")
            # print(f"item_name：{item_name} - item_id：{item_id} - 数据重复 跳过！")
            continue
        else:
            save_num += 1
            data_list.append(data_dict)

    # print(data_list)
    if data_list:
        manage_mysql.save_data(table,data_list)
        logger_get_data.info(f"存入mysql数据库成功！！{data_list}")
    else:
        logger_get_data.info("暂无数据更新")
    return save_num

def get_id_data():
    proxies = Get_ip.ip_proxies()
    url = 'https://sf.caa123.org.cn/sf-web-ws/ws/0.1/lots'
    max_page,response_one,proxies = get_max_page(url,proxies)
    all_save_num = 0
    for page in range(max_page):
        params = get_params(page)
        if page == 0:
            response = response_one
        else:
            response, proxies = get_response(url,params,proxies)
        save_num = manage_response(response)
        logger_get_data.info(f"数据获取进度进度：{page+1}/{max_page}")
        all_save_num += save_num
        # if page_bool == False:      # 数据开始重复不再进行翻页操作
        #     logger_get_data.warning("有数据重复，取消翻页直接跳出程序")
        #     break
    logger_get_data.info(f"程序运行结束共获取数据：{all_save_num} 条")

if __name__ == '__main__':
    get_id_data()



