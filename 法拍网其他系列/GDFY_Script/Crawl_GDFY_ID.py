# -*- coding: UTF-8 -*-
'''
@Project ：法拍 
@File ：jiexi.py
@Author ：hao
@Date ：2022/12/1 11:02
@url ： https://www.gdcourts.gov.cn/index.php?v=index_ktgg_list&page=3
'''
import sys
sys.path.append("..")
import time

import requests
from lxml import etree
from wbh_word.spider import Get_ip
from loguru import logger
from wbh_word.manage_data import manage_mysql
from wbh_word.spider.Get_response import get_html_response
import requests


logger.add("/home/wangdong/fp_spider/GDFY_Script/logger/IDlist_get_data.log", filter=lambda record: record["extra"]["name"] == "IDlist_get_data")
logger_get_data = logger.bind(name="IDlist_get_data")

Mysql_table = "wbh_GDFY_data"
def get_headers():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'close',
        'Referer': 'https://www.gdcourts.gov.cn/index.php?v=index_ktgg_list&page=101',
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

def get_params(page):
    params = {
        'v': 'index_ktgg_list',
        'page': str(page),
    }
    return params


def get_resposne(proxies,page):
    url = 'https://www.gdcourts.gov.cn/index.php'
    params = get_params(page)

    response,proxies = get_html_response(url=url,headers=headers,proxies=proxies,params=params,timeout=150)
    response = response.text
    html_resposne = response.replace('&nbsp', '')       # 用来测试响应数据是否可用
    html_try = etree.HTML(html_resposne)
    try:
        res_tr = html_try.xpath('/html/body/div[@class="Article_content"]/div/table//tr')
    except AttributeError:      # 数据异常无法匹配成功
        proxies = Get_ip.ip_proxies()       # 重新访问
        response,proxies = get_resposne(proxies, page)
    return response,proxies

def dispose_response(response):
    '''
    []  # 第一个数据需要剔除
    ['2022-12-02 14:30', '至', '2022-12-02 15:00', '东莞市第三人民法院', '大院第一审判庭', '（2022）粤1973刑初3750号']
    ['2022-12-05 15:00', '至', '2022-12-05 16:00', '德庆县人民法院', '第三审判庭', '（2022）粤1226民初1299号']
    ['2022-12-05 15:00', '至', '2022-12-05 16:00', '德庆县人民法院', '第三审判庭', '（2022）粤1226民初1299号']
    '''
    html = response.replace('&nbsp', '')
    html = etree.HTML(html)
    res_tr = html.xpath('/html/body/div[@class="Article_content"]/div/table//tr')
    data_list = []
    # data_dict = {"item_id": item_id, "down_time": down_time, "update_time": update_time, "status_Mongo": 1,"status_Update": 1}
    for res in res_tr[1:]:       # 第一个数据为表头  需要剔除
        text_list = []
        res_td_list = res.xpath("td")
        for res_td in res_td_list:
            text = res_td.xpath('nobr//text()')
            if "至" in text:    # ['2022-12-02 14:30', '至', '2022-12-02 15:00']
                text = ''.join(text)
            else:           # ['德庆县人民法院', '第三审判庭'], ['（2022）粤1226民初1299号']
                text = ','.join(text)

            text_list.append(text)
        href_lists = res_td.xpath('nobr/a/@href')          # 取最后一个标签元素  即案号  用来获取url
        url_list = []
        for href in href_lists:
            url = 'https://www.gdcourts.gov.cn/' + href
            url_list.append(url)
        url = ','.join(url_list)
        text_list.append(url)
        data_list.append(text_list)
    return data_list


def get_save_bool(Mysql_table,url):
    select_list = ['url']
    where_data = [{'url':url}]

    where_data = manage_mysql.read_where_data(Mysql_table,select_list,where_data)
    if where_data:
        save_bool = False        # 数据库已有数据，，不插入数据
    else:
        save_bool = True         # 需要插入数据
    return save_bool

def save_Mysql_dict(Mysql_table,data_list,page):
    save_num = 0
    for data in data_list:
        # print(data)
        time = data[0]
        place = data[1]
        case_name = data[2]
        url = data[3]
        data_list = [{'case_name':case_name,'url':url,'time':time,'place':place,"status_detail":1}]
        save_bool = get_save_bool(Mysql_table,url)
        if save_bool:
            manage_mysql.save_data(Mysql_table,data_list)
            logger_get_data.info(f"当前进度：{page} / 100 入库成功  {data_list}")
            save_num += 1
        else:
            print(f"当前进度：{page} / 100 案号：{case_name}  url:{url} 数据重复，跳过")
            continue
    return save_num

def run():
    all_save_num = 0
    try:
        proxies = Get_ip.ip_proxies()
    except:
        proxies = None
    for page in range(1,101):      # 1~100页数据  超过100页不能访问
        print(" ====================================================== ")
        print(f"************** 当前进度: {page} / 100 ************")
        response,proxies = get_resposne(proxies,page)       # 获取当前页数据
        time.sleep(2.3)
        data_list = dispose_response(response)
        # print(data_list)
        save_num = save_Mysql_dict(Mysql_table,data_list,page)      # 保存到sql数据库
        all_save_num += save_num
        print(" ====================================================== \n")
    logger_get_data.info(f"本次程序运行成功！共录入{all_save_num}条数据")

if __name__ == '__main__':
    run()


