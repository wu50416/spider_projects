# -*- coding: UTF-8 -*-
'''
@Project ：法拍 
@File ：BJHL_get_id.py
@Author ：hao
@Date ：2022/12/28 9:36 
'''
import sys
sys.path.append("..")
from datetime import datetime
from loguru import logger
from lxml import etree
from wbh_word.spider import Get_ip
from wbh_word.spider import Get_response
from wbh_word.manage_data import manage_mysql

Mysql_table = 'wbh_BJHL_id'
logger.add("/home/wangdong/fp_spider/BJHL_Script/logger/IDlist_get_data.log", filter=lambda record: record["extra"]["name"] == "IDlist_get_data")
logger_get_data = logger.bind(name="IDlist_get_data")
def get_headers():
    headers = {
        'authority': 'otc.cbex.com',
        'accept': 'text/html, */*; q=0.01',
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


def get_bdwlx_dict():
    bdwlx_dict = {'住宅用房': 6, '商业用房': 26, '机动车': 5, '工业用房': 27, '其他用房': 28, '股权': 14, '债权': 17,
                   '土地': 100138, '林权': 36, '矿权': 39, '无形资产': 100047, '珍品': 100059, '资产': 100037, '交通工具': 100084, '船舶': 12,
                   '航空交通': 29, '其他': 100286}
    return bdwlx_dict

def get_params(page):
    data = {
        # 'bdwlx': '5',             # 标的物类型（不填表示全选）
        'bdwszd': '440000',         # 广东省全省数据
        'kpsjbegin': '',
        'kpsjend': '',
        'jgbegin': '',
        'jgend': '',
        'order': '0',
        'dk': '',
        'xg': '',
        'flushResources': 'true',
        'keyWord': '',
        'pageNo': str(page),        # 从1开始
        'pageSize': '16',
    }
    return data

def get_id_html(page,proxies):
    url = 'https://otc.cbex.com/page/sfpm/list/list_li'
    params = get_params(page)
    id_html,proxies = Get_response.post_html_response(url,headers,params,proxies=proxies)
    id_html = id_html.text
    return id_html,proxies

def get_save_bool(item_id,xmid):
    select_list = ['item_id','xmid']
    where_data = [{'item_id':item_id,'xmid':xmid}]

    where_data = manage_mysql.read_where_data(Mysql_table,select_list,where_data)
    if where_data:
        save_bool = False        # 数据库已有数据，，不插入数据
    else:
        save_bool = True         # 需要插入数据
    return save_bool


def dispose_id_html(page,id_html):
    break_bool = False       # 是否取消继续执行（退出）（翻页/解析任务）
    html = etree.HTML(id_html)
    res_li_list = html.xpath('//li')
    all_save_dict = []
    if len(res_li_list) == 0:
        break_bool = True       # 确认退出
    else:
        down_time = str(datetime.now())  # 首次入库时间
        update_time = str(datetime.now())  # 更新时间
        for res_li in res_li_list:
            item_id = res_li.xpath(r'./@data-itemno')[0]
            xmid = res_li.xpath(r'./@data-xmid')[0]
            ur = res_li.xpath('.//a/@href')[0]
            url = "https://otc.cbex.com/"+ur
            title = res_li.xpath(r'.//a[@class="title"]/text()')[0]
            save_dict = {'item_id':item_id,'xmid':xmid,'url':url,'title':title,'down_time':down_time,'update_time':update_time,
                         'status_Mongo':1,'status_Update':1}
            save_bool = get_save_bool(item_id,xmid)
            if save_bool:       # 是否需要保存
                logger_get_data.info(f"正在获取{page}页数据---item_id: {item_id},xmid: {xmid}，title: {title}数据录入成功！！")
                all_save_dict.append(save_dict)
            else:
                logger_get_data.warning(f"正在获取{page}页数据---item_id: {item_id},xmid: {xmid}，title: {title}数据录入重复 跳过！！")
        if all_save_dict:
            manage_mysql.save_data(Mysql_table,all_save_dict)
    return break_bool,all_save_dict

def run():
    break_bool = False
    page = 1
    all_num = 0
    try:
        proxies = Get_ip.ip_proxies()
    except:
        proxies = None
    while break_bool == False:       # 是否继续执行
        id_html,proxies = get_id_html(page,proxies)
        break_bool,all_save_dict = dispose_id_html(page,id_html)
        all_num += len(all_save_dict)
        page += 1
    logger_get_data.info(f"程序运行成功----本次共录入{all_num}条数据")

if __name__ == '__main__':
    run()
