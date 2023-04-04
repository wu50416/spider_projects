# -*- coding: UTF-8 -*-
'''
@Project ：法拍 
@File ：SF_get_detail.py
@Author ：hao
@Date ：2022/12/5 15:47 
'''
import sys
sys.path.append("..")
import random
import time
import requests
from datetime import datetime
from loguru import logger
from wbh_word.manage_data import manage_mongo
from wbh_word.manage_data import manage_mysql
from wbh_word.Dispose_data import Dispose_time
from wbh_word.spider import Get_ip


'''
    基础数据：https://sf.caa123.org.cn/sf-web-ws/ws/0.1/lot/8246?_=1670211105060
    拍品介绍：在基础数据响应中的 remark 键中
    拍卖公告：https://sf.caa123.org.cn/sf-web-ws/ws/0.1/notice/lot/8246?_=1670211105057
    公告附件：https://sf.caa123.org.cn/sf-web-ws/ws/0.1/goods/lot/8246?_=1670211105059
    竞买须知：https://sf.caa123.org.cn/sf-web-ws/ws/0.1/instruction/lot/8246?_=1670211105058
    竞价记录：https://sf.caa123.org.cn/sf-web-ws/ws/0.1/records/lot/8246?start=0&count=10&_=1670211105056
    成交确认书：https://sf.caa123.org.cn/sf-web-ws/ws/0.1/deal/lot/8246?_=1670211105063
    
    状态码：lotStatus
    即将开始：lotStatus: "0"
    正在进行：lotStatus: "1"
    已流拍：lotStatus: "2"
    已成交：lotStatus: "3"
    已终止：lotStatus: "4"
    已撤回：lotStatus: "5"
'''

MySql_table = 'wbh_ZGPM_SF_id'
Mongo_table = 'wbh_ZGPM_SF_detail'

logger.add("/home/wangdong/fp_spider/ZGPMXH_Script/logger/Detail_get_data.log", filter=lambda record: record["extra"]["name"] == "Detail_get_data")
# logger.add("D:/yj_pj/法拍/BLZC/FP/ZGPMXH/logger/IDlist_warning_data.log", filter=lambda record: record["extra"]["name"] == "IDlist_warning_data")
logger_get_data = logger.bind(name="Detail_get_data")
# logger_warning_data = logger.bind(name="IDlist_warning_data")

def get_headers():
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': '__root_domain_v=.caa123.org.cn; _qddaz=QD.826467981949210; Hm_lvt_a601ba8a951181d36d7e8543a7f59135=1669883701,1670206617,1670222091; sec_tc=AQAAAE7S6CWhLAAA2hG7L/B2+U7+wGJv; Hm_lpvt_a601ba8a951181d36d7e8543a7f59135=1670224864',
        'Referer': 'https://sf.caa123.org.cn/pages/lotdetail.html?lotId=10978',
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

def get_id_list():
    # [('11045', '广东省清新县（现为清远市清新区）太和镇八号区一宗土地使用权及地下室', '房产', '住宅用房'), ('8359', '广州市荔湾区文昌南路137号之一地下2层288A车位', '房产', '其他用房')]
    return_list = ['item_id','item_name','standardType','secondaryType','status_Mongo','status_Update']  # 查询后返回的字段
    where_list = [{"status_Update": 1}]         # 查询需要更新的数据  备注：status_Mongo为1时 ， status_Update 一定也为1
    data_list = manage_mysql.read_where_data(MySql_table,return_list,where_list)
    # print(data_list)
    return data_list

def get_url(key_word,item_id):
    # 拍品介绍：在基础数据响应中的 remark 键中
    url_dict = {
        'lot' : f'https://sf.caa123.org.cn/sf-web-ws/ws/0.1/lot/{item_id}?',                # 基础数据  (注意！！拍品介绍包含在基础数据 remark 中！！！)
        'notice' : f'https://sf.caa123.org.cn/sf-web-ws/ws/0.1/notice/lot/{item_id}?',      # 拍卖公告
        'goods' : f'https://sf.caa123.org.cn/sf-web-ws/ws/0.1/goods/lot/{item_id}?',        # 公告附件
        'instruction' : f'https://sf.caa123.org.cn/sf-web-ws/ws/0.1/instruction/lot/{item_id}?',        # 竞买须知
        'records' : f'https://sf.caa123.org.cn/sf-web-ws/ws/0.1/records/lot/{item_id}?start=0&count=10',    # 竞价记录  重第一个读取前十个
        'deal' : f'https://sf.caa123.org.cn/sf-web-ws/ws/0.1/deal/lot/{item_id}?',      # 成交确认书
    }
    url = url_dict[key_word]
    return url


headers = get_headers()
def get_response(url,proxies):
    try:
        response = requests.get(url=url,headers=headers,proxies=proxies,timeout=5).json()
    except Exception as e:
        proxies = Get_ip.ip_proxies()
        time.sleep(float(random.randint(200, 400)) / 1000)
        response,proxies = get_response(url,proxies)
    return response,proxies

