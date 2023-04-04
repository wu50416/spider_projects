# -*- coding: UTF-8 -*-
'''
@Project ：法拍 
@File ：analysis_JD.py
@Author ：hao
@Date ：2022/12/12 10:45 
'''
import re
from loguru import logger
from wbh_word.Dispose_data import Dispose_time
from wbh_word.manage_data import manage_mongo, manage_mysql


'''
    Mongo  ->  Mysql        将mongo数据提取至mysql
'''
Mongo_table = "wbh_JD_details_new"
MySql_table = "wbh_JD_data"
all_dict = {}           # 所有的数据
Update_dict = {}        # 需要更新的数据


logger.add("D:/yj_pj/法拍/BLZC/JD/logger/Analysis_data.log", filter=lambda record: record["extra"]["name"] == "get_data")
logger_data = logger.bind(name="get_data")
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

def get_searchLabel_id(searchLabel_Name):
    # 资产性质
    # searchLabel = {"labelId": 1027, "labelName": "诉讼资产"}, {"labelId": 1028, "labelName": "刑案资产"}, {"labelId": 1029,"labelName": "破产资产"}, {"labelId": 1030, "labelName": "海关罚没"}, {"labelId": 1039, "labelName": "政府罚没"}, {"labelId": 1031,"labelName": "国有资产"}, {"labelId": 1032, "labelName": "商业资产"}, {"labelId": 1033, "labelName": "金融资产"}
    searchLabel_dict = {'诉讼资产': 1027, '刑案资产': 1028, '破产资产': 1029, '海关罚没': 1030, '政府罚没': 1039, '国有资产': 1031, '商业资产': 1032, '金融资产': 1033}
    searchLabel_id = searchLabel_dict[searchLabel_Name]
    return searchLabel_id

def get_searchCategory_id(searchCategory_name):
    # 标的物类型：
    searchCategory_dict = {'住宅用房': 101, '商业用房': 102, '工业用房': 103, '其他用房': 104, '机动车': 105, '船舶': 106, '其他交通运输工具': 107,'股权': 108, '债权': 109, '矿权': 110, '林权': 111, '土地': 112, '工程': 113, '机械设备': 114, '无形资产': 115,'知识产权': 116, '租赁/经营权': 117, '奢侈品': 118, '生活物资': 119, '工业物资': 120, '库存物资': 121, '打包处置': 122,'其他财产': 123}
    searchCategory_id = searchCategory_dict[searchCategory_name]
    return searchCategory_id

def get_auctionStatus_name(auctionStatus_id):
    auctionStatus_id = int(auctionStatus_id)
    auctionStatus_dict = {0:'预告',1:'进行中',2:'已结束'}
    auctionStatus_name = auctionStatus_dict[auctionStatus_id]
    return auctionStatus_name

def get_displayStatus_name(displayStatus_id):
    displayStatus_id = int(displayStatus_id)
    displayStatus_dict = {1:'无异常',7:'已终止',5:'已撤回',6:'已暂缓'}
    displayStatus_name = displayStatus_dict[displayStatus_id]
    return displayStatus_name

def get_paimaiTimes_name(paimaiTimes_id):           # 有些没有paimaiTimes字段
    paimaiTimes_id = int(paimaiTimes_id)
    paimaiTimes_dict = {0:None,1:'一拍',2:'二拍',4:'变卖',6:'破产'}
    paimaiTimes_name = paimaiTimes_dict[paimaiTimes_id]
    return paimaiTimes_name

def get_req_url(req_id):
    '''
        req_id 共有三种参数（item_id，albumId，courtVendorId），使用前先确保传参是否正确！！！！！
        1、获取基础数据 getProductBasicInfo                  获取 albumId （请求拍卖公告的一个参数）
        2、获取标的物详情（标的物介绍） queryProductDescription
        3、获取标的物介绍 附件 queryAttachFilesForIntro
        4、获取拍卖公告（竞买公告） queryAnnouncement  注意！！ 这里要用到 base中的 albumId
        5、获取拍卖须知（竞买须知） queryNotice
        6、获取出价记录、报名数 getPaimaiRealTimeData           获取成交价、报名数、确认是否结束    注意：无关注提醒            # confirmationUrl 成交确认书
        # getPaimaiRealTimeData                 这个接口替换掉了原本的Price_url
        7、获取围观数、关注提醒 paimai_getPaimaiDetaiExpandValues
        8、获取处置方信息 queryVendorInfo            注意！！ 这里要用到 base中的 courtVendorId
    '''
    req_id = str(req_id)
    Basic_url = 'https://api.m.jd.com/api?appid=paimai&functionId=getProductBasicInfo&body={%22paimaiId%22:' + req_id + '}&loginType=3'
    Description_url = 'https://api.m.jd.com/api?appid=paimai&functionId=queryProductDescription&body={%22paimaiId%22:' + req_id +',%22source%22:0}&loginType=3'
    AttachFiles_url = 'https://api.m.jd.com/api?appid=paimai&functionId=queryAttachFilesForIntro&body={%22custom%22:0,%22paimaiId%22:' + req_id + ',%22source%22:0}&loginType=3'
    Announcement_url = 'https://api.m.jd.com/api?appid=paimai&functionId=queryAnnouncement&body={%22albumId%22:' + req_id + '}&loginType=3'
    Notice_url = 'https://api.m.jd.com/api?appid=paimai&functionId=queryNotice&body={%22paimaiId%22:' + req_id + '}&loginType=3'

    # Price_url = 'https://paimai.jd.com/json/current/englishquery.html?paimaiId='+ req_id +'&start=0&end=9'
    Price_url = 'https://api.m.jd.com/api?appid=paimai&functionId=getPaimaiRealTimeData&body={"paimaiId":'+ req_id +'}&loginType=3'
    DetaiExpand_url = 'https://api.m.jd.com/api?appid=paimai&functionId=paimai_getPaimaiDetaiExpandValues&body={"paimaiId":'+ req_id +'}&loginType=3'
    VendorInfo_url = 'https://api.m.jd.com/api?appid=paimai&functionId=queryVendorInfo&body={"publishSource":7,"vendorId":'+ req_id +'}&loginType=3'

    url_dict = {
        'Basic_url': Basic_url,
        'Description_url':Description_url,
        'AttachFiles_url':AttachFiles_url,
        'Announcement_url':Announcement_url,
        'Notice_url':Notice_url,
        'Price_url':Price_url,
        'DetaiExpand_url':DetaiExpand_url,
        'VendorInfo_url':VendorInfo_url,
    }
    return url_dict




