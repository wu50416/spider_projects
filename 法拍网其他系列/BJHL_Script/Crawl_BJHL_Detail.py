# -*- coding: UTF-8 -*-
'''
@Project ：法拍 
@File ：BJHL_get_detail.py
@Author ：hao
@Date ：2022/12/28 11:55 
'''
import sys
sys.path.append("..")
import time
from datetime import datetime
import requests
from loguru import logger
from lxml import etree
from wbh_word.spider import Get_ip
from wbh_word.spider import Get_response
from wbh_word.manage_data import manage_mysql
from wbh_word.manage_data import manage_mongo
import Analysis_BJHL

logger.add("/home/wangdong/fp_spider/BJHL_Script/logger/Detail_get_data.log", filter=lambda record: record["extra"]["name"] == "Detail_get_data")
logger_get_data = logger.bind(name="Detail_get_data")
Mysql_table = 'wbh_BJHL_id'
Mongo_table = 'wbh_BJHL_detail'

def get_headers():
    headers = {
        'authority': 'otc.cbex.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://otc.cbex.com',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    return headers
headers = get_headers()

def get_data_list():
    # [('https://www.gdcourts.gov.cn//index.php?v=index_ktgg_detail&pid=3607108', '（2022）粤1973刑初3750号', '东莞市第三人民法院,大院第一审判庭', '1')]
    return_list = ['item_id','xmid','url','title','status_Mongo']  # 查询后返回的字段
    where_list = [{'status_Update':1}]         # 查询需要更新的数据  备注：status_Mongo为1时 ， status_Update 一定也为1
    data_list = manage_mysql.read_where_data(Mysql_table,return_list,where_list)
    return data_list



def get_url(url_name,item_id=None,xmid=None):
    '''
    结束状态确认：1、prjBidInfo中有无 “结束时间” 文字   2、 如果无，结束条件： 当前时间 > 结束时间+竞价周期+额外加10天时间
    base_url(html格式) : 基础数据、竞买须知、标的物介绍、竞买公告     注意这里是get请求
    prjBidInfo_url : 主要用于判断是否结束（if "结束时间！" in html）     当前价用 bidInfo_url
    bidInfo_url : '最高报价': '44621217', '延时次数': '155', '竞价次数': '341', '状态': '成交'      注意，这里请求还需要携带 data = {'cpdm': xmid, 'jjcc': 1}
    detailInfo_url : '报名人数': 31, '关注人数': 79, '围观人数': 35579
    priorityPsn_url : 优先购买权人（if "无优先购买权人信息！" in html）
    cjqrs_url : 成交确认书
    '''
    nowtime = int(round(time.time() * 1000))
    url_dict = {
        'base_url':'https://otc.cbex.com/sfpm/detail/{}.html'.format(item_id),
        'prjBidInfo_url': 'https://otc.cbex.com/page/sfpm/detail/prjBidInfo?cpdm={}&jjcc=1'.format(xmid),
        'bidInfo_url':'https://otc.cbex.com/service/sfpm/detail/bidInfo?tag={}_&puuid={}&isSubmitBzj=false&ws=true'.format(xmid, nowtime),
        'detailInfo_url': 'https://otc.cbex.com/service/sfpm/detail/detailInfo?xmid={}&itemno={}'.format(xmid, item_id),
        'priorityPsn_url':'https://otc.cbex.com/page/sfpm/detail/priorityPsn?itemno={}'.format(item_id),
        'cjqrs_url': 'https://otc.cbex.com/page/sfpm/detail/cjqrs?itemno={}'.format(item_id),
    }
    url = url_dict[url_name]
    return url

def get_base_data(item_id,proxies):
    # base_url 基础数据、竞买须知、标的物介绍、竞买公告     注意这里是get请求
    base_url = get_url('base_url',item_id=item_id)
    base_data,proxies = Get_response.get_html_response(base_url,headers,proxies=proxies,time_sleep=(0,0))
    base_data = base_data.text
    return base_data,proxies

def get_prjBidInfo_data(xmid,proxies):
    # prjBidInfo_url 主要用于判断是否结束（if "结束时间！" in html）     当前价用 bidInfo_url的数据
    prjBidInfo_url = get_url('prjBidInfo_url',xmid=xmid)
    prjBidInfo_data,proxies = Get_response.post_html_response(prjBidInfo_url,headers,proxies=proxies,time_sleep=(0,0))
    prjBidInfo_data = prjBidInfo_data.text
    return prjBidInfo_data,proxies

def get_bidInfo_data(xmid,proxies):
    # bidInfo_url : '最高报价': '44621217', '延时次数': '155', '竞价次数': '341', '状态': '成交'
    bidInfo_url = get_url('bidInfo_url',xmid=xmid)
    data = {'cpdm': xmid, 'jjcc': 1}
    bidInfo_data,proxies = Get_response.post_json_response(bidInfo_url,headers,data=data,proxies=proxies,time_sleep=(0,0))
    return bidInfo_data,proxies

def get_detailInfo_data(xmid, item_id,proxies):
    # {"code":"","msg":"","object":{"bmrs":4,"sfgz":0,"gzrs":4,"wgcs":10368},"success":true}
    # detailInfo_url : '报名人数': 31, '关注人数': 79, '围观人数': 35579
    detailInfo_url = get_url('detailInfo_url',xmid=xmid,item_id=item_id)
    detailInfo_data,proxies = Get_response.post_json_response(detailInfo_url,headers,proxies=proxies,time_sleep=(0,0))
    return detailInfo_data,proxies

def get_priorityPsn_data(item_id,proxies):
    # 优先购买权人（if "无优先购买权人信息！" in html）
    priorityPsn_url = get_url('priorityPsn_url',item_id=item_id)
    priorityPsn_data,proxies = Get_response.post_html_response(priorityPsn_url,headers,proxies=proxies,time_sleep=(0,0))
    priorityPsn_data = priorityPsn_data.text
    return priorityPsn_data,proxies

def get_cjqrs_data(item_id,proxies):
    cjqrs_url = get_url('cjqrs_url', item_id=item_id)
    cjqrs_data, proxies = Get_response.post_html_response(cjqrs_url, headers, proxies=proxies,time_sleep=(0, 0))
    cjqrs_data = cjqrs_data.text
    return cjqrs_data,proxies

# def get_end_bool(prjBidInfo_data,):
#     pass

def run():
    proxies = Get_ip.ip_proxies()
    # proxies = None
    data_list = get_data_list()
    index = 0
    save_num = 0    # 保存的个数
    update_num = 0  # 更新个数
    for data in data_list:
        index += 1
        item_id = data[0]
        xmid = data[1]
        url = data[2]
        title = data[3]
        status_Mongo = int(data[4])
        down_time = str(datetime.now())  # 首次入库时间
        update_time = str(datetime.now())  # 更新时间
        base_data,proxies = get_base_data(item_id,proxies)
        prjBidInfo_data, proxies = get_prjBidInfo_data(xmid,proxies)
        bidInfo_data, proxies = get_bidInfo_data(xmid,proxies)
        detailInfo_data, proxies = get_detailInfo_data(xmid, item_id,proxies)
        priorityPsn_data, proxies = get_priorityPsn_data(item_id,proxies)
        cjqrs_data,proxies = get_cjqrs_data(item_id,proxies)

        if status_Mongo == 1:       # 首次入库
            Mongo_save_dict = {'item_id': item_id, 'xmid': xmid, 'title': title, 'url': url,'base_data': base_data, 'prjBidInfo_data': prjBidInfo_data
                , 'bidInfo_data': bidInfo_data,'detailInfo_data':detailInfo_data,'priorityPsn_data':priorityPsn_data,'cjqrs_data':cjqrs_data
                ,'down_time':down_time,'update_time':update_time,'status_analysis':1}
            if ("即将开始" in prjBidInfo_data) or ("竞价中" in prjBidInfo_data):
                Mongo_save_dict['status_Update'] = 1
                Mysql_Update_dict = [{'status_Mongo':0,'update_time':update_time}]        # 未结束
            else:
                Mongo_save_dict['status_Update'] = 0
                Mysql_Update_dict = [{'status_Mongo': 0,'status_Update':0, 'update_time': update_time}]  # 已结束
            where_data = [{'item_id': item_id, 'xmid': xmid}]
            manage_mongo.save_mongodb_data(Mongo_table,Mongo_save_dict)
            manage_mysql.update_data(Mysql_table,Mysql_Update_dict,where_data=where_data)
            save_num += 1
            logger_get_data.info(f"进度：{index} / {len(data_list)} 录入数据成功：item_id: {item_id} , xmid: {xmid}")

        elif status_Mongo == 0:     # 已经入库，但需要更新数据
            Mongo_Update_dict = {'base_data': base_data, 'prjBidInfo_data': prjBidInfo_data,'bidInfo_data': bidInfo_data, 'detailInfo_data': detailInfo_data
                , 'priorityPsn_data': priorityPsn_data, 'cjqrs_data': cjqrs_data, 'update_time': update_time}
            if ("即将开始" in prjBidInfo_data) or ("竞价中" in prjBidInfo_data):       # 还是没有结束
                Mysql_Update_dict = [{'update_time': update_time}]
            else:       # 结束、停止更新数据
                Mongo_Update_dict['status_Update'] = 0
                Mysql_Update_dict = [{'status_Update': 0, 'update_time': update_time}]
            Mongo_where_dict = {'item_id': item_id, 'xmid': xmid}
            Mysql_where_dict = [Mongo_where_dict]
            manage_mongo.Update_mongodb_data(Mongo_table,Mongo_where_dict,Mongo_Update_dict)
            manage_mysql.update_data(Mysql_table,Mysql_Update_dict,Mysql_where_dict)
            logger_get_data.info(f"进度：{index} / {len(data_list)} 录入更新成功：item_id: {item_id} , xmid: {xmid}")
            update_num += 1
    logger_get_data.info(f"运行完美结束！！ 本次录入数据：{save_num} 条，更新数据: {update_num} 条")
    Analysis_BJHL.run()

if __name__ == '__main__':
    run()

