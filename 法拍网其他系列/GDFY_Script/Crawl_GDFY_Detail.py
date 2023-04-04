# -*- coding: UTF-8 -*-
'''
@Project ：法拍 
@File ：GDFY_detail.py
@Author ：hao
@Date ：2022/12/8 17:21 
'''
import sys
sys.path.append("..")
import time
from datetime import datetime

from loguru import logger
from wbh_word.manage_data import manage_mysql
from wbh_word.spider import Get_ip
from wbh_word.spider.Get_response import get_html_response
from lxml import etree


logger.add("/home/wangdong/fp_spider/GDFY_Script/logger/Detail_get_data.log", filter=lambda record: record["extra"]["name"] == "Detail_get_data")
logger_get_data = logger.bind(name="Detail_get_data")

Mysql_table = "wbh_GDFY_data"
def get_data_list():
    # [('https://www.gdcourts.gov.cn//index.php?v=index_ktgg_detail&pid=3607108', '（2022）粤1973刑初3750号', '东莞市第三人民法院,大院第一审判庭', '1')]
    return_list = ['url','case_name','status_detail']  # 查询后返回的字段
    where_list = [{"status_detail": 1}]         # 查询需要更新的数据  备注：status_Mongo为1时 ， status_Update 一定也为1
    data_list = manage_mysql.read_where_data(MySql_table,return_list,where_list)
    return data_list

def get_headers():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'close',
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
    return headers


headers = get_headers()
def get_response(url,proxies):
    response, proxies = get_html_response(url=url, headers=headers, proxies=proxies, timeout=100)
    response = response.text
    # time.sleep(2.5)
    if len(response) < 5000:
        logger_get_data.warning(f"url {url}响应长度为： {len(response)}，response：{response}")
        response, proxies = get_response(url,proxies)
    return response, proxies


def dispose_response(response):
    html = response.replace('&nbsp', '')
    # print(html)
    html = etree.HTML(html)
    try:
        res_td_list = html.xpath('//div[@class="Article_content"]/div[@class="ktggform"]//tr[2]//td')
        detail_data_list = []
        for res_td in res_td_list:
            text = res_td.xpath('.//text()')
            if "至" in text:  # ['2022-12-02 14:30', '至', '2022-12-02 15:00']
                text = ''.join(text)
            else:  # ['德庆县人民法院', '第三审判庭'], ['（2022）粤1226民初1299号']
                text = ','.join(text)
            detail_data_list.append(text)
        # ['2022-12-05 15:00至2022-12-05 16:00', '德庆县人民法院,第三审判庭', '（2022）粤1226民初1299号', '德庆县人民法院定于2022-12-05 15:00 在德庆县人民法院第三审判庭公开开庭审理[原告]广东璞真酒业有限公司,[被告]德庆县德城商行买卖合同纠纷一案']
        if detail_data_list:
            return detail_data_list
        else:
            print("detail_data_list:",detail_data_list)
            raise
    except Exception as e:
        print(e)
        print("response: ",response)

def run():
    data_list =get_data_list()
    try:
        proxies = Get_ip.ip_proxies()
    except:
        proxies = None
    index = 1
    update_time = str(datetime.now())  # 更新时间
    for data in data_list:
        detail_url = data[0]
        case_name = data[1]
        logger_get_data.info(f" ====== 进度：{index} / {len(data_list)}  正在获取{case_name}的数据 --- url：{detail_url}  =====")
        index += 1
        html_response,proxies = get_response(url=detail_url,proxies=proxies)
        detail_data_list = dispose_response(html_response)

        detail_time = detail_data_list[0]
        detail_place = detail_data_list[1]
        detail_case_name = detail_data_list[2]
        datail_data = detail_data_list[3]

        updata_list = [{"time":detail_time,"place":detail_place,"case_name":detail_case_name,"detail_data":datail_data,"update_time":update_time,"status_detail":0}]
        where_data = [{'url': detail_url}]
        manage_mysql.update_data(MySql_table, updata_list, where_data)
        # print("Mysql存入成功！！！")




if __name__ == '__main__':
    run()