def analysis_Mongo(Mongo_data):         # Mongo原有的数据
    AssetType_name = Mongo_data['searchLabel_Name']         # 资产类型名称
    AssetType = get_searchLabel_id(AssetType_name)          # 资产类型ID
    Type_name = Mongo_data['searchCategory_Name']           # 标的物类型名称
    Type = get_searchCategory_id(Type_name)                 # 标的物类型ID

    this_dict = {"AssetType_name":AssetType_name,"AssetType":AssetType,"Type_name":Type_name,"Type":Type}
    all_dict.update(this_dict)


def analysis_Update_Basic(Basic_response,item_id):     # 基础_需要更新的数据
    Basic_data = Basic_response['data']

    StartPrice = Basic_data['startPrice']       # 起拍价

    AssessmentPriceStr = Basic_data.get('assessmentPrice',None) # 评估价

    # ['assessmentPrice']
    if AssessmentPriceStr == 0:         # 评估价为0:（无评估价）      # 注意，这里与SQL类型冲突，不能为None，需要修改！！！
        AssessmentPriceStr = None

    EnsurePrice = Basic_data['ensurePrice']                 # 保证金
    PriceLowerOffset = Basic_data['priceLowerOffset']       # 加价幅度

    s_time_tf = Basic_data['startTime']                     # 1668909600000
    StartTime = Dispose_time.get_time_data(s_time_tf)           # 开始时间
    e_time_tf = Basic_data['endTime']
    EndTime = Dispose_time.get_time_data(e_time_tf)             # 结束时间


    this_dict = {"StartPrice":StartPrice,"AssessmentPriceStr":AssessmentPriceStr,"EnsurePrice":EnsurePrice,"PriceLowerOffset":PriceLowerOffset,
                 "StartTime":StartTime,"EndTime":EndTime}
    all_dict.update(this_dict)
    Update_dict.update(this_dict)           # 这部分数据需要更新


def analysis_fixed_Basic(Basic_response):
    # 固定不会更新的基础部分的数据
    Basic_data = Basic_response['data']

    ItemID = int(Basic_data['paimaiId'])             # 项目id
    Title = Basic_data['title']                 # 标的名称

    ContactInfo = Basic_data['judicatureBasicInfoResult']['consultName']    # 咨询方
    Telephone = Basic_data['judicatureBasicInfoResult']['consultTel']       # 联系方式

    # "productAddressResult":{"address":"南城区莞太路23号鸿禧商业大厦四楼整层","city":"东莞市","cityId":1655,"county":"东莞市","countyId":1655,"province":"广东","provinceId":19,"town":""}
    Address_data = Basic_data['productAddressResult']
    province = Address_data['province']     # 省
    city = Address_data['city']             # 市
    district = Address_data['county']       # 县
    Address = Address_data['address']       # 具体地址


    albumId = Basic_data['albumId']
    NoticeUrl = get_req_url(ItemID)['Notice_url']          # 竞买须知url
    DescUrl = get_req_url(ItemID)['Description_url']       # 标的物介绍
    GongGaoUrl = get_req_url(albumId)['Announcement_url']   # 竞买公告  注意！！ 这里要用到 base中的 albumId


    this_dict = {"ItemID":ItemID,"Title":Title,"ContactInfo":ContactInfo,"Telephone":Telephone,"province":province,"city":city,
                 "district":district,"Address":Address,"NoticeUrl":NoticeUrl,"DescUrl":DescUrl,"GongGaoUrl":GongGaoUrl}
    all_dict.update(this_dict)


def analysis_AttachFiles(AttachFiles_response):     # 3、获取标的物介绍 附件
    '''
    {"code":0,"data":[{"attachmentAddress":"https://storage.jd.com/auction.gateway/ATTACHMENT_a7b40319c475442bb01b2fb79a8d76bb.pdf","attachmentCode":"ATTACHMENT_8360489484b94d1c883148663c460eb3_1670572930587","attachmentFormat":"pdf","attachmentName":"JEEP检测报告.pdf","attachmentSize":"8991522","attachmentStyle":"2","attachmentType":"3","code":"10023540289018","evtId":292793815,"isDeleted":0}],"message":"成功","status":0}
    '''
    AttachFiles_dataList = AttachFiles_response['data']
    if AttachFiles_dataList:                        # 附件
        url_list = []
        for data in AttachFiles_dataList:
            attachmentAddress_url = data['attachmentAddress']
            url_list.append(attachmentAddress_url)
        GovAttachList = ';'.join(url_list)
    else:
        GovAttachList = None

    this_dict = {"GovAttachList":GovAttachList}
    all_dict.update(this_dict)


