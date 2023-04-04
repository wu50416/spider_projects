# -*- coding: UTF-8 -*-
'''
@Project ：法拍 
@File ：get_id_data.py
@Author ：hao
@Date ：2022/12/22 13:58 
'''
import sys
sys.path.append("..")
import random
import re
import time
from datetime import datetime
import requests
from loguru import logger
from lxml import etree
from wbh_word.spider import Get_ip
from wbh_word.spider import Get_response
from wbh_word.manage_data import manage_mysql

# 融e购司法拍卖
Mysql_table = 'wbh_ICBC_id'
logger.add("/home/wangdong/fp_spider/ICBC_Script/logger/get_ICBC_ID.log", filter=lambda record: record["extra"]["name"] == "get_id_list")
logger_data = logger.bind(name="get_id_list")
def get_headers():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'B2BSESSION=218af399-0ce3-41d4-8d2c-63b561bf2305; DWRSESSIONID=EuFHtAXd6Y48!Sc!DozwWbuPlspAJrxZTko; JSESSIONID=0000E4CJ-3JwRRKsro983pTqBSC:78ed4631-49ef-4684-9e6c-9384e371220e',
        'Origin': 'https://gf.trade.icbc.com.cn',
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
def get_city_dict():
    city_dict = {'湛江市': '4408', '茂名市': '4409', '中山市': '4420', '阳江市': '4417', '深圳市': '4403', '佛山市': '4406', '广州市': '4401', '汕尾市': '4415', '江门市': '4407',
                '肇庆市': '4412', '云浮市': '4453', '梅州市': '4414', '惠州市': '4413', '韶关市': '4402', '河源市': '4416', '清远市': '4418', '东莞市': '4419', '珠海市': '4404', '汕头市': '4405'}
    return city_dict

def get_categoryFilter_dict():
    categoryFilter_dict = {'住宅用房': 'SM310000000000000006', '商业用房': 'SM310000000000000026', '车辆': 'SM310000000000000005', '其他': 'SM310000000000000255', '建设用地使用权': 'SM310000000000000007',
                            '其他用房': 'SM310000000000000028', '宅基地使用权': 'SM310000000000000023', '其他土地使用权': 'SM310000000000000025', '工业用房': 'SM310000000000000027', '一般动产': 'SM310000000000000031', '股权': 'SM310000000000000014'}
    return categoryFilter_dict

def get_params(page,category_key,category_value,city_key,city_value):
    data = {
        'categoryFilter': '["{}"]'.format(category_value),
        'MerchantFilterList': '[]',
        'YanPinList': '[]',
        'AgencyList': '[]',
        'SMProvinceFilter': '["44"]',
        'SMSecondRegionFilter': '["{}"]'.format(city_value),
        'SMThirdRegionFilter': '[]',
        'SMProvinceId': '',
        'SMPledgeFilter': '',
        'SMOrderStatusFilter': '[]',
        'SMDaikuanFilter': '[]',
        'SMXianGouFilter': '[]',
        'sortFilter': '',
        'dirFilter': '0',
        'catId': '',
        'categoryId_level': '',
        'category_Type': '3',
        'filterSecObjectId': '',
        'filterSecObjectName': '',
        'query': '',
        'viewType': 'large',
        'resultSecLevel': '',
        'selectedSearch': '[{"searchName":"分类","searchValue":"' + category_key + '","searchType":"category","storeOrCategoryId":"' + category_value + '","propId":"","enumId":"","priceId":""},{"searchName":"省区","searchValue":"广东省","searchType":"province","storeOrCategoryId":"44","propId":"","enumId":"","priceId":""},{"searchName":"市","searchValue":"' + city_key + '","searchType":"secondRegion","storeOrCategoryId":"' + city_value + '","propId":"","enumId":""}]',
        'exQuery': '',
        'currentPage': str(page),
        'orderStatusFlag': '',
        'searchType': '',
        'subjectChildType': '1',
        'startPrice': '',
        'endPrice': '',
        'resultLevel': '1',
        'filterObjectId': '8',
        'filterObjectName': '资产处置平台',
        'concatInfoForSearch': '',
        'smBidType': '',
        'smIndustry': '',
        'smEnsureWay': '',
        'smYapinType': '',
        'smAddr': '',
        'smMerchant': '',
        'smProvince': '',
        'smCity': '',
        'imgUrl': '',
        'innerSearch': '1',
    }
    return data

