# -*- coding: UTF-8 -*-
'''
@Project ：Project 
@File    ：获取营销策略中心数据.py
@IDE     ：PyCharm 
@Author  ：hao@
@Date    ：2022/9/1 14:01
'''
import copy
import datetime
import time
import os
import glob
import random
import pandas as pd
import requests

os.chdir(os.path.dirname(__file__))
from dynamictoken_api import get_params

PATH = r'data'  # Excel 文件所在文件夹
OUTPUT = '营销策略中心-汇总.xlsx'
SHEETS = ['拉新快', '会员快', '上新快', '货品加速', '爆发收割', '活动加速', '线索通', '获客易']


headers = {
    'authority': 'adbrain.taobao.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://adbrain.taobao.com/indexbp.html',
    'accept-language': 'zh-CN,zh;q=0.9',
 }


def combine():
    writer = pd.ExcelWriter(os.path.join(PATH, OUTPUT))
    for sheet in SHEETS:
        pattern = rf'营销策略中心计划商品列表-{sheet}.xlsx'
        file_list = glob.glob(os.path.join(PATH, pattern))
        if not file_list:
            continue
        for file in file_list:
            if pattern.endswith('csv'):
                df2 = pd.read_csv(file, engine='python')
            else:
                df2 = pd.read_excel(file)
        # del df2['launchTime']
        df2.to_excel(writer, sheet_name=sheet, index=False)
    writer.save()


def get_keys(d, value):
    return [k for k, v in d.items() if v == value]


def get_plan_good_one(type_value, start_date, end_date, effect, offset, unifyType):
    params = (
        ('r', 'mx_4362'),
        ('startTime', start_date),
        ('endTime', end_date),
        ('effect', effect),
        ('offset', offset),
        ('pageSize', pageSize),
        ('bizCode', type_value),
        ('unifyType', unifyType),
        ('timeStr', timeStr),
        ('dynamicToken', dynamicToken),
        ('csrfID', csrfID),
    )
    effect_mapping = {'1': '1天转化数据', '3': '3天转化数据', '7': '7天转化数据',
                      '15': '15天转化数据', '-1': '15天累计数据', '30': '30天累计数据'}

    try:                       # https://adbrain.taobao.com/api/cross/report/findList.json        # 万相台服务商
        response = requests.get('https://adbrain.taobao.com/api/campaign/report/findOverProductCampaignReportPage.json',
                                headers=headers, params=params, timeout=7)
    except Exception as e:
        response = requests.get('https://adbrain.taobao.com/api/campaign/report/findOverProductCampaignReportPage.json',
                                headers=headers, params=params, timeout=7)

    print(start_date, end_date,'response.text : ', response.text)
    break_bool = False
    datas = response.json()['data'].get('list', [])

    count = response.json()['data'].get('count', 0)
    print('count: ',count,'pageSize: ',pageSize )
    if count < pageSize:
        break_bool = True
    data_list = []

    for index, data in enumerate(datas):
        # print('index:',index)
        print('data：',data)
        item_id = data.get('itemId')
        if item_id is None or item_id == 0:
            item_id = data.get('itemIdInString')
        # print(item_id)
        if str(item_id) != '0':
            item = {}
            item['取数时间'] = start_date
            item['计划ID'] = data.get('campaignId', '-')
            item['计划名称'] = data.get('campaignName', '-')
            item['计划开始时间'] = start_date
            item['计划结束时间'] = end_date
            item['转化周期'] = effect_mapping.get(str(effect))


            item['商品ID'] = item_id
            item['商品名称'] = data.get('itemName')
            # item['launchTime'] = data.get('launchTime')
            item['展现量'] = data.get('adPv')
            item['点击量'] = data.get('click')
            item['消耗'] = data.get('charge')
            if unifyType == 'kuan':
                item['成交金额'] = data.get('alipayInshopAmtKuan')
                item['总成交笔数'] = data.get('alipayInShopNumKuan')
                item['总收藏数'] = data.get('inshopItemColNumKuan')
                item['总购物车数'] = data.get('cartNumKuan')
                item['预售成交笔数'] = data.get('prepayInshopNumKuan')
                item['预售成交金额'] = data.get('prepayInshopAmtKuan')
                # 新增
                item['直接成交笔数'] = data.get('dirAlipayInShopNumKuan')
                item['直接成交金额'] = data.get('dirAlipayInshopAmtKuan')
                # item['间接成交笔数'] = data.get('indirAlipayInShopNumKuan')
                # item['间接成交金额'] = data.get('indirAlipayInshopAmtKuan')

            else:
                item['成交金额'] = data.get('alipayInshopAmt')
                item['总成交笔数'] = data.get('alipayInShopNum')
                item['总收藏数'] = data.get('inshopItemColNum')
                item['总购物车数'] = data.get('cartNum')
                item['预售成交笔数'] = data.get('prepayInshopNum')
                item['预售成交金额'] = data.get('prepayInshopAmt')
                item['直接成交笔数'] = data.get('dirAlipayInShopNum')
                item['直接成交金额'] = data.get('dirAlipayInshopAmt')
                # item['间接成交笔数'] = data.get('indirAlipayInShopNum')
                # item['间接成交金额'] = data.get('indirAlipayInshopAmt')
        else:
            continue

        data_list.append(item)
    return data_list, break_bool


