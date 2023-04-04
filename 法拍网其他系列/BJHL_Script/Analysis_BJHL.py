# -*- coding: UTF-8 -*-
'''
@Project ：法拍 
@File ：Analysis_BJHL.py
@Author ：hao
@Date ：2023/1/13 10:02 
'''
import datetime
import re
import time

from loguru import logger
from wbh_word.Dispose_data import Dispose_time
from wbh_word.manage_data import manage_mongo, manage_mysql
from lxml import html

etree = html.etree



# Mongo_table -> MySql_table
Mongo_table = "wbh_BJHL_detail"
MySql_table = "wbh_BJHL_data"
All_dict = {}  # 所有的数据(第一次解析的数据)     status_analysis = 1
Update_dict = {}  # 需要更新的数据Mysql_Update_dict
Mongo_data_dict = {}
logger.add("/home/wangdong/fp_spider/BJHL_Script/logger/Analysis_BJHL.log",filter=lambda record: record["extra"]["name"] == "Analysis_BJHL")
logger_data = logger.bind(name="Analysis_BJHL")

def get_data():
    '''
        status_analysis = 1 : 未解析
        status_analysis = 2 : 已解析但需要更新数据
        status_analysis = 0 : 已解析而且不再需要更新
        status_Update = 1 : 需要更新
        status_Update = 0 : 不需要再更新
    '''
    # $lt（小于）， $gt（大于）， $lte（小于等于）， $gte（大于等于）， $ne（不等于）
    mongo_find_dict = {"status_analysis": {"$ne": 0}}  # 获取 status_analysis ！= 0 数据
    results = manage_mongo.read_one_where_data(Mongo_table, mongo_find_dict)
    return results


'''
结束状态确认：1、prjBidInfo中有无 “结束时间” 文字   2、 如果无，结束条件： 当前时间 > 结束时间+竞价周期+额外加10天时间
base_url(html格式) : 基础数据、竞买须知、标的物介绍、竞买公告     注意这里是get请求
prjBidInfo_url : 主要用于判断是否结束（if "结束时间！" in html）     当前价用 bidInfo_url
bidInfo_url : '最高报价': '44621217', '延时次数': '155', '竞价次数': '341', '状态': '成交'      注意，这里请求还需要携带 data = {'cpdm': xmid, 'jjcc': 1}
detailInfo_url : '报名人数': 31, '关注人数': 79, '围观人数': 35579
priorityPsn_url : 优先购买权人（if "无优先购买权人信息！" in html）
cjqrs_url : 成交确认书
'''