def manage_lot_response(lot_response):      # 当前状态
    '''
        {0:"即将开始",1:"正在进行",2:"已流拍",3:"已成交",4:"已终止",5:"已撤回"}
        即将开始：lotStatus: "0"
        正在进行：lotStatus: "1"
        已流拍：lotStatus: "2"
        已成交：lotStatus: "3"
        已终止：lotStatus: "4"
        已撤回：lotStatus: "5"
        已暂缓：lotStatus: "6"
    '''
    nowPrice = float(lot_response['nowPrice'])
    lotStatus_id = int(lot_response['lotStatus'])       # 获取状态码   当有0 / 1 时 ，数据需要更新
    endTimes = int(lot_response['endTime'])
    e_time = Dispose_time.get_time_data(endTimes)

    status_dict = {0:"即将开始",1:"正在进行",2:"已流拍",3:"已成交",4:"已终止",5:"已撤回",6:"已暂缓"}
    lotStatus_name = status_dict[lotStatus_id]

    if lotStatus_id == 0 or lotStatus_id == 1:
        end_bool = False       # 当为False时，未结束，需要更新
    else:
        end_bool = True

    return nowPrice,lotStatus_id,lotStatus_name,e_time,end_bool

def get_detail_data(data_list):
    '''
    基础数据：lot
    拍品介绍：在基础数据响应中的 remark 键中
    拍卖公告：notice
    公告附件：goods
    竞买须知：instruction
    竞价记录：records
    成交确认书：deal
    '''
    proxies = Get_ip.ip_proxies()
    index = 0
    ip_usenum = 0
    for data in data_list:
        index += 1
        if ip_usenum>10:
            proxies = Get_ip.ip_proxies()
            ip_usenum = 0
        ip_usenum += 1
        down_time = str(datetime.now())         # 首次入库时间
        update_time = str(datetime.now())       # 更新时间
        item_id = data[0]
        item_name = data[1]
        standardType = data[2]
        secondaryType = data[3]
        status_Mongo = int(data[4])
        status_Update = int(data[5])


        lot_url = get_url("lot",item_id)
        notice_url = get_url("notice", item_id)
        goods_url = get_url("goods", item_id)
        instruction_url = get_url("instruction", item_id)
        records_url = get_url("records", item_id)
        deal_url = get_url("deal", item_id)


        lot_response,proxies = get_response(lot_url,proxies)        # 基础数据 + 拍卖物介绍

        nowPrice,lotStatus_id,lotStatus_name,e_time,end_bool = manage_lot_response(lot_response)

        if end_bool:            # 为True时，已结束 不再需要更新
            sql_updata_list = [{"nowPrice":nowPrice,"status_Mongo": '0', 'status_Update': '0',"update_time":update_time,'e_time':e_time}]  # 结束，不需要再更新
        else:
            sql_updata_list = [{"nowPrice":nowPrice,"status_Mongo": '0',"update_time":update_time}]  # 未结束 但入库，此时 status_Update = 1


        if status_Mongo == 1 and status_Update == 1:  # 需要入库
            notice_response, proxies = get_response(notice_url, proxies)            # 拍卖公告
            goods_response, proxies = get_response(goods_url, proxies)              # 公告附件
            instruction_response, proxies = get_response(instruction_url, proxies)  # 竞买须知
            records_response, proxies = get_response(records_url, proxies)          # 竞价记录
            deal_response, proxies = get_response(deal_url, proxies)                # 成交确认书

            mongo_save_dict = {"item_id":item_id,"item_name":item_name,"standardType":standardType,"secondaryType":secondaryType,"lot_response":lot_response
                ,"lotStatus_name":lotStatus_name,"lotStatus_id":lotStatus_id,"notice_response":notice_response,"goods_response":goods_response
                ,"instruction_response":instruction_response,"records_response":records_response,"deal_response":deal_response
                ,"down_time":down_time,"update_time":update_time}
            manage_mongo.save_mongodb_data(Mongo_table, mongo_save_dict)
            logger_get_data.info(f'item_id:{item_id} 入库mongo成功！！当前进度：{index}/{len(data_list)}')

        elif status_Mongo == 0 and status_Update == 1:  # 已入库,但需要更新
            records_response, proxies = get_response(records_url, proxies)  # 竞价记录
            deal_response, proxies = get_response(deal_url, proxies)  # 成交确认书
            # 基础数据及拍卖物介绍 + 竞价记录 + 成交确认书
            mongo_update_dict ={"lot_response":lot_response,"lotStatus_name":lotStatus_name,"lotStatus_id":lotStatus_id,"records_response":records_response
                ,"deal_response":deal_response,"update_time":update_time}
            mongo_where_dict = {"item_id":item_id}
            manage_mongo.Update_mongodb_data(Mongo_table,mongo_where_dict,mongo_update_dict)
            logger_get_data.info(f'item_id:{item_id} 更新mongo成功！！当前进度：{index}/{len(data_list)}')

        time.sleep(float(random.randint(200, 400)) / 1000)
        sql_where_data = [{"item_id": item_id}]
        manage_mysql.update_data(MySql_table, sql_updata_list, sql_where_data)

if __name__ == '__main__':
    # [('11045', '广东省清新县（现为清远市清新区）太和镇八号区一宗土地使用权及地下室', '房产', '住宅用房'), ('8359', '广州市荔湾区文昌南路137号之一地下2层288A车位', '房产', '其他用房')]
    data_list = get_id_list()
    # get_url('notice', 123123)
    get_detail_data(data_list)

