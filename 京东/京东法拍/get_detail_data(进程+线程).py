import os
import requests
import threading
from loguru import logger
from datetime import datetime
from multiprocessing import Pool

from wbh_word.Dispose_data import Dispose_time
from wbh_word.spider import Get_ip
from wbh_word.manage_data import manage_mongo
from wbh_word.manage_data import manage_mysql

logger.add("D:/yj_pj/法拍/BLZC/JD/logger/Detail_get_data.log", filter=lambda record: record["extra"]["name"] == "get_data")
logger.add("D:/yj_pj/法拍/BLZC/JD/logger/Detail_warning.log", filter=lambda record: record["extra"]["name"] == "warning")
logger_data = logger.bind(name="get_data")
logger_warning = logger.bind(name="warning")

# Mysql -> Mongo
Mongo_table = 'wbh_JD_details_new'
MySql_table = 'wbh_JD_id'        # 这里最终需要替换为 wbh_JD_id
# ----------------多线程重写----------------------
class MyThread(threading.Thread):
    def __init__(self, func, args):
        """
        :param func: run方法中的函数名
        :param args: func函数所需的参数
        """
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        print('当前子线程:{}启动'.format(threading.current_thread().name))
        self.result = self.func(self.args)
        return self.func

    def get_result(self):  # 获取返回值
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except:
            return None



def get_headers1():
    headers1 = {
        'Host': 'api.m.jd.com',
        'Connection': 'close',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'script',
        'Referer': 'https://auction.jd.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Cookie': '__jda=122270672.1657003436722516907276.1657003437.1657003437.1657003437.1; __jdc=122270672; __jdv=122270672|direct|-|none|-|1657003436723; __jdu=1657003436722516907276; areaId=19; ipLoc-djd=19-1607-0-0; __jdb=122270672.3.1657003436722516907276|1.1657003437; 3AB9D23F7A4B3C9B=KLSD5FML7GAEOJX37D5SFZ6TR5SGHX3JOKK25JBIP6X7YPE2UJZ4UA6ISM6ATVL2YO54MCNKSJ2A56U22PDBX245JA',
    }
    return headers1
def get_headers2():
    headers2 = {
        'authority': 'api.m.jd.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        # 'cookie': '__jdu=1150602776; shshshfpa=47614922-da9a-fc9b-0d9d-671b3befe1bc-1668567652; shshshfpb=giRKoWKWc7IctLwsAZzhqAw; shshshfp=8029a00ba0d20e11eb69483951bda194; areaId=19; ipLoc-djd=19-1607-0-0; unpl=JF8EALBnNSttDBxdURgDEhUXHw9cW10IQh4FbWcGVQ9bGFBRGAAaG0N7XlVdXhRLFB9tZhRUXFNPVg4bAysSEXteXVdZDEsWC2tXVgQFDQ8VXURJQlZAFDNVCV9dSRZRZjJWBFtdT1xWSAYYRRMfDlAKDlhCR1FpMjVkXlh7VAQrAhsWEUxcV1hbD3sWM2hXNWRfWUlTBRMyGiIRex8AAlkNSxMAaSoFVFlZTFUGHQQcIhF7Xg; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_ef8e20866ec94118873120c2b5e2308b|1672368789091; __jdc=122270672; __jda=122270672.1150602776.1668567649.1672368789.1672737782.20; __jdb=122270672.7.1150602776|20.1672737782; 3AB9D23F7A4B3C9B=NZRRPGS4T6FFDD4E5R7YJ4C5WASBRGAVVPEX66FIZWA7KDDKQSCGW23VHDB6Q2DP6C3DQMCXCZ7Z3IUJH72T3SEQUE; RT="z=1&dm=jd.com&si=cl475u43s7m&ss=lcg0w3lm&sl=0&tt=0&r=b896cdb9aa1a86e3209b3ce6a896e898&ul=5ns8&hd=5nub"',
        'referer': 'https://paimai.jd.com/',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }
    return headers2
headers1 = get_headers1()
headers2 = get_headers2()

def get_auctionStatus_name(auctionStatus_id):
    auctionStatus_dict = {0:'预告',1:'进行中',2:'已结束'}
    auctionStatus_name = auctionStatus_dict[auctionStatus_id]
    return auctionStatus_name

def get_displayStatus_name(displayStatus_id):
    displayStatus_dict = {1:'无异常',7:'已中止',5:'已撤回',6:'已暂缓'}
    displayStatus_name = displayStatus_dict[displayStatus_id]
    return displayStatus_name