def dispose_detail_html(detail_html):  # 处理基础html数据
    etr = etree.HTML(detail_html)

    PaimaiTimes = ''.join(etr.xpath(r'//div[@class="main"]/div[2]//p[@class="bd_detail_name"]/text()')).replace(' ', '').replace('\n', '')
    PaimaiTimes = re.findall('【(.*?)】', PaimaiTimes)[0]                 # 第几拍（一拍、二拍、变卖）


    '''
    bd_detail_right_list : 列表： [0]:标的公告，[1]：处置单位，[2]：联系方式(咨询方、电话)
    '''
    bd_detail_right_list = etr.xpath(r'//div[@class="bd_detail_right"]//tr')
    Disposal = bd_detail_right_list[1].xpath(r'td/text()')[0]                                  # 处置方
    ContactInfo = bd_detail_right_list[2].xpath(r'./td/text()')[0].replace(' ', '').replace('\n', '')  # 咨询方
    Telephone = bd_detail_right_list[2].xpath(r'./td//p/text()')[0]                             # 电话


    p_list = etr.xpath(r'//p[@class="mt10"]')
    Address = ''
    City = ''
    Loan = 1
    GovAttachList = []  # 附件

    for p in p_list:
        files = ''.join(p.xpath(r'./text()')).replace(' ', '').replace('\n', '')
        if '标的物所在地：' in files:
            City += files.replace('标的物所在地：', '')        # 城市
            Address += files.replace('标的物所在地：', '')      # 标的物地址
        elif '标的物位置：' in files:
            Address += files.replace('标的物位置：', '')
        elif '贷款' in files:
            if '不' in files:        # 是否贷款
                Loan = 0
        elif '附件' in files:
            a_list = p.xpath(r'.//a/@href')
            for k in a_list:
                link = 'https://otc.cbex.com' + k
                GovAttachList.append(link)
    GovAttachList = ';'.join(GovAttachList)


    NoticeUrl = etr.xpath(r'//pre[@id="content_bidnotice"]')[0]      # 竞买须知      //pre[@id="content_bidnotice"]
    NoticeUrl = etree.tostring(NoticeUrl, encoding='utf8').decode()

    DescUrl = etr.xpath(r'//div[@id="bd_detail_tab_ct3"]')[0]        # 标的物介绍      /pre[@id="content_item_description"]
    DescUrl = etree.tostring(DescUrl, encoding='utf8').decode()

    GongGaoUrl = etr.xpath(r'//pre[@id="content_ggdetail"]')[0]      # 竞买公告      /pre[@id="content_item_description"]
    GongGaoUrl = etree.tostring(GongGaoUrl, encoding='utf8').decode()


    info_dict = {}                  # 起拍价 、 评估价 、 保证金 、 加价幅度
    li_list = etr.xpath(r'//div[@class="main"]//div[@class="bd_detail_info"]/ul/li')
    for li in li_list[:3]:
        key = li.xpath(r'./span[@class="jjfd"]/text()')
        key = ''.join(key).replace(': ', '').replace(' ', '')
        value = li.xpath(r'./span[@class="jjfd"]/span[@class="title_tip"]/text()')
        value = ''.join(value).replace('\n', '').replace('¥', '').replace(' ', '').replace(',', '')
        key1 = li.xpath(r'./span[@class="fwf"]/text()')
        key1 = ''.join(key1).replace(': ', '').replace(' ', '')
        value1 = li.xpath(r'./span[@class="fwf"]/span[@class="title_tip"]/text()')
        value1 = ''.join(value1).replace('\n', '').replace('¥', '').replace(' ', '').replace(',', '')
        dd = {'起拍价': 'StartPrice', '评估价': 'AssessmentPriceStr', '保证金': 'EnsurePrice', '加价幅度': 'PriceLowerOffset'}
        if len(value) == 0:
            value = 0
        if len(value1) == 0:
            value1 = 0
        try:
            info_dict[dd[key]] = value
        except:
            pass
        try:
            info_dict[dd[key1]] = value1
        except:
            pass

    # print(f'info_dict : {info_dict}')


    casual_save_dict = {'PaimaiTimes':PaimaiTimes,'Disposal':Disposal,'ContactInfo':ContactInfo,'Telephone':Telephone,'City':City,'Address':Address,
                        'Loan':Loan,'GovAttachList':GovAttachList}
    casual_save_dict.update(info_dict)


    # casual_update_dict = {}         # 详情页数据不需要更新
    # 竞买须知、标的物介绍、竞买公告                       # 、竞买成功确认书(Mongo是需要更新)
    casual_mongo_dict = {'NoticeUrl':NoticeUrl,'DescUrl':DescUrl,'GongGaoUrl':GongGaoUrl}


    All_dict.update(casual_save_dict)
    # Update_dict.update(casual_update_dict)            # 本页面不需要更新
    Mongo_data_dict.update(casual_mongo_dict)