def dispose_page_response(page_response):
    page_response = page_response.text
    yes_no = re.findall('当前查询条件下无可匹配的记录', page_response)  # 判断是否有数据
    if len(yes_no) == 0:        # 等于0即有数据
        continue_bool = False        # 有数据,不跳过
        total = re.findall('total = (.*?);', page_response)
        max_page = int(total[0])  # 获取最大值
    else:
        continue_bool = True       # 无数据，跳过
        max_page = 0    # 没有数据时这个参数用不上
    return continue_bool,max_page


def get_save_bool(Mysql_table,url):
    select_list = ['url']
    where_data = [{'url':url}]

    where_data = manage_mysql.read_where_data(Mysql_table,select_list,where_data)
    if where_data:
        save_bool = False        # 数据库已有数据，，不插入数据
    else:
        save_bool = True         # 需要插入数据
    return save_bool


def get_save_dict(this_response):
    etr = etree.HTML(this_response)
    ul_list = etr.xpath(r'//div[@class="tabContent5"]/div/ul')
    all_dict_list = []
    down_time = str(datetime.now())  # 首次入库时间
    update_time = str(datetime.now())  # 更新时间
    for ul in ul_list:
        info_dict = {}
        li_list = ul.xpath(r'.//li')
        title = ''.join(li_list[1].xpath(r'./a/@title'))
        link = 'https://gf.trade.icbc.com.cn' + ''.join(li_list[1].xpath(r'./a/@href'))
        prodId = link.split('=')[1]
        image_url = ''.join(li_list[0].xpath(r'./a/img/@src'))
        # print(title, prodId, link)

        info_dict['ItemID'] = prodId
        info_dict['Title'] = title
        info_dict['url'] = link
        info_dict['image_url'] = image_url
        info_dict['down_time'] = down_time
        info_dict['update_time'] = update_time
        save_bool = get_save_bool(Mysql_table, url=link)
        if save_bool:
            all_dict_list.append(info_dict)
        else:
            continue
    return all_dict_list

def save_Mysql_data(all_dict_list):
    manage_mysql.save_data(Mysql_table,all_dict_list)



def get_id_data():
    city_dict = get_city_dict()
    categoryFilter_dict = get_categoryFilter_dict()     # 标的物类型
    effective_num = 0   # 统计有效数据
    for category_key, category_value in categoryFilter_dict.items():
        for city_key, city_value in city_dict.items():

            url = 'https://gf.trade.icbc.com.cn/searchproducts/pv.jhtml'

            page_params = get_params(1,category_key,category_value,city_key,city_value)        # 获取首页数据
            page_response,_ = Get_response.post_html_response(url,headers,page_params,timeout=5)
            # print(response.text)

            continue_bool,max_page = dispose_page_response(page_response)
            if continue_bool:
                logger_data.warning(f" {category_key}, {category_value}, {city_key} 当前查询条件下无可匹配的记录")
                continue
            for page in range(1,max_page+1):
                if page == 1:
                    this_response = page_response
                else:       # 防止重复取第一页数据
                    params = get_params(page, category_key, category_value, city_key, city_value)
                    this_response,_ = Get_response.post_html_response(url,headers,params,timeout=5)
                this_response = this_response.text

                all_dict_list = get_save_dict(this_response)
                if all_dict_list:
                    effective_num += len(all_dict_list)
                    save_Mysql_data(all_dict_list)
                    logger_data.info(f"进度：{page} / {max_page}  ----  {category_key}, {category_value}, {city_key}, {city_value} 共入库数据：{len(all_dict_list)}")
                else:
                    logger_data.warning(f"进度：{page} / {max_page}  ----  {category_key}, {category_value}, {city_key}, {city_value} 数据全部重复，剔除！！")
    logger_data.info(f"本次运行共录入数据： {effective_num} 条")

if __name__ == '__main__':
    get_id_data()