def get_id_data():
    table = MySql_table
    select_list = ['item_id','title','city_Name','searchLabel_Name','searchCategory_Name','status_Mongo','status_Update']  # 查询字段
    where_data = [{'status_Update': 1}]      # 查询需要更新的数据  备注：status_Mongo为1时 ， status_Update 一定也为1
    # 取不重复数据、且排序
    id_data = manage_mysql.read_where_data(table=table,select_list = select_list,where_data=where_data)
    data_list = list(id_data)
    # print(data_list)
    return data_list

def split_list(list,thread_num):
    list_total = []
    num = thread_num  # 线程数量
    x = len(list) // num  # 将参数进行分批（批数 = 线程数）方便传参
    count = 1  # 计算这是第几个列表
    for i in range(0, len(list), x):
        if count < num:
            list_total.append(list[i:i + x])
            count += 1
        else:
            list_total.append(list[i:])
            break
    return list_total

# 292142186&start=0&end=9 -----

def get_response(url,proxies):
    try:
        response = requests.get(url=url, headers=headers1, proxies=proxies, timeout=(3,5))
        response = response.json()
        # print('response : ',response)
        # return response,proxies
    except Exception as e:
        proxies = Get_ip.ip_proxies()
        if 'timed out' not in str(e):
            logger_warning.warning(f'线程：{threading.current_thread().getName()}-- 发送请求失败，更换ip重新访问,url: {url} ----- 错误：{e}')
        response,proxies = get_response(url,proxies)

    return response,proxies

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


def get_necessary_response(item_id,proxies):
    '''
    无论是更新还是入库时候，都必须要第一个请求的数据，其中包括：
    1、Basic_url         更新字段：结束时间
    2、Price_url         更新字段：状态信息、当前价、报名数、出价次数
    3、DetaiExpand_url   更新字段：围观数、关注提醒
    '''
    url_dict = get_req_url(item_id)
    Basic_url = url_dict['Basic_url']
    Basic_response, proxies = get_response(Basic_url, proxies)  # 1、获取基础数据     同时获取 albumId （请求拍卖公告的一个参数）

    Price_url = url_dict['Price_url']
    Price_response, proxies = get_response(Price_url, proxies)  # 6、获取出价记录 （用于获取价格和判断是否结束）

    DetaiExpand_url = url_dict['DetaiExpand_url']
    DetaiExpand_respnse, proxies = get_response(DetaiExpand_url, proxies)
    necessary_response_dict = {'Basic_response':Basic_response,'Price_response':Price_response,'DetaiExpand_respnse':DetaiExpand_respnse}

    return necessary_response_dict,proxies


def get_other_detail_response(item_id,Basic_response,proxies):
    '''
    这部分只需要在入库时候请求，无需更新
    1、获取标的物详情（标的物介绍） Description_url
    2、获取标的物介绍 附件 AttachFiles_url
    3、拍卖公告（竞买公告） Announcement_url     注意！！ 这里url参数要用到 base中的 albumId
    4、获取拍卖须知（竞买须知） Notice_url
    5、获取处置方信息 VendorInfo_url            注意！！ 这里要用到 base中的 courtVendorId
    '''
    albumId = str(Basic_response['data']['albumId'])                # 获取拍卖公告参数

    try:
        vendorId = str(Basic_response['data']['courtVendorId'])    # 获取处置方信息参数
    except:
        try:
            vendorId = str(Basic_response['data']['vendorId'])
        except:
            logger_warning.error(f"获取{item_id}的courtVendorId失败！！！！！！")

    url_dict = get_req_url(item_id)

    Description_url = url_dict['Description_url']
    Description_response, proxies = get_response(Description_url, proxies)  # 1、获取标的物详情（标的物介绍）

    AttachFiles_url = url_dict['AttachFiles_url']
    AttachFiles_response, proxies = get_response(AttachFiles_url, proxies)  # 2、获取标的物介绍 附件

    Announcement_url = get_req_url(albumId)['Announcement_url']
    Announcement_response, proxies = get_response(Announcement_url,proxies)  # 3、获取拍卖公告（竞买公告）    注意！！ 这里要用到 reponse中的 albumId

    Notice_url = url_dict['Notice_url']
    Notice_response, proxies = get_response(Notice_url, proxies)             # 4、获取拍卖须知（竞买须知）

    VendorInfo_url = get_req_url(vendorId)['VendorInfo_url']            # 5、获取处置方信息
    VendorInfo_response, proxies = get_response(VendorInfo_url, proxies)

    other_detail_dict = {'Description_response':Description_response,'AttachFiles_response':AttachFiles_response,'Announcement_response':Announcement_response,
                         'Notice_response':Notice_response,'VendorInfo_response':VendorInfo_response}

    return other_detail_dict,proxies