# {'code': 0, 'data': {'accessEnsureNum': 0, 'accessNum': 326, 'auctionStatus': 2, 'bidCount': 0, 'bidList': [], 'bidderName': '', 'blowCondition': '', 'blowFlag': 0, 'confirmationUrl': '', 'currentBidUserNumber': '', 'currentPrice': 280.0, 'currentPriceStr': '280', 'currentUser': '', 'delayEndTime': '', 'displayStatus': 1, 'endTime': 1628620800000, 'jdShipOrderAddress': '', 'judicatureRealTimeInfoResult': {'bankAccountResult': None, 'refNum': ''}, 'myBid': None, 'myNumber': '暂无代码', 'oldPriorPurchaserLevel': 0, 'orderStatus': -1, 'paimaiChargeOrderResult': {'commissionOrderPassKey': '', 'commissionOrderPayUrlForM': '', 'commissionOrderPayUrlForPc': '', 'commissionOrderStatus': 1, 'popOrderPassKey': '', 'popOrderPayUrlForM': '', 'popOrderPayUrlForPc': '', 'popOrderStatus': 1, 'selfOrderPassKey': '', 'selfOrderPayUrlForM': '', 'selfOrderPayUrlForPc': '', 'selfOrderStatus': 1}, 'paimaiGroupReduceRealTimeResult': None, 'paimaiId': 280492523, 'passKey': '', 'pauseTime': None, 'payDeadline': '', 'payUrl': '', 'priceLowerOffset': 10.0, 'priorPurchaserLevel': 0, 'remainTime': -1, 'remarks': '', 'restartTime': '', 'whetherTrustee': 0}, 'message': '成功', 'status': 0}
def analysis_Price(Price_response):     # 6、获取出价记录 （用于获取价格和判断是否结束）
    Price_data = Price_response['data']
    CurrentPriceStr = Price_data['currentPrice']                        # 当前价

    PaimaiTimes_id = Price_data.get('PaimaiTimes',0)
    PaimaiTimes = get_paimaiTimes_name(PaimaiTimes_id)                      # {0:None,1:'一拍',2:'二拍',4:'变卖',6:'破产'}

    BidStatus = Price_data['auctionStatus']                             # 拍卖状态id
    BidStatus_name = get_auctionStatus_name(BidStatus)                      # {0:'预告',1:'进行中',2:'已结束'}

    DisplayStatus = Price_data['displayStatus']              # {1:'无异常',5:'已撤回',6:'已暂缓',7:'已终止'}
    DisplayStatus_name = get_displayStatus_name(DisplayStatus)

    Remarks = Price_data['remarks']                         # 异常原因
    if not Remarks:
        Remarks = None

    DelayedCount = Price_data.get('delayedCount',None)       # 延时次数
    bidCount = Price_data['bidCount']                       # 竞买次数

    AccessEnsureNum = Price_data['accessEnsureNum']         # 报名人数

    confirmationUrl = Price_data['confirmationUrl']
    confirmationUrl_data = re.findall(r'(.*?)\?', confirmationUrl)
    if confirmationUrl_data:
        confirmationUrl_data = confirmationUrl_data[0]
        ShowSfDealConfirm = 1                               # 是否有成交确认书
        Confirm_url = 'https:'+confirmationUrl_data         # 成交确认书URL
    else:
        ShowSfDealConfirm = 0
        Confirm_url = None


    this_dict = {"CurrentPriceStr":CurrentPriceStr,"PaimaiTimes":PaimaiTimes,"PaimaiTimes_id":PaimaiTimes_id,"BidStatus":BidStatus,
                 "BidStatus_name":BidStatus_name,"DisplayStatus":DisplayStatus,"DisplayStatus_name":DisplayStatus_name,"Remarks":Remarks,
                 "DelayedCount":DelayedCount,"bidCount":bidCount,"AccessEnsureNum":AccessEnsureNum,"ShowSfDealConfirm":ShowSfDealConfirm,
                 "Confirm_url":Confirm_url}
    all_dict.update(this_dict)
    Update_dict.update(this_dict)


def analysis_DetaiExpand(DetaiExpand_response):             # 获取围观数、关注提醒
    DetaiExpand_data = DetaiExpand_response['data']
    FollowerCount = DetaiExpand_data['followerCount']       # 关注提醒数
    AccessNum = DetaiExpand_data['accessNum']               # 围观数

    this_dict = {"FollowerCount":FollowerCount,"AccessNum":AccessNum}
    all_dict.update(this_dict)
    Update_dict.update(this_dict)


def analysis_VendorInfo(VendorInfo_response):               # 获取处置方信息
    # {"code":0,"data":{"applicantPhone":"11111111111","logoUrl":"","mobile":"","shopId":641541,"shopName":"东莞市第一人民法院"},"message":"成功","status":0}
    VendorInfo_data = VendorInfo_response['data']
    Disposal = VendorInfo_data['shopName']                  # 处置方名称

    this_dict = {"Disposal":Disposal}
    all_dict.update(this_dict)


