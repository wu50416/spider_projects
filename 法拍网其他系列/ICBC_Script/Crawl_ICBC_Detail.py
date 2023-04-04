# -*- coding: UTF-8 -*-
'''
@Project ：法拍 
@File ：get_detail_data.py
@Author ：hao
@Date ：2022/12/23 16:01 
'''
import sys
sys.path.append("..")
import re
import time
from datetime import datetime
from wbh_word.manage_data import manage_mysql, manage_mongo
from wbh_word.spider import Get_response, Get_ip
from loguru import logger
import Analysis_ICBC

logger.add("/home/wangdong/fp_spider/ICBC_Script/logger/get_ICBC_Detail.log", filter=lambda record: record["extra"]["name"] == "get_detail_list")
logger_data = logger.bind(name="get_detail_list")

Mysql_table = 'wbh_ICBC_id'
Mongo_table = 'wbh_ICBC_detail'
def get_headers():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'DWRSESSIONID=EuFHtAXd6Y48!Sc!DozwWbuPlspAJrxZTko; B2BSESSION=60418a4c-117d-4c85-9757-4e5944c5ee4b; JSESSIONID=0000Ezy6-qqLV8OLqubPapB9cBB:0dc9e9f7-375d-463e-8cd4-fc43f944b7c4',
        'Referer': 'https://gf.trade.icbc.com.cn/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    return headers

headers = get_headers()
def read_sql_data():
    select_data = ['ItemID','url','image_url','title','status_Mongo']
    where_dict = [{'status_Update':1}]
    data_list = manage_mysql.read_where_data(Mysql_table,select_data,where_dict)
    # print(data_list)
    # [('http://www.gpai.net/sf/item2.do?Web_Item_ID=38055', '【一拍】兴宁市兴城和山河侧新兴豪庭7幢2单元1号1601房')]
    return data_list

def get_detail_html(url,proxies):
    detail_html,proxies = Get_response.get_html_response(url,headers,proxies=proxies)
    return detail_html,proxies

def get_subjectMatterTradeId(detail_html):
    subjectMatterTradeId = re.findall("subjectMatterTradeId='(.*?)';", detail_html)[0]
    # print(subjectMatterTradeId)     # 202212020001319455
    return subjectMatterTradeId

def get_NewDateNew(subjectMatterTradeId,proxies):
    params = {
        'subjectMatterTradeId': str(subjectMatterTradeId),
    }
    url = 'https://gf.trade.icbc.com.cn/subjectMatterTrade/getNewDateNew.jhtml'
    NewDateNew,proxies = Get_response.get_json_response(url,headers,params,proxies=proxies)
    return NewDateNew,proxies

def get_visitorCount(prodId,image_url,title,proxies):
    url = 'https://gf.trade.icbc.com.cn/wholeSaleProd/visitorCount.jhtml'
    data = {
        'prodId': prodId,
        'imageUrl': image_url,
        'prodName': title,
    }
    visitorCount,proxies = Get_response.post_json_response(url,headers,data=data,proxies=proxies)
    # print('visitorCount : ',visitorCount)
    return visitorCount,proxies

def get_save_bool(NewDateNew):
    endTimeDate = NewDateNew['basicMap']['endTimeDate']
    e_time = datetime.strptime(endTimeDate,"%Y-%m-%d %H:%M:%S")
    if e_time>datetime.now():       # 未结束
        save_bool = 'update'
    else:
        save_bool = 'save'      # 已结束
    return save_bool


def run(data_list):
    proxies = Get_ip.ip_proxies()
    # proxies = None
    save_num = 0    # 保存的个数
    update_num = 0  # 更新个数
    index = 0
    for data in data_list:
        # select_data = ['ItemID','url','image_url','title','status_Mongo']
        ItemID = data[0]
        url = data[1]
        image_url = data[2]
        title = data[3]
        status_Mongo = int(data[4])

        down_time = str(datetime.now())         # 首次入库时间
        update_time = str(datetime.now())       # 更新时间

        detail_html, proxies = get_detail_html(url,proxies)
        detail_html = detail_html.text

        subjectMatterTradeId = get_subjectMatterTradeId(detail_html)        # html中获取这个参数来获取NewDateNew数据
        NewDateNew, proxies = get_NewDateNew(subjectMatterTradeId,proxies)
        visitorCount, proxies = get_visitorCount(ItemID,image_url,title,proxies)
        # print(NewDateNew)

        save_bool = get_save_bool(NewDateNew)
        index += 1
        if status_Mongo == 1:       # 待入库\
            save_num += 1
            Mongo_save_dict = {'ItemID':ItemID,'url':url,'title':title,'image_url':image_url,'detail_html':detail_html,'NewDateNew':NewDateNew,'visitorCount':visitorCount
                ,'subjectMatterTradeId':subjectMatterTradeId,'down_time':down_time,'update_time':update_time,'status_analysis':1}
            if save_bool == 'save':
                Mongo_save_dict['status_Update'] = 0        # 不再更新
                Mysql_update_dict = [{'status_Mongo':0,'status_Update':0}]
            else:
                Mongo_save_dict['status_Update'] = 1        # 后续需要更新
                Mysql_update_dict = [{'status_Mongo':0}]
            Mysql_update_where = [{'url':url}]
            manage_mongo.save_mongodb_data(Mongo_table,Mongo_save_dict)
            manage_mysql.update_data(Mysql_table, Mysql_update_dict,Mysql_update_where)
            logger_data.info(f"进度：{index} / {len(data_list)} 录入数据成功：url: {url}")

        elif status_Mongo == 0:          # 待更新
            update_num += 1
            Mongo_update_dict = {'detail_html': detail_html, 'NewDateNew': NewDateNew,'visitorCount':visitorCount, 'update_time': update_time}
            if save_bool == 'save':
                Mongo_update_dict['status_Update'] = 0        # 不再更新
                Mysql_update_dict = [{'status_Update':0}]
                Mysql_update_where = [{'url': url}]
                manage_mysql.update_data(Mysql_table, Mysql_update_dict, Mysql_update_where)
            else:
                Mongo_update_dict['status_Update'] = 1        # 后续需要更新
            where_dict = {'url': url}
            manage_mongo.Update_mongodb_data(Mongo_table,where_dict,Mongo_update_dict)
            logger_data.info(f"进度：{index} / {len(data_list)} 更新数据成功：url: {url}")
    logger_data.info(f"运行完美结束！！ 本次录入数据：{save_num} 条，更新数据: {update_num} 条    正在开始解析数据")

    Analysis_ICBC.run()

if __name__ == '__main__':
    data_list = read_sql_data()
    # print(data_list)
    run(data_list)