def dispose_prjBidInfo(prjBidInfo):
    '''
    # 用于获取状态
    1、  即将开始 开始时间： 2023年 02月 06日 10:00
        起拍价： ￥1,354,989.00 　
        参与报价
    2、  竞价中
        当前价： ￥1,400,000.00
        起拍价： ￥1,400,000.00　　
        参与报价
    3、  已结束 结束时间： 2019年 09月 29日 11:01:08
        75 次延时
        竞价结束。
        最高报价金额： ￥3,592,050.00
    4、  已撤回
        本标的物已撤回。
        撤回原因：录入信息有误，撤回重新发布
    5、  本标的物已竞价暂停。
        暂停原因：
    6、  已流拍
        标的物已流拍。
    7、  已中止
        本标的物已中止。
        中止原因：案外人异议
    '''
    yes_no = re.findall(r'结束时间', prjBidInfo)
    EndTime = None      # 默认为None
    if len(yes_no) > 0:
        end_time = re.findall('<span class="time_num">(.*?)</span>', prjBidInfo)
        EndTime = '-'.join(end_time[0:-1]) + ' ' + end_time[-1]                                     # 结束时间
    StartTime = re.findall('.html(.*?);', prjBidInfo)[0].replace("('", '').replace("')", '')        # 开始时间
    if not StartTime:
        etr = etree.HTML(prjBidInfo)
        start_times = etr.xpath(r'//span[@class="time_num"]//text()')           # ['2023', '01', '19', '10:00']
        start_s = start_times[-1].split(':')            # ['10', '00']
        StartTime = datetime.datetime(int(start_times[0]), int(start_times[1]), int(start_times[2]), int(start_s[0]),int(start_s[1]))
    try:
        BidStatus = re.findall('<span class="state_mark xmztz_cls">(.*?)</span>', prjBidInfo)[0]  # 拍卖状态（中文）
    except:
        BidStatus = re.findall('<span class="state_mark_short xmztz_cls ">(.*?)</span>', prjBidInfo)[0]
    try:
        Remarks = re.findall('<p class="fs16 lh20 wsn" data-value="\d">(.*?)</p>', prjBidInfo)[0]          # 状态：data-value=     后面接多种数字
    except:
        Remarks = None


    casual_dict = {'StartTime':StartTime,'EndTime':EndTime,'BidStatus':BidStatus,'Remarks':Remarks}
    # print(casual_dict)
    All_dict.update(casual_dict)
    Update_dict.update(casual_dict)

def dispose_bidInfo(bidInfo):
    '''
    item_id : 8DBE7D3C3ADEA96F62BD4F0895BC9993
    {"code":"","msg":"","object":{"dateTime":"1673579955000","JJCC":"","JJMS":"","KHH":"000120119990","FID_CSDM":"","ZXJ":"3592050","ZXBJRQ":"","FID_KZSX":"",
    "FID_QYCS":"","ZXBJSJ":"","fixTakeTime":"2","STAMP":"0","ZDBJ":"2542050","ZGBJ":"0","FID_SQRQ":"","ZDJ":"3592050","TODAY":"20230113","FID_YDBZ":"",
    "TIME":"11:19:15","FID_LJWYCS":"","FID_SQDW":"","JYZT":"400","FID_CKCS":"75","JYZTSM":"成交","WTXX":"","ZDWTJ":"3602050","FID_SQSJ":"","CJJJ":"3592050",
    "COUNT":"89","style":"cj","ZGJ":"3592050"},"success":true}
    '''
    CurrentPriceStr = bidInfo['object']['ZGJ']      # 当前价（最高价）
    DelayedCount = bidInfo['object']['FID_CKCS']       # 延时次数
    BidCount = bidInfo['object']['COUNT']              # 竞买次数
    # BidStatus = bidInfo['object']['JYZTSM']            # 拍卖状态 （这个会不太准确,需要使用prjBidInfo中数据）


    casual_dict = {'CurrentPriceStr':CurrentPriceStr,'DelayedCount':DelayedCount,'BidCount':BidCount}

    All_dict.update(casual_dict)
    Update_dict.update(casual_dict)

def dispose_detailInfo(detailInfo):
    '''
    {"code":"","msg":"","object":{"bmrs":1,"sfgz":0,"gzrs":6,"wgcs":10504},"success":true}
    '''
    AccessEnsureNum = detailInfo['object']['bmrs']          # 报名人数
    FollowerCount = detailInfo['object']['gzrs']            # 关注提醒人数
    AccessNum = detailInfo['object']['wgcs']                # 围观数

    casual_dict = {'AccessEnsureNum':AccessEnsureNum,'FollowerCount':FollowerCount,'AccessNum':AccessNum}
    All_dict.update(casual_dict)
    Update_dict.update(casual_dict)

def dispose_priorityPsn(priorityPsn):
    '''
    顺位	姓名
    无优先购买权人信息！
    '''
    if '无优先购买权人' in priorityPsn:
        ShowName = 0                # 是否有优先购买权人
    else:
        ShowName = 1

    casual_dict = {'ShowName':ShowName}


    All_dict.update(casual_dict)
    Update_dict.update(casual_dict)

