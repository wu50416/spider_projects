# -*- coding: UTF-8 -*-
'''
@Project ：法拍 
@File ：analysis_RMFYSS.py
@Author ：hao
@Date ：2023/1/9 15:12 
'''
import re
import time

from loguru import logger
from wbh_word.Dispose_data import Dispose_time
from wbh_word.manage_data import manage_mongo, manage_mysql
from lxml import html
etree = html.etree

# Mongo_table -> MySql_table
Mongo_table = "wbh_ICBC_detail"
MySql_table = "wbh_ICBC_data"
All_dict = {}           # 所有的数据(第一次解析的数据)     status_analysis = 1
Update_dict = {}        # 需要更新的数据Mysql_Update_dict
Mongo_data_dict = {}
logger.add("/home/wangdong/fp_spider/ICBC_Script/logger/Analysis_ICBC.log", filter=lambda record: record["extra"]["name"] == "Analysis_ICBC")
logger_data = logger.bind(name="Analysis_ICBC")
def get_data():
    '''
        status_analysis = 1 : 未解析
        status_analysis = 2 : 已解析但需要更新数据
        status_analysis = 0 : 已解析而且不再需要更新
        status_Update = 1 : 需要更新
        status_Update = 0 : 不需要再更新
    '''
    # $lt（小于）， $gt（大于）， $lte（小于等于）， $gte（大于等于）， $ne（不等于）
    mongo_find_dict = {"status_analysis": {"$ne":0}}        # 获取 status_analysis ！= 0 数据
    results = manage_mongo.read_one_where_data(Mongo_table,mongo_find_dict)
    return results

'''
    状态码：
    2：未开始（公告中）
    3：已撤回（暂未遇到）
    4：拍卖中
    9：已流拍
    
    11：竞买结束
    18：变卖中
    
    
    25：已撤拍  （一般都是用25）

'''



def dispose_detail_html(detail_html):           # 处理基础html数据
    etr = etree.HTML(detail_html)
    dl_list = etr.xpath(r'//*[@id="subjectMatter"]/dl')
    # print(files)
    PaimaiTimes = ''.join(dl_list[0].xpath(r'./dd/text()')).replace(' ', '').replace('\t', '').replace('\n', '')
    City = ''.join(etr.xpath(r'//li[@class="omit"]/text()')).replace(' ', '').replace('\t', '').replace('\n', '')
    StartPrice = ''.join(etr.xpath(r'//dd[@id="onsetMoney"]/@title')).replace(',', '').replace('￥', '')         # 起拍价
    PriceLowerOffset = ''.join(etr.xpath(r'//dd[@id="keySei"]/@title')).replace(',', '').replace('￥', '')         # 加价幅度
    EnsurePrice = ''.join(dl_list[5].xpath(r'./dd/@title')).replace(',', '').replace('￥', '')                     # 保证金

    AssessmentPriceStr = ''.join(dl_list[6].xpath(r'./dd/@title')).replace(',', '').replace('￥', '')              # 评估价
    if len(AssessmentPriceStr) == 0:
        AssessmentPriceStr = 0

    Disposal = ''.join(etr.xpath(r'//h5[@id="goToCourt"]/@title')).replace(',', '').replace('￥', '')   # 处置方
    ContactInfo = etr.xpath(r'//div[@class="reg_x clear"]/dl[@class="clear"]/dd/@title')[0]             # 联系人
    Telephone = etr.xpath(r'//div[@class="reg_x clear"]/dl[@class="clear"]/dd/@title')[0]               # 联系方式



    NoticeUrl = etr.xpath(r'//*[@id="div_notice_gfword"]')[0]  # 竞买须知
    Notice_html = etree.tostring(NoticeUrl, encoding='utf8').decode()

    DescUrl = etr.xpath(r'//div[@class="p_word  rygtable"]')[0]  # 标的物介绍
    DescUrl_html = etree.tostring(DescUrl, encoding='utf8').decode()

    GongGaoUrl = etr.xpath(r'//*[@id="div_announcement_gfword"]')[0]  # 竞买公告
    GongGaoUrl_html = etree.tostring(GongGaoUrl, encoding='utf8').decode()

    GovAttachLists = etr.xpath(r'//ul/p/a/@href')           # 相关附件
    GovAttachList = []
    for link in GovAttachLists:
        url = 'https://gf.trade.icbc.com.cn' + link
        GovAttachList.append(url)
    GovAttachList = ';'.join(GovAttachList)

    if '<div class="pai_title_text">竞买成功确认书</div>' in detail_html:      # 是否有成交确认书
        ShowSfDealConfirm = 1
        ShowSfDealConfirm_xpath = etr.xpath(r'//div[@class="c-sx-dl dt-w80 "]')[0]           # 成交确认书
        ShowSfDealConfirm_html = etree.tostring(ShowSfDealConfirm_xpath, encoding='utf8').decode()
    else:
        ShowSfDealConfirm = 0
        ShowSfDealConfirm_html = None




    casual_save_dict = {'StartPrice':StartPrice,'AssessmentPriceStr':AssessmentPriceStr,'EnsurePrice':EnsurePrice,'PriceLowerOffset':PriceLowerOffset,
                         'PaimaiTimes':PaimaiTimes,'City':City,'Disposal':Disposal,'ContactInfo':ContactInfo,'Telephone':Telephone,
                         'GovAttachList':GovAttachList,'ShowSfDealConfirm':ShowSfDealConfirm}

    # 更新：附件、成交确认书
    casual_update_dict = {'GovAttachList':GovAttachList,'ShowSfDealConfirm':ShowSfDealConfirm}

    # 竞买须知、标的物介绍、竞买公告、竞买成功确认书(Mongo是需要更新)
    casual_mongo_dict = {'Notice_html':Notice_html,'DescUrl_html':DescUrl_html,'GongGaoUrl_html':GongGaoUrl_html,'ShowSfDealConfirm_html':ShowSfDealConfirm_html}


    All_dict.update(casual_save_dict)
    Update_dict.update(casual_update_dict)
    Mongo_data_dict.update(casual_mongo_dict)


    # return Mysql_All_dict,Mysql_Update_dict,Mongo_data_dict