# 解析Price_response 和 Basic_response 获取状态等数据
def manage_Status_response(Price_response,Basic_response):
    Price_data = Price_response['data']
    currentPrice = float(Price_data.get('currentPrice',0))       # 当前价格
    auctionStatus_id = int(Price_data['auctionStatus'])    # 拍卖状态
    auctionStatus_name = get_auctionStatus_name(auctionStatus_id)
    displayStatus_id = int(Price_data['displayStatus'])    # 异常状态
    displayStatus_name = get_displayStatus_name(displayStatus_id)
    if auctionStatus_id == 2:      # 已结束
        endTime_bool = True
        e_time_tf = Price_data['endTime']
    else:                       # 未结束
        endTime_bool = False
        e_time_tf = Basic_response['data']['endTime']       # 还未结束，通过basic响应获取结束时间
    endTime = Dispose_time.get_time_data(e_time_tf)

    '''    
    try:    # 已结束
        endTime = Price_data['endTime']
        endTime_bool = True     # 是否结束，有endTime说明已结束
    except:
        endTime_bool = False
        e_time_tf = Basic_response['endTime']       # 还未结束，通过basic响应获取结束时间
        endTime = Dispose_time.get_time_data(e_time_tf)
        '''
    Status_dict = {'currentPrice':currentPrice,'auctionStatus_id':auctionStatus_id,'auctionStatus_name':auctionStatus_name,'displayStatus_id':displayStatus_id,
                   'displayStatus_name':displayStatus_name,'endTime':endTime}

    return Status_dict,endTime_bool