def get_plan_goods_ss(start_date, end_date,  type_, effect, offset=0, unifyType='kuan'):
    '''
    获取计划商品  by day
    :param start_date:
    :param end_date:
    :param df_s:
    :param type_:
    :param effect:
    :param output:
    :return:
    '''
    type_name = list(type_.keys())[0]
    type_value = type_[type_name]
    columns = ['取数时间', '计划ID', '计划名称', '计划开始时间', '计划结束时间', '转化周期', '商品ID', '商品名称',
               '展现量', '点击量', '消耗', '成交金额', '总成交笔数', '总收藏数', '总购物车数']    # , '预售成交笔数', '预售成交金额'
    df_result = pd.DataFrame(columns=columns)
    end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date()
    one_day = datetime.timedelta(days=1)

    date = datetime.datetime.strptime(str(start_date), '%Y-%m-%d').date()

    while date <= end_date:
        page_count = 0
        while True:
            nex_date = date + one_day
            offset = page_count * page_count
            result_list, break_bool = get_plan_good_one(type_value=type_value, start_date=str(date), end_date=str(date), effect=effect, offset=offset, unifyType=unifyType)
            if result_list:
                df_result = df_result.append(result_list)
            date = nex_date
            print('开始时间',date,'截止时间：',end_date)
            page_count += 1
            time.sleep(2)
            print(break_bool)
            if break_bool:
                break
    output = f'data/营销策略中心计划商品列表-{type_name}.xlsx'
    df_result.to_excel(output, index=False)


def get_plan_goods_no_byday(start_date, end_date,  type_, effect, unifyType='kuan'):
    '''
    获取计划商品  by day
    :param start_date:
    :param end_date:
    :param df_s:
    :param type_:
    :param effect:
    :param output:
    :return:
    '''
    type_name = list(type_.keys())[0]
    type_value = type_[type_name]
    columns = ['取数时间', '计划ID', '计划名称', '计划开始时间', '计划结束时间', '转化周期', '商品ID', '商品名称', 'launchTime',
               '展现量', '点击量', '消耗', '成交金额', '总成交笔数', '总收藏数', '总购物车数']        # , '预售成交笔数', '预售成交金额'
    df_result = pd.DataFrame(columns=columns)

    end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date()

    date = datetime.datetime.strptime(str(start_date), '%Y-%m-%d').date()
    if date <= end_date:
        page_count = 0
        while True:
            offset = page_count * pageSize
            result_list, break_bool = get_plan_good_one(type_value=type_value, start_date=str(date), end_date=str(end_date), effect=effect, offset=offset, unifyType=unifyType)
            if result_list:
                df_result = df_result.append(result_list)
            page_count += 1
            time.sleep(2)
            print('break_bool',break_bool)
            if break_bool:
                break

    output = f'data/营销策略中心计划商品列表-{type_name}.xlsx'
    df_result.to_excel(output, index=False)


if __name__ == '__main__':


    error_list = []
    print("程序执行开始-----》")
    # cook = get_cookies_from_chrome()
    cookie = ''
    headers['cookie'] = cookie

    effect = '15'  # 15天转化(默认 15天）
    # 通用
    type_list = [
        {'拉新快': 'adStrategyDkx'},
        # {'会员快': 'adStrategyRuHui'},
        {'上新快': 'adStrategyShangXin'},
        {'活动加速': 'adStrategyYuRe'},
        # {"获客易": "adStrategyLiuZi"},
        # {'货品加速': 'adStrategyProductSpeed'},
        # {'爆发收割': 'adStrategyBaoFa'},
    ]

    start_date = datetime.date(2022, 9, 1)
    end_date = datetime.date(2022, 9, 28)


    pageSize = 60
    timeStr, dynamicToken, csrfID = get_params(cookie, key_words="tuijian")
    # 全渠道 unifyType = 'kuan'   末次归因需要传入 unifyType = 'zhai'
    for type_ in type_list:
        # byday
        get_plan_goods_ss(start_date=start_date, end_date=end_date,effect=effect,  type_=type_, unifyType='zhai')

        # get_plan_goods_no_byday(start_date=start_date, end_date=end_date,effect=effect, type_=type_, unifyType='zhai')

    print("数据采集结束-----》正在文件保存")
    combine()
    print("程序执行完毕------》文件合并完毕")
    print("error!!!!!!!!", '单个计划商品数据出现多个', error_list)
    # send_msg("营销策略中心数据完成啦，请发送给需要的人哦")