def dispose_NewDateNew(NewDateNew):
    '''
    这部分全部都是需要更新的
    延时次数,开始时间，结束时间，当前价格, 竞买次数（totalCountSf）
    {"historyMap":{"recordBidHistoryList":[{"pageCountSf":2,"pageSizeSf":10,"totalCountSf":13,"bidTime":"08.31 10:13:16","price":164140,"pageIndexSf":1,"bidHistoryId":"20190831101316092166","id":"T9907","time":"2019年08月31日 10:13:16"},{"bidTime":"08.31 10:11:12","price":162140,"bidHistoryId":"20190831101112092056","id":"S2497","time":"2019年08月31日 10:11:12"},{"bidTime":"08.31 10:09:27","price":160140,"bidHistoryId":"20190831100927092172","id":"T9907","time":"2019年08月31日 10:09:27"},{"bidTime":"08.31 10:09:01","price":158140,"bidHistoryId":"20190831100901092165","id":"S2497","time":"2019年08月31日 10:09:01"},{"bidTime":"08.31 10:05:29","price":156140,"bidHistoryId":"20190831100529092110","id":"T9907","time":"2019年08月31日 10:05:29"},{"bidTime":"08.31 10:04:26","price":154140,"bidHistoryId":"20190831100426092081","id":"S2497","time":"2019年08月31日 10:04:26"},{"bidTime":"08.31 10:01:54","price":152140,"bidHistoryId":"20190831100154092109","id":"T9907","time":"2019年08月31日 10:01:54"},{"bidTime":"08.31 09:59:38","price":150140,"bidHistoryId":"20190831095938091981","id":"S2497","time":"2019年08月31日 09:59:38"},{"bidTime":"08.31 09:58:44","price":148140,"bidHistoryId":"20190831095844092101","id":"T9907","time":"2019年08月31日 09:58:44"},{"bidTime":"08.31 09:57:21","price":146140,"bidHistoryId":"20190831095721092099","id":"S2497","time":"2019年08月31日 09:57:21"}]},"getNewDataFromWebFlag":"1","basicMap":{"nowDate":"2023-01-11 17:34:23","showTime":"08月31日  10:18","prodId":"B000445087","endPrice":"164140.00","bidControlType":"1","quoteType":"0","biddingBeginDate":"2019-08-30 10:00:00","endTimeDate":"2019-08-31 10:18:16","timeAndStatusFlag":"1","downTimeForMobile":0,"completeTimeDate":"2019-08-31 10:18:17","announcementBeginDate":"2019-07-24 13:30:00","roadShow":"0","tradeStatus":"22","delayTime":10,"endTime":0,"tradeId":"201907240000609101","statusUpdateTime":"2019-09-10 11:30:00","endDateStr":"2019-08-31 10:18:16"}}
    '''
    StartTime = NewDateNew['basicMap']['biddingBeginDate']                    # 开始时间
    EndTime = NewDateNew['basicMap']['endTimeDate']                           # 结束时间
    DelayedCount = NewDateNew['basicMap']['delayTime']                        # 延时次数
    CurrentPriceStr = NewDateNew['basicMap']['endPrice']                      # 当前价
    BidStatus = NewDateNew['basicMap']['tradeStatus']                         # 交易状态

    casual_dict = {'CurrentPriceStr':CurrentPriceStr,'StartTime':StartTime,'EndTime':EndTime,'DelayedCount':DelayedCount,'BidStatus':BidStatus}

    All_dict.update(casual_dict)
    Update_dict.update(casual_dict)