def run():
    all_results = get_data()
    # print(all_results)
    index = 1
    for data_list in all_results:
        # Price_response = data_list['Price_response']

        status_Update = int(data_list['status_Update'])
        status_analysis = int(data_list['status_analysis'])       # 读取 status_Update == 1 or status_analysis == 1的字段

        # data_list = {'item_id': '280492523', 'title': '【居家装饰】原值1200元全新两个泰国进口乳胶枕头改善睡眠保护颈椎', 'city_Name': '广州市', 'searchLabel_Name': '商业资产', 'searchCategory_Name': '库存物资', 'Basic_response': {'code': 0, 'data': {'albumId': 2779803, 'assessmentPrice': 0.0, 'auctionType': 5, 'businessType': 1, 'categoryId': 21440, 'commentScore': 0, 'commission': 10.0, 'commissionInfo': '', 'commissionMax': '', 'commissionRateSection': '', 'customId': 0, 'customPayTime': 2, 'delayedTime': 5, 'displayStatus': 1, 'downReason': '', 'endTime': 1628620800000, 'ensurePrice': 100.0, 'entrustLocation': '', 'extendInfoMap': '{}', 'isLogin': 'N', 'isPriorPurchaser': 0, 'judicatureBasicInfoResult': {'consultName': '刘先生', 'consultTel': '18229473009', 'loan': 0, 'purchaseRestriction': 0, 'snapshotInfoResultList': [], 'specialNotice': ''}, 'jumpOrgUrl': '', 'jumpPcOrgUrl': '', 'jumpPcShopUrl': 'https://pmmall.jd.com/assets/10167538', 'jumpShopUrl': 'https://pmmall.m.jd.com/#/mall/10167538', 'labelList': [{'associateType': 1, 'id': 1032, 'name': '商业资产', 'showOrder': 6, 'showType': 1, 'specialType': 3, 'status': 1, 'type': 1}], 'lat': '', 'lng': '', 'minPrice': '无', 'originalId': '', 'paimaiGroupReduceBasicInfoResult': {'reduceStageRule': ''}, 'paimaiId': 280492523, 'paimaiImageResultList': [{'imagePath': 'jfs/t1/108784/31/3765/203349/5e168b0bE844f5807/985c6e3a4749614c.png', 'skuId': 10034964494317}, {'imagePath': 'jfs/t1/98094/8/10081/224845/5e168b0cEe8681960/2e8c4d97c7ec6a75.png', 'skuId': 10034964494317}, {'imagePath': 'jfs/t1/88364/34/10140/532044/5e168b0dEefa87b4e/85bca99c0c7c8acd.png', 'skuId': 10034964494317}, {'imagePath': 'jfs/t1/107464/26/3824/296284/5e168b0cE61597f45/6ec0ceabe236aa56.png', 'skuId': 10034964494317}, {'imagePath': 'jfs/t1/89331/2/10152/158229/5e168b0bE6129f148/5d6d847c912a9e38.png', 'skuId': 10034964494317}], 'pin': '', 'platType': 4, 'priceHigherOffset': 100000000000.0, 'priceLowerOffset': 10.0, 'productAddressResult': {'address': '其他', 'city': '广州市', 'cityId': 1601, 'county': '白云区', 'countyId': 50258, 'province': '广东', 'provinceId': 19, 'town': '', 'townId': 0}, 'productId': 10021357225012, 'publishSource': 9, 'rateSection': '', 'remark': '', 'selfOrderHasDiscount': 0, 'serviceMoneyInfo': '', 'serviceMoneyType': 0, 'serviceOrganization': '', 'serviceSupport': '', 'skuId': 10034964494317, 'specifyCertificate': '', 'startPrice': 280.0, 'startTime': 1628534400000, 'supervisionOrganization': '', 'supportJdShip': 2, 'tailPayMode': 1, 'title': '【居家装饰】原值1200元全新两个泰国进口乳胶枕头改善睡眠保护颈椎', 'totalStock': 1, 'uploadOrganization': '', 'vendorId': 10167538, 'vrFlag': 0, 'vrUrl': '', 'whetherAudit': 0, 'ynExt': 'N'}, 'message': '成功', 'status': 0}, 'Description_response': {'code': 0, 'data': "<p><br/><a href='//img30.360buyimg.com/popWareDetail/jfs/t1/88364/34/10140/532044/5e168b0dEefa87b4e/85bca99c0c7c8acd.png' target='_blank'><img src='//img30.360buyimg.com/popWareDetail/jfs/t1/88364/34/10140/532044/5e168b0dEefa87b4e/85bca99c0c7c8acd.png' alt='' id='dtf6-0354ef69e786-ck'/></a><br/><a href='//img30.360buyimg.com/popWareDetail/jfs/t1/107464/26/3824/296284/5e168b0cE61597f45/6ec0ceabe236aa56.png' target='_blank'><img src='//img30.360buyimg.com/popWareDetail/jfs/t1/107464/26/3824/296284/5e168b0cE61597f45/6ec0ceabe236aa56.png' alt='' id='dtf6-9dab1f018f46-ck'/></a><br/><a href='//img30.360buyimg.com/popWareDetail/jfs/t1/98094/8/10081/224845/5e168b0cEe8681960/2e8c4d97c7ec6a75.png' target='_blank'><img src='//img30.360buyimg.com/popWareDetail/jfs/t1/98094/8/10081/224845/5e168b0cEe8681960/2e8c4d97c7ec6a75.png' alt='' id='dtf6-ab62eb6919e0-ck'/></a><br/><a href='//img30.360buyimg.com/popWareDetail/jfs/t1/89331/2/10152/158229/5e168b0bE6129f148/5d6d847c912a9e38.png' target='_blank'><img src='//img30.360buyimg.com/popWareDetail/jfs/t1/89331/2/10152/158229/5e168b0bE6129f148/5d6d847c912a9e38.png' alt='' id='dtf6-4481d35efdf4-ck'/></a><br/><a href='//img30.360buyimg.com/popWareDetail/jfs/t1/108784/31/3765/203349/5e168b0bE844f5807/985c6e3a4749614c.png' target='_blank'><img src='//img30.360buyimg.com/popWareDetail/jfs/t1/108784/31/3765/203349/5e168b0bE844f5807/985c6e3a4749614c.png' alt='' id='dtf6-cc31734bb576-ck'/></a></p>", 'message': '成功', 'status': 0}, 'AttachFiles_response': {'code': 0, 'data': [], 'message': '成功', 'status': 0}, 'Announcement_response': {'code': 0, 'data': {'content': '<p style="text-indent:56px;text-autospace:ideograph-numeric"><span style=";font-family:宋体;font-size:19px">经委托方申请，湖南森拓拍卖有限公司就委托方（到期质押产品或倒闭企业清算库存物资）委托处置资产一案</span><span style=";font-family:宋体;font-size:19px"><span style="font-family:宋体">，将在京东网资产竞价网络平台（网址</span><span style="font-family:宋体">http://zichan.jd.com）开展网上拍卖公开竞价活动，现公告如下：&nbsp;</span></span></p><p style="text-indent:56px;text-autospace:ideograph-numeric"><span style=";font-family:宋体;font-size:19px">&nbsp;&nbsp;&nbsp;</span><span style=";font-family:宋体;font-size:19px"><br/></span><strong><span style="font-family: 宋体;font-size: 19px">一、竞买标的物：</span></strong></p><p style="margin-left:28px;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;font-weight: bold;font-size: 19px">1.&nbsp;</span><strong><span style="font-family: 宋体;font-size: 19px">全新：</span></strong></p><p style="margin-right:0;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px">1，</span><strong><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px"><span style="font-family:宋体">【数码家电】原值</span><span style="font-family:宋体">298元挪威品牌SKOGSTAD迷你掌心电吹风一台</span></span></strong></p><p style="margin-right:0;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px">2，</span><strong><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px"><span style="font-family:宋体">【居家装饰】原值</span><span style="font-family:宋体">3万全新未拆封海伦凯勒HK125D白色钢琴一台</span></span></strong></p><p style="margin-right:0;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px">3，</span><strong><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px"><span style="font-family:宋体">【运动保健】参考价</span><span style="font-family:宋体">1.98万元多功能全自动按摩加热豪华按摩椅一台</span></span></strong></p><p style="margin-right:0;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px">4，</span><strong><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px">【居家装饰】全新水移画孔雀晒花工艺古筝一台</span></strong></p><p style="margin-right:0;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px">5，</span><strong><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px"><span style="font-family:宋体">【居家装饰】原值</span><span style="font-family:宋体">1200元全新两个泰国进口乳胶枕头改善睡眠保护颈椎</span></span></strong></p><p style="margin-right:0;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px">6，</span><strong><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px"><span style="font-family:宋体">【居家装饰】原值</span><span style="font-family:宋体">3980元樱能Q1全自动防盗智能指纹锁一把</span></span></strong></p><p style="margin-right:0;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px">7，</span><strong><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px"><span style="font-family:宋体">【数码家电】原值</span><span style="font-family:宋体">868元美固车载冰箱制冷冷藏车家两用冷暖箱21L一个</span></span></strong></p><p style="margin-right:0;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px">8，</span><strong><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px">【居家装饰】多喜爱刺绣薄被可水洗机洗空调被一床</span></strong></p><p style="margin-right:0;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px">9，</span><strong><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px"><span style="font-family:宋体">【酒水食品】原值</span><span style="font-family:宋体">1860元 &nbsp;2014年白牡丹福鼎白茶饼一个</span></span></strong></p><p style="margin-right:0;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px">10，</span><strong><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px"><span style="font-family:宋体">【服装百货】参考价</span><span style="font-family:宋体">690元ELLE女士时尚潮流项链一条</span></span></strong></p><p style="margin-left:28px;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;font-weight: bold;font-size: 19px">2.&nbsp;</span><strong><span style="font-family: 宋体;font-size: 19px">开拍时间：</span></strong><span style="font-family: 宋体;font-size: 19px">以京东平台拍卖每个标的物开拍、结束时间为准。</span></p><p style="margin-left:28px;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;font-weight: bold;font-size: 19px">3.&nbsp;</span><strong><span style="font-family: 宋体;font-size: 19px">特别提醒竞买人</span></strong><span style="font-family: 宋体;font-size: 19px">：</span><span style="font-family: 宋体;letter-spacing: 0;font-size: 19px;background: rgb(255, 255, 255)"><span style="font-family:宋体">（</span><span style="font-family:宋体">1）本宗拍卖标的物是质押到期物品或倒闭企业清算财物，拍品所设的拍卖条件及披露信息，均由拍卖人提供并解释。（2）</span></span><span style="font-family: 宋体;letter-spacing: 0;font-size: 19px;background: rgb(255, 255, 255)"><span style="font-family:宋体">本标的</span></span><span style="font-family: 宋体;letter-spacing: 0;font-size: 19px;background: rgb(255, 255, 255)"><span style="font-family:宋体">且未经专用评估机构评估，</span></span><span style="font-family: 宋体;letter-spacing: 0;font-size: 19px;background: rgb(255, 255, 255)"><span style="font-family:宋体">标题原值评估价是根据一些旗舰店、线下门店的销售价格综合评估仅供参考。具体价值请自行考察。（</span><span style="font-family:宋体">3）</span></span><span style="font-family: 宋体;letter-spacing: 0;font-size: 19px;background: rgb(255, 255, 255)"><span style="font-family:宋体">有意者请亲自实地看样，未看样的竞买人视为对本标的实物现状的确认，责任自负。对于大批量且标明是杂款杂码衣物或其他产品的，由于展示位有限图片展示的仅仅是处理标的物的一小部分，请详细了解产品后再参拍，建议批量产品看货以后再拍卖以免对您造成损失。</span></span></p><p style="margin-top:0;margin-right:0;margin-bottom:5px;margin-left:0;padding:0 0 0 0 ;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;font-size: 19px">二、竞买人条件：</span></p><p style="margin-top:0;margin-right:0;margin-bottom:5px;margin-left:0;padding:0 0 0 0 ;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;font-size: 19px"><span style="font-family:宋体">（</span><span style="font-family:宋体">1）凡具备完全民事行为能力的公民、法人和其他组织均可参加竞买。&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></span></p><p style="margin-top:0;margin-right:0;margin-bottom:5px;margin-left:0;padding:0 0 0 0 ;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;font-size: 19px"><span style="font-family:宋体">（</span><span style="font-family:宋体">2）竞价前，竞买人须在京东注册账号并通过实名认证（已注册京东账号需通过实名认证）。</span></span></p><p style="margin-top:0;margin-right:0;margin-bottom:5px;margin-left:0;padding:0 0 0 0 ;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;font-size: 19px">三、参拍保证金：</span><span style="font-family: 宋体;font-size: 19px">项目竞价前系统将冻结竞买人缴纳的保证金，竞价结束后未能竞得者冻结的保证金自动解冻，冻结期间不计利息。</span></p><p style="margin-top:0;margin-right:0;margin-bottom:5px;margin-left:0;padding:0 0 0 0 ;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;font-size: 19px">四</span><span style="font-family: 宋体;font-size: 19px">、优先购买权人参加竞买的，应于开拍前向本公司提交合法有效的证明，资格经本公司确认后才能以优先购买权人的身份参与竞买，逾期不提交的，视为放弃对本标的物享有优先购买权。本标的优先购买权人未参加竞拍，亦视为放弃优先购买权。</span></p><p style="margin-top:0;margin-right:0;margin-bottom:5px;margin-left:0;padding:0 0 0 0 ;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;font-size: 19px">五</span><span style="font-family: 宋体;font-size: 19px">、</span><span style="font-family: 宋体;font-size: 19px">标的</span><span style="font-family: 宋体;font-size: 19px">咨询、展示</span><span style="font-family: 宋体;font-size: 19px">、</span><span style="font-family: 宋体;font-size: 19px">看样的时间与方式：开拍前接受咨询有意者请自行看样</span><span style="font-family: 宋体;font-size: 19px">。</span><span style="font-family: 宋体;font-size: 19px">拍品不支持开具发票。</span></p><p style="margin-top:0;margin-right:0;margin-bottom:5px;margin-left:0;padding:0 0 0 0 ;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;font-size: 19px">六</span><span style="font-family: 宋体;font-size: 19px"><span style="font-family:宋体">、本次竞价活动设置延时出价功能，在竞价活动结束前，每最后</span><span style="font-family:宋体">5分钟如果有竞买人出价，就自动延迟5分钟。</span></span></p><p style="margin-top:0;margin-right:0;margin-bottom:5px;margin-left:0;padding:0 0 0 0 ;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;font-size: 19px">七</span><span style="font-family: 宋体;font-size: 19px"><span style="font-family:宋体">、对此次竞价标的物权属有异议者，请于竞价开始前</span><span style="font-family:宋体">3个工作日与拍卖人联系。</span></span></p><p style="margin-top:0;margin-right:0;margin-bottom:5px;margin-left:0;padding:0 0 0 0 ;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;font-size: 19px">八</span><span style="font-family: 宋体;font-size: 19px">、竞价方式：没有保留价的增价竞价方式，至少一人报名且出价不低于起拍价，方可成交。</span></p><p style="margin-top:0;margin-right:0;margin-bottom:5px;margin-left:0;padding:0 0 0 0 ;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;font-size: 19px">九</span><span style="font-family: 宋体;font-size: 19px">、本次网络竞价所涉标的物，全部依其现状进行处置。现状是指看样时点标的的质量、数量、新旧程度、使用现状等现实状况，至竞价时点竞买人没有异议，则表示竞买人认可看样时点与竞价时点标的现状一致。请欲报名参与竞价的竞买人充分考虑标的显性和隐性的瑕疵风险以及市场价格的波动，谨慎选择，慎重决定。</span></p><p style="margin-top:0;margin-right:0;margin-bottom:5px;margin-left:0;padding:0 0 0 0 ;text-autospace:ideograph-numeric;line-height:28px"><strong><span style="font-family: 宋体;font-size: 19px">十</span></strong><strong><span style="font-family: 宋体;font-size: 19px">、</span></strong><strong><span style="font-family: 宋体;font-size: 19px">特别说明</span></strong><strong><span style="font-family: 宋体;font-size: 19px">：</span></strong><strong><span style="font-family: 宋体;font-size: 19px">本拍卖公司承接拍品均为全新未拆封正品，无产品质量问题。请买受人放心参拍。</span></strong></p><p style="margin-top:0;margin-right:0;margin-bottom:5px;margin-left:0;padding:0 0 0 0 ;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;font-size: 19px">十</span><span style="font-family: 宋体;font-size: 19px">一</span><span style="font-family: 宋体;font-size: 19px">、本次网上公开竞价《竞买公告》、《竞拍须知》、《标的物介绍》等标的物相关文件已在京东网资产竞价网络平台公开展示，请仔细阅读。</span><span style="font-family: 宋体;font-size: 19px">湖南森拓</span><span style="font-family: 宋体;font-size: 19px">拍卖有限公司已就前述相关标的物相关文件的所有条款向竞买人如实告知并做出详细说明，竞买人知悉并同意接受前述文件的全部条款和内容，竞买人和资产处置方双方不存在任何歧异和误认，竞买人承诺不再对前述文件的条款提出任何异议。</span></p><p style="margin-top:0;margin-right:0;margin-bottom:5px;margin-left:0;padding:0 0 0 0 ;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;letter-spacing: 0;font-size: 19px">十二、</span><span style="font-family: 宋体;letter-spacing: 0;font-size: 19px">因委托人未尽瑕疵告知义务或是单方面违约，成交后无法交付或是无法办理过户手续的，属于委托人的责任，委托人负责全额退款。给买受人带来经济损失的，买受人可向委托人要求赔偿。根据拍卖相关法律及与委托人的协议约定，拍卖人不承担因此产生的任何责任。</span></p><p style="margin-top:0;margin-right:0;margin-bottom:5px;margin-left:0;padding:0 0 0 0 ;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;font-size: 19px">十</span><span style="font-family: 宋体;font-size: 19px">三</span><span style="font-family: 宋体;font-size: 19px">、竞买人在竞价前请务必再仔细阅读竞买须知。</span></p><p style="margin-top:0;margin-right:0;margin-bottom:5px;margin-left:0;padding:0 0 0 0 ;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;font-size: 19px">十</span><span style="font-family: 宋体;font-size: 19px">四</span><span style="font-family: 宋体;font-size: 19px">、本公告其他未尽事宜，请向本公司咨询。</span></p><p style="margin-top:0;margin-right:0;margin-bottom:5px;margin-left:0;padding:0 0 0 0 ;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;font-size: 19px">咨询电话：</span><span style="font-family: 宋体;font-size: 19px">18229473009</span></p><p style="margin-top:0;margin-right:0;margin-bottom:5px;margin-left:0;padding:0 0 0 0 ;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;font-size: 19px">&nbsp;</span></p><p style="margin-top:0;margin-right:0;margin-bottom:5px;margin-left:0;padding:0 0 0 0 ;text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;font-size: 19px"><span style="font-family:宋体">此公告在</span><span style="font-family:宋体">“京东网”上发布。</span></span></p><p style="margin-top:0;margin-right:0;margin-bottom:5px;margin-left:0;padding:0 0 0 0 ;text-autospace:ideograph-numeric;text-align:right;line-height:28px"><span style="font-family: 宋体;font-size: 19px">湖南森拓</span><span style="font-family: 宋体;font-size: 19px">拍卖有限公司</span></p><p><br/></p>', 'id': 3472337, 'title': '拍卖公告'}, 'message': '成功', 'status': 0}, 'Notice_response': {'code': 0, 'data': '<p style="text-autospace:ideograph-numeric;line-height:28px"><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">一、</span></span><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">湖南森拓</span></span><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">拍卖有限公司在京东网络资产竞价平台（网址</span><span style="font-family:宋体">http://zichan.jd.com）进行公开竞价活动，现就有关的网上竞价事宜敬告各位竞买人</span></span><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">。</span></span></p><p style="text-autospace:ideograph-numeric;line-height:28px"><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">二、竞买人在竞价前须详细阅读此《竞拍须知》，了解本须知的全部内容。本次竞价活动遵循</span><span style="font-family:宋体">“公开、公平、公正、诚实守信”的原则，竞价活动具备法律效力。参加本次竞价活动的当事人和竞买人必须遵守本须知的各项条款，并对自己的行为承担法律责任。</span></span></p><p style="text-autospace:ideograph-numeric;line-height:28px"><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">三、凡具备完全民事行为能力的公民、法人和其他组织均可参加竞买（竞买人须在京东网上实名注册）。</span></span></p><p style="text-autospace:ideograph-numeric;line-height:28px"><strong><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">四、发货说明</span></span></strong><strong><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">：</span></span></strong><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">1、</span></span><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">发货时间：客户支付</span></span><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">拍卖尾</span></span><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">款后</span></span><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">1-3</span></span><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">个工作日内发出</span></span><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">（</span></span><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">疫情及春节期间需要延迟发货</span></span><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">）。</span></span><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">2、</span></span><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">发货费用：</span></span><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">物流费用由买家到付，</span></span><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px"><span style="font-family:宋体">走物流的</span></span><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">批量产品及较重产品</span><span style="font-family:宋体">(比如钢琴、按摩椅等)可能不同物流公司不同地区会需要到当地城市物流点自提，请竞买人知悉。</span></span><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px"><span style="font-family:宋体">3、签收方式：买家验货后签收，如因</span></span><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px"><span style="font-family:宋体">快递</span></span><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px"><span style="font-family:宋体">的原因出现损坏等现象，应当场拍照取证反馈给本公司并拒收。一旦本人签收或非本人签收，后续出现任何问题，本公司概不负责。</span></span><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px"><span style="font-family:宋体">4</span></span><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">、发货地址：默认为买家预留地址</span></span><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">，</span></span><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">如需更改地址请在拍卖成交后</span><span style="font-family:宋体">12个小时内必须电话联系项目经理 18229473009 刘先生，否则发错地址由买受人自行承担责任。5、</span></span><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px"><span style="font-family:宋体">货品单一款式</span></span><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px"><span style="font-family:宋体">、</span></span><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px"><span style="font-family:宋体">颜色、</span></span><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px"><span style="font-family:宋体">数量或有出入，实际发货数量不足时按单价折算退还不足部分款项</span></span><span style="font-family: 宋体;letter-spacing: 0;font-size: 16px"><span style="font-family:宋体">，</span></span><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">颜色随机发货，如有款式、颜色等要求具体情况请在开拍前联系项目经理</span><span style="font-family:宋体">18229473009 刘先生。6、本产品不支持7天无理由退换货。</span></span></p><p style="text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">五</span></span><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">、优先购买权人参与竞买的，可以与其他竞买人以相同的价格出价，没有更高出价的，竞价财产由优先购买权人竞得。顺序不同的优先购买权人以相同价格出价的，竞价财产由顺序在先的优先购买权人竞得。顺序相同的优先购买权人以相同价格出价的，竞价财产由出价在先的优先购买权人竞得。</span></span></p><p style="text-autospace:ideograph-numeric;line-height:28px"><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">六</span></span><span style="font-family: 宋体;font-size: 16px"><span style="font-family:宋体">、本次竞价活动设置延时出价功能，在竞价活动结束前，每最后</span><span style="font-family:宋体">5分钟如果有竞买人出价，就自动延迟5分钟。</span></span></p><p style="text-autospace:ideograph-numeric;line-height:28px"><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">七</span></span><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">、竞拍前，竞买人须在京东注册账号并通过实名认证（已注册京东账号需通过实名认证）。竞买人在对标的物第一次确认出价竞拍前，按网络资产竞价平台服务系统提示在线报名缴纳保证金（因保证金金额较大，请提前开通网银支付的大额支付功能，或前往银行柜台办理提高网银支付限额的相关业务），支付后系统会自动冻结该笔保证金。具体要求请阅读竞价页面内的《竞拍须知》、《保证金须知》及京东网络竞价平台告知的竞价流程（竞价前必看）的相关准则。竞价成交的，本标的物竞得者（以下称买受人）冻结的保证金将自动转为部分成交款，由京东结算给</span></span><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">湖南森拓</span></span><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">拍卖有限公司。竞价结束后未能竞得者的保证金以及竞价未成交的（即流拍的）竞买人的保证金在竞价活动结束后即时解冻，保证金冻结期间不计利息。</span></span></p><p style="text-autospace:ideograph-numeric;line-height:28px"><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">八</span></span><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">、竞价成交后，买受人以任何理由违约的，交纳的保证金不予退还，本公司将依法对标的物再行处置，违约后重新处置的，原买受人不得参加竞买。</span></span></p><p style="text-autospace:ideograph-numeric;line-height:28px"><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">九</span></span><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">、本次竞价是经法定公告期和展示期后举行的，已就本次处置标的物已知及可能存在的瑕疵作了客观、详尽的说明。</span></span><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">湖南森拓</span></span><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">拍卖有限公司对本次处置标的物所作的说明、图片、文字等内容，仅供竞买人参考，不构成对标的物的任何担保。所以请竞买人在竞价前务必仔细审查标的物，调查是否存在瑕疵，认真研究查看所竞买标的物的实际情况，并请亲临展示现场，实地看样，未看样的竞买人视为对本标的实物现状的确认，慎重决定竞买行为，竞买人一旦作出竞买决定，即表明已完全了解，并接受标的物的现状和一切已知及未知的瑕疵。</span></span></p><p style="text-autospace:ideograph-numeric;line-height:28px"><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">十</span></span><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">、资产竞价过程中出现下列情形的，</span></span><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">湖南森拓</span></span><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">拍卖有限公司可以要求转让方立即中止或者终结资产转让活动，同时</span></span><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">湖南森拓</span></span><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">拍卖有限公司有权直接做出资产竞价活动中止和终结的决定：</span></span></p><p style="text-autospace:ideograph-numeric;line-height:28px"><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">（</span><span style="font-family:宋体">1）存在违反国家法律法规或其他有关方提出争议情形时；</span></span></p><p style="text-autospace:ideograph-numeric;line-height:28px"><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">（</span><span style="font-family:宋体">2）在资产竞价交易过程中出现违反各项交易规则、细则等相关规定，并妨碍正常交易秩序的；</span></span></p><p style="text-autospace:ideograph-numeric;line-height:28px"><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">（</span><span style="font-family:宋体">3）交易双方及相关主体因纠纷争讼，由仲裁机构（或法院）做出中止和终结决定的。</span></span></p><p style="text-autospace:ideograph-numeric;line-height:28px"><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">十</span></span><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">一</span></span><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">、本竞拍须知未尽事宜，请向本公司咨询。如发生争议，协商解决，协商不成的可向</span></span><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">长沙市开福区</span></span><span style=";font-family:宋体;font-size:16px"><span style="font-family:宋体">人民法院提起诉讼。</span></span></p><p style="text-autospace:ideograph-numeric;line-height:28px"><span style=";font-family:宋体;font-size:16px">&nbsp;</span></p><p style="text-autospace:ideograph-numeric;line-height:28px"><span style=";font-family:Calibri;font-size:14px">&nbsp;</span></p><p><br/></p>', 'message': '成功', 'status': 0}, 'Price_response': {'code': 0, 'data': {'accessEnsureNum': 0, 'accessNum': 326, 'auctionStatus': 2, 'bidCount': 0, 'bidList': [], 'bidderName': '', 'blowCondition': '', 'blowFlag': 0, 'confirmationUrl': '', 'currentBidUserNumber': '', 'currentPrice': 280.0, 'currentPriceStr': '280', 'currentUser': '', 'delayEndTime': '', 'displayStatus': 1, 'endTime': 1628620800000, 'jdShipOrderAddress': '', 'judicatureRealTimeInfoResult': {'bankAccountResult': None, 'refNum': ''}, 'myBid': None, 'myNumber': '暂无代码', 'oldPriorPurchaserLevel': 0, 'orderStatus': -1, 'paimaiChargeOrderResult': {'commissionOrderPassKey': '', 'commissionOrderPayUrlForM': '', 'commissionOrderPayUrlForPc': '', 'commissionOrderStatus': 1, 'popOrderPassKey': '', 'popOrderPayUrlForM': '', 'popOrderPayUrlForPc': '', 'popOrderStatus': 1, 'selfOrderPassKey': '', 'selfOrderPayUrlForM': '', 'selfOrderPayUrlForPc': '', 'selfOrderStatus': 1}, 'paimaiGroupReduceRealTimeResult': None, 'paimaiId': 280492523, 'passKey': '', 'pauseTime': None, 'payDeadline': '', 'payUrl': '', 'priceLowerOffset': 10.0, 'priorPurchaserLevel': 0, 'remainTime': -1, 'remarks': '', 'restartTime': '', 'whetherTrustee': 0}, 'message': '成功', 'status': 0}, 'DetaiExpand_respnse': {'code': 0, 'data': {'followerCount': 11, 'accessNum': 326}, 'status': 0}, 'VendorInfo_response': {'code': 0, 'data': {'allProductCount': 0, 'applicantPhone': '', 'dealingProductCount': 0, 'logoUrl': '//img30.360buyimg.com/popshop/jfs/t1/76688/2/157/10217/5ce3b155Eb0eb6918/a4a19570847748d0.jpg', 'mobile': '', 'shopId': 10167538, 'shopIdForJD': 10033248, 'shopName': '湖南森拓拍卖有限公司', 'vendorId': 10167538}, 'message': '成功', 'status': 0}, 'currentPrice': 280.0, 'down_time': '2022-12-14 10:54:06.532500', 'update_time': '2022-12-14 10:54:06.532500', 'status_analysis': 1, 'status_Update': 0}
        item_id = data_list['item_id']
        Basic_response = data_list['Basic_response']
        AttachFiles_response = data_list['AttachFiles_response']
        Price_response = data_list['Price_response']
        DetaiExpand_respnse = data_list['DetaiExpand_respnse']
        VendorInfo_response = data_list['VendorInfo_response']

        analysis_Mongo(data_list)
        analysis_Update_Basic(Basic_response,item_id)
        analysis_fixed_Basic(Basic_response)
        analysis_AttachFiles(AttachFiles_response)
        analysis_Price(Price_response)
        analysis_DetaiExpand(DetaiExpand_respnse)
        analysis_VendorInfo(VendorInfo_response)

        Mongo_update_time = data_list['update_time']  # Mongo的最后更新时间

        # !!!!这里有个bug，，status_analysis 状态不会更新到SQL中，而是将Mongo的状态复制过去sql
        # 后面需要将更新过后Mongo的 status_analysis 状态刷到SQL去
        other_dict = {"Mongo_update_time":Mongo_update_time}        # ,"status_analysis":status_analysis
        all_dict.update(other_dict)
        Update_dict.update(other_dict)


        Mysql_all_dict = [all_dict]  # 转换格式
        Mysql_Updata_list = [Update_dict]  # 需要更新
        Mongo_where_dict = {'item_id':item_id}
        Mysql_where_dict = [{'ItemID':item_id}]

        if status_analysis == 1:  # 是否是第一次解析，是否是需要第一次入Mysql
            if status_Update == 1:
                analysis = 2
                Mysql_all_dict[0]['status_analysis'] = analysis
                mongo_update_dict = {'status_analysis': analysis}        # 1 -> 2        ,后续需要继续更新
            elif status_Update == 0:
                analysis = 0
                Mysql_all_dict[0]['status_analysis'] = analysis
                mongo_update_dict = {'status_analysis': analysis}        # 1 -> 0        ，后续无需再更新

            manage_mysql.save_data(MySql_table,Mysql_all_dict)    # 入Mysql库
            manage_mongo.Update_mongodb_data(Mongo_table, Mongo_where_dict, mongo_update_dict)

        elif status_analysis == 2:          # 已解析过了，但需要更新数据
            if status_Update == 0:
                analysis = 0
                mongo_update_dict = {'status_analysis': analysis}        # 2 -> 0        ,后续无需再更新,否则 2 -> 2 ,任然需要更新
                Mysql_Updata_list[0]['status_analysis'] = analysis
            else:
                analysis = status_analysis
                mongo_update_dict = {'status_analysis': analysis}
                Mysql_Updata_list[0]['status_analysis'] = analysis
            manage_mysql.update_data(MySql_table,Mysql_Updata_list,Mysql_where_dict)
            manage_mongo.Update_mongodb_data(Mongo_table, Mongo_where_dict, mongo_update_dict)
        logger_data.info(f"进度：{index} --- item_id: {item_id} 解析成功！analysis解析状态:{analysis}")
        index += 1


if __name__ == '__main__':

    run()



# 286439563
# 116960659
# 116960661
# 145787827
# 109824895
# 284503421
# 286019441
# 284257969


# 291476118