def dispose_cjqrs(cjqrs):
    '''
    网络竞价成功确认书
    处置单位：
    标的物名称：
    标的物网拍链接：https://otc.cbex.com/sfpm/detail/.htm
    网拍公告时间：
    网拍开始时间：
    网拍结束时间：\n \njavax.servlet.jsp.JspException: In <parseDate>, value attribute can not be parsed: \" \"\n",
    '''
    if '【网络竞价结果】' in cjqrs:
        ShowSfDealConfirm = 1           # 是否有成交确认书
    else:
        ShowSfDealConfirm = 0

    # print(f'ShowSfDealConfirm: {ShowSfDealConfirm} ')

    casual_dict = {'ShowSfDealConfirm':ShowSfDealConfirm}
    All_dict.update(casual_dict)
    Update_dict.update(casual_dict)




def run():
    Mongo_data_list = get_data()
    index = 1
    for Mongo_dict in Mongo_data_list:
        ItemID = Mongo_dict['item_id']
        xmid = Mongo_dict['xmid']
        Title = Mongo_dict['title']
        detail_html = Mongo_dict['base_data']
        prjBidInfo = Mongo_dict['prjBidInfo_data']
        bidInfo = Mongo_dict['bidInfo_data']
        detailInfo = Mongo_dict['detailInfo_data']
        priorityPsn = Mongo_dict['priorityPsn_data']
        cjqrs = Mongo_dict['cjqrs_data']

        Mongo_update_time = Mongo_dict['update_time']  # Mongo的最后更新时间
        status_Update = Mongo_dict['status_Update']
        status_analysis = Mongo_dict['status_analysis']

        # print('ItemID : ', ItemID)
        dispose_detail_html(detail_html)  # 接触详情页的html
        dispose_prjBidInfo(prjBidInfo)
        dispose_bidInfo(bidInfo)
        dispose_detailInfo(detailInfo)
        dispose_priorityPsn(priorityPsn)
        dispose_cjqrs(cjqrs)


        casual_dict = {'ItemID': ItemID,'xmid':xmid, 'Title': Title, 'Mongo_update_time': Mongo_update_time}  # 临时，从Mongo上获取的数据
        All_dict.update(casual_dict)
        casual_dict = {'Mongo_update_time': Mongo_update_time}  # Mongo数据的更新时间
        Update_dict.update(casual_dict)

        Mysql_Save_dict = [All_dict]
        Mysql_Update_dict = [Update_dict]
        Mongo_Update_dict = Mongo_data_dict  # Mongo的数据是一定会更新的
        # print(Mysql_Save_dict)
        # print(Mysql_Update_dict)
        # print(Mongo_data_dict.keys())

        Mysql_where_dict = [{'ItemID': ItemID,'xmid':xmid}]
        Mongo_where_dict = {'item_id': ItemID,'xmid':xmid}


        if status_analysis == 1:  # 是否是第一次解析，是否是需要第一次入Mysql
            if status_Update == 1:
                analysis = 2  # 1 -> 2        ,后续需要继续更新
            else:  # status_Update == 0
                analysis = 0  # 1 -> 0        ，后续无需再更新
            Mysql_Save_dict[0]['status_analysis'] = analysis
            Mongo_Update_dict['status_analysis'] = analysis
            manage_mysql.save_data(MySql_table, Mysql_Save_dict)  # 入Mysql库
            manage_mongo.Update_mongodb_data(Mongo_table, Mongo_where_dict, Mongo_Update_dict)
        elif status_analysis == 2:  # 已解析过了，但需要更新数据
            if status_Update == 0:  # 2 -> 0        ,后续无需再更新,否则 2 -> 2 ,任然需要更新
                analysis = 0
            else:
                analysis = status_analysis  # 2 -> 2        ,后续需要继续更新
            Mysql_Update_dict[0]['status_analysis'] = analysis
            Mongo_Update_dict['status_analysis'] = analysis
            manage_mysql.update_data(MySql_table, Mysql_Update_dict, Mysql_where_dict)
            manage_mongo.Update_mongodb_data(Mongo_table, Mongo_where_dict, Mongo_Update_dict)
        logger_data.info(f"第 {index} 条数据 解析成功！！ ItemID ： {ItemID} ,xmid : {xmid} status_analysis： {status_analysis} -> {analysis}")
        index += 1
        # time.sleep(10)


if __name__ == '__main__':
    run()