def dispose_visitorCount(visitorCount):
    '''
    解析：0人报名 ,1人设置提醒 ,324次围观
    visitorCount : {"visitorCount":"324","signUpNum":"0","tendencyNum":"0","remindPPNum":"1"}
    '''
    FollowerCount = visitorCount['remindPPNum']      # 关注提醒人数
    AccessNum = visitorCount['visitorCount']         # 围观人数
    AccessEnsureNum = visitorCount['signUpNum']      # 报名人数

    casual_dict = {'FollowerCount':FollowerCount,'AccessNum':AccessNum,'AccessEnsureNum':AccessEnsureNum}

    All_dict.update(casual_dict)
    Update_dict.update(casual_dict)






def run():
    Mongo_data_list = get_data()
    index = 1
    for Mongo_dict in Mongo_data_list:
        detail_html = Mongo_dict['detail_html']
        NewDateNew = Mongo_dict['NewDateNew']
        visitorCount = Mongo_dict['visitorCount']
        ItemID = Mongo_dict['ItemID']
        Title = Mongo_dict['title']
        Mongo_update_time = Mongo_dict['update_time']  # Mongo的最后更新时间
        status_Update = Mongo_dict['status_Update']
        status_analysis = Mongo_dict['status_analysis']

        dispose_detail_html(detail_html)      # 接触详情页的html
        dispose_NewDateNew(NewDateNew)
        dispose_visitorCount(visitorCount)


        casual_dict = {'ItemID':ItemID,'Title':Title,'Mongo_update_time':Mongo_update_time}       # 临时，从Mongo上获取的数据
        All_dict.update(casual_dict)
        casual_dict = {'Mongo_update_time':Mongo_update_time}           # 更新时间
        Update_dict.update(casual_dict)

        Mysql_Save_dict = [All_dict]
        Mysql_Update_dict = [Update_dict]
        Mongo_Update_dict = Mongo_data_dict     # Mongo的数据是一定会更新的
        # print(Mysql_Save_dict)
        # print(Mysql_Update_dict)
        # print(Mongo_data_dict.keys())

        Mysql_where_dict = [{'ItemID':ItemID}]
        Mongo_where_dict = {'ItemID':ItemID}


        if status_analysis == 1:  # 是否是第一次解析，是否是需要第一次入Mysql
            if status_Update == 1:
                analysis = 2                                            # 1 -> 2        ,后续需要继续更新
            else:                                                       # status_Update == 0
                analysis = 0                                            # 1 -> 0        ，后续无需再更新
            Mysql_Save_dict[0]['status_analysis'] = analysis
            Mongo_Update_dict['status_analysis'] = analysis
            manage_mysql.save_data(MySql_table,Mysql_Save_dict)    # 入Mysql库
            manage_mongo.Update_mongodb_data(Mongo_table, Mongo_where_dict, Mongo_Update_dict)
        elif status_analysis == 2:          # 已解析过了，但需要更新数据
            if status_Update == 0:                                      # 2 -> 0        ,后续无需再更新,否则 2 -> 2 ,任然需要更新
                analysis = 0
            else:
                analysis = status_analysis                               # 2 -> 2        ,后续需要继续更新
            Mysql_Update_dict[0]['status_analysis'] = analysis
            Mongo_Update_dict['status_analysis'] = analysis
            manage_mysql.update_data(MySql_table,Mysql_Update_dict,Mysql_where_dict)
            manage_mongo.Update_mongodb_data(Mongo_table, Mongo_where_dict, Mongo_Update_dict)
        logger_data.info(f"正在解析第 {index} 条数据 , ItemID ： {ItemID} status_analysis： {status_analysis} -> {analysis}")
        index += 1
        # time.sleep(10)


if __name__ == '__main__':
    run()

