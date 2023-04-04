# -*- coding: UTF-8 -*-
'''
@Project ：法拍 
@File ：get_id_list.py
@Author ：hao
@Date ：2022/12/19 10:19 
'''
import sys
sys.path.append("..")
import random
import time
from datetime import datetime

import requests
from loguru import logger
from lxml import etree
from wbh_word.spider import Get_ip
from wbh_word.spider import Get_response
from wbh_word.manage_data import manage_mysql
import requests

logger.add("/home/wangdong/fp_spider/GPW_Script/logger/IDlist_get_data.log", filter=lambda record: record["extra"]["name"] == "IDlist_get_data")
logger_get_data = logger.bind(name="IDlist_get_data")

# 公拍网数据
Mysql_table = 'wbh_GPW_id'
def get_headers():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': 'dLwyZZHe134zS=5LLE3XuOZIMaGbrix0XnZUgjwXf7fJ8a4QGxLaHNdZvJhyCaMF289ox_Rgf3UGlaAwTjQGCR_u5rBsNtPQJ.GnG; HMF_CI=8a3cfe9004fc51516d796309c6e74c014b63b8d7a23b61b430cdae0f752d093580242ddf3e376a0f81a941277bb82408b4e6930fe25dda3e4458b83ebfc1f2a257; ASPSESSIONIDSQACDDQC=GKNDPGBCBOHOMCNOLHAAPDLD; SF_cookie_67=29422949; SF_cookie_8=27902555; Hm_lvt_263a15f1b2e57ebc22960d3fa7c5537e=1669970065,1670206153,1671183793; ASPSESSIONIDSSDDBATC=JIFCHLNDOKBAEIIFNNNEALCJ; ASPSESSIONIDSSDBCCQC=DJIBIJODJDIIKJPPHEJDLKDJ; HMY_JC=5893bf05e66d34607ff34863f3b15d356f91af49ddeedb3b4b2160520f22e06a44,; Hm_lpvt_263a15f1b2e57ebc22960d3fa7c5537e=1671419854; dLwyZZHe134zT=ryMxrAc7TSL3p.A57rfsVQZt1jL38CgN2.cSxocIuQ7r3XBrtJOXYRG0g1JSoSxvxD.w49e2mBtfodjxNMKfGMN64.Osnw33bShn1yOHtEMlC2JPeO9JFxlDK9DFURD0xF6Yo5wN_JIphpb.lrtDO.7WdfpbG9cgHbrqu5xBPnagHmcroReptQ8xB2SzaDQvahMGFOcYOkjgTLfSTks8b9ZpDLQ8F0vMHyj9RHKVdZ7kRIcoarXYHB1cR7SniDhr9_LIpwROp39V.11GcNJljXCtsu5hks.xA_a1u8RHHPmvx86X3Gr1_N8AcG7ov0ahUvKdEH4VLQG53qoen26Mp2nTbtH69Kx3U_VTEpYIyGkokygyjHjddPHp8CT4cLYWXoSdxBq9qr.z1.Bcu5GNLa; C3VK=682b61',
        'Referer': 'http://s.gpai.net/sf/search.do',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }
    return headers
headers = get_headers()

def get_params(page):
    params = {
        'cityNum': '44',   # 广东
        'Page': page,
    }
    return params

def get_html(page,proxies):

    params = get_params(page)
    response,proxies = Get_response.get_html_response(url='http://s.gpai.net/sf/search.do',params=params,headers=headers,proxies=proxies,timeout=10)
    # response = requests.get('http://s.gpai.net/sf/search.do', params=params, headers=headers, verify=False).text
    html = response.text
    return html,proxies

def get_save_bool(Mysql_table,url):
    select_list = ['url']
    where_data = [{'url':url}]

    where_data = manage_mysql.read_where_data(Mysql_table,select_list,where_data)
    if where_data:
        save_bool = False        # 数据库已有数据，，不插入数据
    else:
        save_bool = True         # 需要插入数据
    return save_bool

def get_sql_dict():
    try:
        proxies = Get_ip.ip_proxies()
    except:
        print("代理无法使用，proxies改外None")
        proxies = None
    html,proxies = get_html(1,proxies)
    html = etree.HTML(html)


    max_page = html.xpath('/html/body/div/div[7]/div/div[4]/div/a[9]/text()')
    # print(max_page)
    all_sql_dict_list = []
    for page in range(1,int(max_page[0])+1):
        down_time = str(datetime.now())  # 首次入库时间
        update_time = str(datetime.now())  # 更新时间
        if page == 1:
            this_html = html        # 防止重复取数
        else:
            this_html,proxies = get_html(page,proxies)
            this_html = etree.HTML(this_html)
        html_li = this_html.xpath('/html/body/div/div[7]/div/div[3]/ul/li')
        for li in html_li:
            one_sql_dict = {}
            url = li.xpath('./div/div[@class="item-tit"]/a/@href')
            url = 'http:' + url[0]
            title = li.xpath('./div/div[@class="item-tit"]/a/text()')
            s_price = li.xpath('./div/div[@class="gpai-infos"]//b[@class="price-red"]/text()')
            one_sql_dict['url'] = url
            one_sql_dict['title'] = title[0]
            one_sql_dict['s_price'] = s_price[0]
            one_sql_dict['status_Mongo'] = 1
            one_sql_dict['status_Update'] = 1
            one_sql_dict['down_time'] = down_time
            one_sql_dict['update_time'] = update_time
            # print(url)
            # print(title)
            # print(s_price)
            save_bool = get_save_bool(Mysql_table,url)
            if save_bool:
                all_sql_dict_list.append(one_sql_dict)
                logger_get_data.info(f"等待入库！！,  当前进度：{page} / {max_page[0]}  dict:{one_sql_dict}")
            else:
                logger_get_data.info(f"数据重复！！跳过, 当前进度：{page} / {max_page[0]}  dict:{one_sql_dict}")
                continue
        time.sleep((random.randint(500,1000))/1000)
    # print(all_sql_dict_list)
    if all_sql_dict_list:
        manage_mysql.save_data(Mysql_table,all_sql_dict_list)
        logger_get_data.warning(f"所有数据入库成功！！ 本次累计入库{len(all_sql_dict_list)}条数据")
if __name__ == '__main__':
    get_sql_dict()
    # html = get_html(18,None)
    # print(html)