# -*- coding: UTF-8 -*-
'''
@Project ：法拍 
@File ：get_detail_data.py
@Author ：hao
@Date ：2022/12/19 15:47 
'''
import re
import sys
sys.path.append("..")
import random
import time
from datetime import datetime

from loguru import logger

from wbh_word.spider import Get_response, Get_ip
from wbh_word.manage_data import manage_mysql
from wbh_word.manage_data import manage_mongo

logger.add("/home/wangdong/fp_spider/GPW_Script/logger/Detail_get_data.log", filter=lambda record: record["extra"]["name"] == "Detail_get_data")
logger_get_data = logger.bind(name="Detail_get_data")
Mysql_table = 'wbh_GPW_id'
Mongo_table = 'wbh_GPW_detail'
def get_headers():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'HMF_CI=fc3a0f036d298f18353c1dc72d2e1a235cf493ae9cd532018dad68a8b0856139914f1d790027d80ceedc2758105870cb9a246058171fd9534b7b146619f5b16919; Hm_lvt_263a15f1b2e57ebc22960d3fa7c5537e=1669970065,1670206153,1671183793; ASPSESSIONIDAQSBRADD=OONCMCBCPGFMAEGDGDFDMJNK; SF_cookie_67=32244306; ASPSESSIONIDCQRARBCC=AGMBNCODDJNPNKJGAFOHOKDK; ASPSESSIONIDAQTSRCSR=BMLKCJMDOJLKEFJJEHPCLFBH; ASPSESSIONIDCQCSCACC=FHIBEPNDANJHDJDKHNHLNEKL; SF_cookie_44=20325660; ASPSESSIONIDAASCDBQD=IPNLPGODFGECFMPIIGFAKMKI; ASPSESSIONIDCATACARD=MCMFCNODELKLIAKDFMBMOFKA; ASPSESSIONIDCQTQRDRR=LOCEPOPDGCPJBGBNONGKAHMC; ASPSESSIONIDCSRQQDTQ=DBOLNAAAKGCJEJGGKGDEDPPE; HBB_HC=1ebc2ebd20ab3facab67dfd95f1013032db4f1bc9ab103325fcc2debdb7b95af5ac119587082c2a35be873889152c1489c; ASPSESSIONIDCSTCTDAD=DHGDPOPDHNLAFCOEEIAODEJC; Hm_lpvt_263a15f1b2e57ebc22960d3fa7c5537e=1671436006; HOY_TR=FNBTGMQCLJRSWXYA,9613A784BCDEF025,xgtkRhwfqrujblmc,0',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    #
    return headers
headers = get_headers()

def read_data():
    select_data = ['url','title','status_Mongo','status_Update']
    where_dict = [{'status_Update':1}]
    data_list = manage_mysql.read_where_data(Mysql_table,select_data,where_dict)
    # print(data_list)
    # [('http://www.gpai.net/sf/item2.do?Web_Item_ID=38055', '【一拍】兴宁市兴城和山河侧新兴豪庭7幢2单元1号1601房')]
    return data_list

def Update_Mysql(Msql_updata_list,url):      # 通过url定位
    updata_list = Msql_updata_list      # 1 -> 0
    where_dict = [{'url': url}]
    manage_mysql.update_data(Mysql_table,updata_list,where_dict)

def get_detail_data(data_list):
    try:
        proxies = Get_ip.ip_proxies()
    except:
        print("代理无法使用，proxies改外None")
        proxies = None
    index = 1
    update_num = 0      # 统计数据
    save_num = 0
    for data in data_list:
        down_time = str(datetime.now())  # 首次入库时间
        update_time = str(datetime.now())  # 更新时间
        url = data[0]
        title = data[1]
        status_Mongo = int(data[2])
        rule = 'Web_Item_ID=(.*)'
        item_id = re.findall(rule, url)[0]

        html,proxies = Get_response.get_html_response(url,headers,proxies=proxies,timeout=5)
        html = html.text
        # Mongo_save = {'url':url,'title':title,'html':html}

        if status_Mongo == 1:       # 待入库
            save_num += 1
            Mongo_save = {'ItemID': item_id, 'url': url, 'title': title, 'html': html,'status_analysis':1}
            if "正在拍卖" in html:
                Msql_updata_list = [{'status_Mongo':0,'update_time':update_time}]      # 正在拍卖 后续需要更新 status_Update 不变
                Mongo_save['status_Update'] = 1
            elif ("即将开始" in html) or ("尚未开始" in html):
                Msql_updata_list = [{'status_Mongo':0,'update_time':update_time}]
                Mongo_save['status_Update'] = 1
            elif "已结束" in html:
                Msql_updata_list = [{'status_Mongo':0,'status_Update':0,'update_time':update_time}]   # 不再需要更新
                Mongo_save['status_Update'] = 0
            # Update_Mysql(Msql_updata_list, url)
            Mongo_save['down_time'] = down_time
            Mongo_save['update_time'] = update_time
            manage_mongo.save_mongodb_data(Mongo_table,Mongo_save)
            Update_Mysql(Msql_updata_list, url)
            logger_get_data.info(f"进度{index} / {len(data_list)} 入库成功！！")

        elif status_Mongo == 0:       # 已入库，但待更新
            update_num += 1
            Mongo_updata_dict = {'html': html, 'update_time': update_time}
            if "已结束" in html:
                Msql_updata_list = [{'status_Update':0,'update_time':update_time}]   # 不再需要更新
                Mongo_updata_dict['status_Update'] = 0
            else:
                Msql_updata_list = [{'update_time': update_time}]
            Update_Mysql(Msql_updata_list, url)
            Mongo_where_dict = {'url':url}
            manage_mongo.Update_mongodb_data(Mongo_table,Mongo_where_dict,Mongo_updata_dict)
            logger_get_data.info(f"进度{index} / {len(data_list)} 更新成功！！")

        index += 1
        time.sleep(random.randint(1000, 2000) / 1000)
    logger_get_data.info(f"本次累计入库：{save_num}条，更新数据{update_num}条")


if __name__ == '__main__':
    data_list = read_data()
    get_detail_data((data_list))