def get_detail_data(thread_arg):
    index = 0
    ip_usenum = 0
    proxies = Get_ip.ip_proxies()
    num = len(thread_arg)
    for arg_list in thread_arg:
        index += 1
        if ip_usenum>15:
            proxies = Get_ip.ip_proxies()
            ip_usenum = 0
        ip_usenum += 1
        item_id = arg_list[0]
        title = arg_list[1]
        city_Name = arg_list[2]
        searchLabel_Name = arg_list[3]  # 资产性质
        searchCategory_Name = arg_list[4]  # 标的物类型
        status_Mongo = int(arg_list[5])
        status_Update = int(arg_list[6])

        index_html_url = f'https://paimai.jd.com/{item_id}'     # 这个部分用来判断数据是否存在
        response = requests.get(url=index_html_url,headers=headers2)
        response.encoding = 'utf-8'
        html_response = response.text
        if "您所访问的页面不存在" in html_response:           # 出现页面失效情况，将该条数据从sql中剔除
            del_sql = f'''delete from {MySql_table} where `item_id` = "{item_id}"'''
            manage_mysql.run_sql(sql=del_sql)
            logger_warning.error(f"item_id: {item_id}页面不存在！！！！！！，删除mysql！！！")
            continue
        else:
            necessary_response_dict, proxies = get_necessary_response(item_id,proxies)      # 第一步获取必要的数据
            Basic_response = necessary_response_dict['Basic_response']
            Price_response = necessary_response_dict['Price_response']
            DetaiExpand_respnse = necessary_response_dict['DetaiExpand_respnse']    # 获取围观数、关注提醒

            #     Status_dict = {'currentPrice':currentPrice,'auctionStatus':auctionStatus,'auctionStatus_name':auctionStatus_name,'displayStatus':displayStatus,
            #                    'displayStatus_name':displayStatus_name,'endTime':endTime}
            try:
                Status_dict,endTime_bool = manage_Status_response(Price_response,Basic_response)       # 获取价格，并查看是否已结束
            except Exception as e:
                logger_warning.error(f"item_id: {item_id} 报错！！！！",e)
                # 283714785
                raise

            currentPrice = Status_dict['currentPrice']
            auctionStatus_id = Status_dict['auctionStatus_id']
            auctionStatus_name = Status_dict['auctionStatus_name']
            displayStatus_id = Status_dict['displayStatus_id']
            displayStatus_name = Status_dict['displayStatus_name']
            e_time = Status_dict['endTime']

            down_time = str(datetime.now())         # 首次入库时间
            update_time = str(datetime.now())       # 更新时间

            sql_where_data = [{"item_id": item_id}]
            mongo_where_dict = {'item_id': item_id}
            sql_updata_list = [{"auctionStatus_id":auctionStatus_id,"auctionStatus":auctionStatus_name,"displayStatus_id":displayStatus_id,
                                "displayStatus":displayStatus_name,"currentPriceCN":currentPrice,
                                "Update_time":update_time,"status_Mongo": '0','e_time':e_time}]
            if endTime_bool:        # 结束
                sql_updata_list[0]['status_Update'] = 0     # 不再更新


            if status_Mongo == 1 and status_Update == 1:       # 需要入库
                # Basic_response,Description_response,AttachFiles_response,Announcement_response,Notice_response,proxies = get_detail_all_response(item_id, proxies)
                other_detail_dict,proxies = get_other_detail_response(item_id,Basic_response,proxies)
                Description_response = other_detail_dict['Description_response']
                AttachFiles_response = other_detail_dict['AttachFiles_response']
                Announcement_response = other_detail_dict['Announcement_response']
                Notice_response = other_detail_dict['Notice_response']
                VendorInfo_response = other_detail_dict['VendorInfo_response']
                mongodb_save_dict = {'item_id': item_id, 'title': title, 'city_Name': city_Name, 'searchLabel_Name': searchLabel_Name,
                        'searchCategory_Name': searchCategory_Name, 'Basic_response': Basic_response,'Description_response': Description_response,
                        'AttachFiles_response': AttachFiles_response, 'Announcement_response': Announcement_response,'Notice_response': Notice_response,
                        'Price_response':Price_response,'DetaiExpand_respnse':DetaiExpand_respnse,'VendorInfo_response':VendorInfo_response,
                        'currentPrice':currentPrice,'down_time':down_time,'update_time':update_time,"status_analysis":1}
                # status_analysis: 是否需要解析
                if endTime_bool:        # 结束
                    mongodb_save_dict['status_Update'] = 0
                else:
                    mongodb_save_dict['status_Update'] = 1
                manage_mongo.save_mongodb_data(Mongo_table, mongodb_save_dict)
                # manage_mysql.update_data(MySql_table, sql_updata_list, sql_where_data)
                logger_warning.info(f'线程：{threading.current_thread().getName()}-- 进度：{index}/{len(thread_arg)}--item_id:{item_id} 入库 mongo成功！！')
            elif status_Mongo == 0 and status_Update == 1:        # 已入库,但需要更新
                mongo_update_dict = {'Basic_response': Basic_response,'Price_response':Price_response,'currentPrice':currentPrice,'DetaiExpand_respnse':DetaiExpand_respnse,
                                     'update_time':update_time}     #,"status_analysis":1  入库才需要加上，此处是更新
                if endTime_bool:        # 结束
                    mongo_update_dict['status_Update'] = 0
                else:
                    mongo_update_dict['status_Update'] = 1
                logger_warning.info(f'线程：{threading.current_thread().getName()}-- 进度：{index}/{len(thread_arg)}--id:{item_id} 更新 mongo 数据库成功！！')
                manage_mongo.Update_mongodb_data(Mongo_table,mongo_where_dict,mongo_update_dict)

            manage_mysql.update_data(MySql_table, sql_updata_list, sql_where_data)
    logger_warning.info(f'线程：{threading.current_thread().getName()} --- 运行结束！！！')



def create_thread_get_data(list_data,thread_num):
    list_total = split_list(list_data,thread_num) # 调用上面的方法，将任务平均分配给线程（切割列表）
    # print(list_total)
    thread_list =[]     # 线程池
    for thread_arg in list_total:      # 添加线程
        t = MyThread(func=get_detail_data,args=thread_arg)
        thread_list.append(t)        # 等同于下面两句话
        # thread1 = MyThread(func=get_all_ip,args=list_total[0])
        # thread2 = MyThread(func=get_all_ip,args=list_total[1])
    for t in thread_list:       # 批量启动线程
        t.start()
    for t in thread_list:       # 主线程等待子线程
        t.join()
    logger_warning.warning(f'所有线程： 运行结束！')

if __name__ == '__main__':
    list_data = get_id_data()

    print('Current process %s.' % os.getpid( ))
    p = Pool(processes=4)               # 创建容量为4的进程
    list_total = split_list(list_data, 4)  # 进程数
    for thread_list in list_total:
        p.apply_async(create_thread_get_data, (thread_list, 4))

    print("Waiting for all subprocesses done...")
    p.close()
    p.join()
