# -*- coding: UTF-8 -*-
'''
@Project ：法拍 
@File ：RMFYSS_detail.py
@Author ：hao
@Date ：2022/12/6 14:51 
'''
import sys
sys.path.append("..")
import datetime
import time

import requests
import random
import re
from datetime import datetime
from wbh_word.manage_data import manage_mongo
from wbh_word.manage_data import manage_mysql
from loguru import logger
from wbh_word.spider import Get_ip


logger.add("/home/wangdong/fp_spider/RMFYSS_Script/logger/Detail_get_data.log", filter=lambda record: record["extra"]["name"] == "Detail_get_data")
logger_get_data = logger.bind(name="Detail_get_data")

MySql_table = 'wbh_RMFYSS_id'
Mongo_table = 'wbh_RMFYSS_detail'

"""
    查看状态：
    拍卖状态及成交价url：https://www1.rmfysszc.gov.cn/Object/Finish.shtml?jsoncallback=jQuery35908421121231603159_1670297941339&oid=122119&pid=3694351&_=1670297941357
 state:'4'      # 异常状态  可能取消、暂缓、撤回等等异常的原因      状态码为4 时 ， 状态可在html中获取
 state:'0'      # 即走正常的拍卖流程   可能会 流拍、
                1、可能是 流标：   此时会有流标说明  https://www1.rmfysszc.gov.cn/Object/Getlb.shtml?oid=132030
                2、可能是 成交：   此时有成交确认书  https://www1.rmfysszc.gov.cn/GetHtml.aspx?oid=132618
"""
'''    
success: function (data) {
if(data.state=="0"){
    startDate="2022/12/4 10:00:00";
    //竞价结束
    var fun2 = data.fun1;
    if(fun2=="1"){
        //流标
        $("#time1").html("状态:流标");
    }else{
        //成交
        $("#time1").html("状态:成交; <span class=\"ti\">成交价:"+data.price+"万元</span>");
    }
    clearInterval(id1);
    clearInterval(id2);
}else if(data.state=="1"){
    startDate="2022/12/4 10:00:00";
    //正在进行
    $("#time1").html("状态:进行中;当前价:<span class=\"ti\">"+data.price+"万元</span>");
}else if(data.state=="3"){
    startDate="2022/12/4 10:00:00";
    clearInterval(id1);
    clearInterval(id2);
}else if(data.state=="5"){
    GetTime1(1);
}else if(data.state=="6"){
    $("#time1").html("状态:已结束");
}
}
'''

def get_headers():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': '__jsluid_s=a929b4e8e12495a7c21fbc132c191421; __51vcke__JiCAlDGFUXIwGQjY=e9d73f51-d750-5f8b-87a1-866e78d9c645; __51vuft__JiCAlDGFUXIwGQjY=1667974192091; ASP.NET_SessionId=10zbsxmxllfqkcsstzyy1pfl; Cookies-01=78968004; Hm_lvt_5698cdfa8b95bb873f5ca4ecf94ac150=1667974183,1669862514,1670206116,1670295032; __51uvsct__JiCAlDGFUXIwGQjY=7; __vtins__JiCAlDGFUXIwGQjY=%7B%22sid%22%3A%20%225ecf9f36-017f-505d-9d58-97e036ab5fc0%22%2C%20%22vd%22%3A%202%2C%20%22stt%22%3A%2079356%2C%20%22dr%22%3A%2079356%2C%20%22expires%22%3A%201670297637184%2C%20%22ct%22%3A%201670295837184%7D; Hm_lpvt_5698cdfa8b95bb873f5ca4ecf94ac150=1670296589',
        'Referer': 'https://www.rmfysszc.gov.cn/',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    return headers

headers = get_headers()
def get_response(url,params,proxies):
    try:
        response = requests.get(url=url,headers=headers,params=params,proxies=proxies,timeout=5)
        # response = resp.text
        if response.status_code != 200:
            print(f"状态码: {response.status_code}  不为200！重新请求")
            raise
        # response = requests.get(url=url, headers=headers, params=params, proxies=proxies, timeout=5)
    except Exception as e:
        proxies = Get_ip.ip_proxies()
        time.sleep(float(random.randint(200, 400)) / 1000)
        response,proxies = get_response(url,params,proxies)
    return response,proxies


def get_data_list():
    # [('11045', '广东省清新县（现为清远市清新区）太和镇八号区一宗土地使用权及地下室', '房产', '住宅用房'), ('8359', '广州市荔湾区文昌南路137号之一地下2层288A车位', '房产', '其他用房')]
    return_list = ['item_id','status_Mongo','status_Update']  # 查询后返回的字段
    where_list = [{"status_Update": 1}]         # 查询需要更新的数据  备注：status_Mongo为1时 ， status_Update 一定也为1
    data_list = manage_mysql.read_where_data(MySql_table,return_list,where_list)
    print(data_list)
    # [('7495', '1', '1'), ('7496', '1', '1'), ('7497', '1', '1')]
    return data_list


def get_state_id(state_response,html_response):
    # ({state:'0',time:'2022-11-29 10:00:00',price:'0',fun1:'1'})       # 流标
    # {state: '0', time: '2022-04-01 10:09:52', price: '107.7749', fun1: '0'}       # 拍卖成功
    # {state:'1',price:'105.1'}         # 正在进行
    # {state:'4'}       # 拍卖异常
    # 无state_response情况 ：    1、网站问题，本来就没有       2、未开始       # 返回状态：状态异常_待人工确认

    if "很抱歉，您的访问存在异常！" not in html_response:
        state_response = state_response.text
        try:
            state_id_rule = r"state:'(.*?)'"  # 获取状态码  4 / 1 / 0   获取不到则说明可能是未开始
            state_id = int(re.findall(state_id_rule, state_response)[0])
        except Exception as e:  # 未开始
            state_id = "状态异常_待人工确认"
    else:
        state_id = "很抱歉，您的访问存在异常！"
    return state_id

def get_price(state_response):
    # {state:'1',price:'105.1'}  获取状态码
    state_response = state_response.text
    price_rule = r"price:'(.*?)'"        # 价格
    price = re.findall(price_rule, state_response)[0] + '万'
    # print(price)
    return price

def get_end_time(state_response):           # 结束时间
    # {state:'0',time:'2022-04-01 10:09:52',price:'107.7749',fun1:'0'}  获取结束时间
    state_response = state_response.text
    end_time_rule = r"time:'(.*?)'"        # 价格
    end_time = re.findall(end_time_rule, state_response)[0]
    # print(end_time)
    return end_time

def get_fun1_id(state_response):
    state_response = state_response.text
    fun1_id_rule = r"fun1:'(.*?)'"        # 价格
    fun1_id = int(re.findall(fun1_id_rule, state_response)[0])
    # print(fun1_id)
    return fun1_id


def get_html(item_id,proxies):
    url = f'https://www.rmfysszc.gov.cn/statichtml/rm_obj/{item_id}.shtml'
    html_response,proxies = get_response(url,None,proxies)
    html_response.encoding = 'UTF-8'
    html_response = html_response.text
    # print(html_response)
    return html_response,proxies


def get_BidResults_params(html_data):
    # state_url    成交确认书需要用到一下两个参数
    BidResults_params_rule = r"BidResults.aspx\?(.*)';"
    BidResults_params_ = re.findall(BidResults_params_rule, html_data)[0]         # source=f4160008-e09b-4955-99f0-24441c661247&sourceNumber=50010120220000000531&time=2022-11-25&oid=3956&rwobjid=132794&type=0099
    BidResults_params_url = "https://auction.rmfysszc.gov.cn/BidResults.aspx?"+BidResults_params_
    # print(BidResults_params_url)
    rwobjid_rule = r'rwobjid=(.*?)&'        #
    try:
        rwobjid = re.findall(rwobjid_rule,BidResults_params_url)[0]
        # print(rwobjid)
        params = {
            'url': BidResults_params_url,
            'oid': rwobjid
        }
    except:
        print("查找rwobjid失败，params取消rwobjid参数")
        params = {
            'url': BidResults_params_url,
            # 'oid': rwobjid
        }

    return params
def get_BidResults(html_data,proxies):      # 成交确认书
    url = 'https://www1.rmfysszc.gov.cn/GetHtml.aspx'
    params = get_BidResults_params(html_data)
    BidResults,proxies = get_response(url,params,proxies)
    BidResults = BidResults.text
    return BidResults,proxies


def get_AbortiveResults(item_id,proxies):
    url = 'https://www1.rmfysszc.gov.cn/Object/Getlb.shtml'
    params = {'oid': item_id}
    AbortiveResults,proxies = get_response(url,params,proxies)
    AbortiveResults = AbortiveResults.text
    print(AbortiveResults)
    return AbortiveResults,proxies


def run(data_list):
    index = 1
    proxies = Get_ip.ip_proxies()
    # proxies = None
    for data in data_list:
        item_id = data[0]
        status_Mongo = int(data[1])
        status_Update = int(data[2])
        down_time = str(datetime.now())         # 首次入库时间
        update_time = str(datetime.now())       # 更新时间

        html_response, proxies = get_html(item_id, proxies)
        state_url = f'https://www1.rmfysszc.gov.cn/Object/Finish.shtml?&oid={item_id}'
        state_response, proxies = get_response(state_url, None, proxies)
        print(f'当前{item_id}状态码为： {state_response.text}')
        state_id = get_state_id(state_response,html_response)     # 解析状态响应，返回状态码

        # 其中 未开始、正在进行需要更新  数据异常和正常拍卖不再需要更新  入库即可
        if state_id == "状态异常_待人工确认" or state_id == "很抱歉，您的访问存在异常！":     # 未开始，仅获取html即可  数据需要更新
            sql_updata_list = [{"item_status":state_id,"status_Mongo": '0',"status_Update":'1', "update_time": update_time}]
            mongo_save_dict = {"item_id":item_id,"item_status":state_id,"html_response":html_response,"Results_Book":"-","update_time":update_time}

        elif state_id == 1:  # 正在进行      # 更新价格  {state:'1',price:'105.1'}
            price = get_price(state_response)
            sql_updata_list = [{"item_status": "正在进行","price":price, "status_Mongo": '0', "update_time": update_time}]
            mongo_save_dict = {"item_id": item_id, "item_status": "正在进行", "html_response": html_response,"Results_Book": "-", "update_time": update_time}

        elif state_id == 4:  # 数据异常 状态码为4   可能取消、暂缓、撤回等等异常的原因   状态（基础数据那块）、时间（在拍卖公告） 可在html中获取 即直接获取html数据即可
            # {state: '4'}
            sql_updata_list = [{"item_status":"state_id=4,状态需从html中查看","status_Mongo": '0',"status_Update":'0', "update_time": update_time}]
            mongo_save_dict = {"item_id": item_id, "item_status": "state_id=4,状态需从html中查看", "html_response": html_response,"Results_Book": "-", "update_time": update_time}

        elif state_id == 0:         # 正常拍卖 且拍卖结果已出  此时有结束时间  情况分两类，fun1 = 0:成交     fun1 = 1:流拍
                # ({state:'0',time:'2022-11-29 10:00:00',price:'0',fun1:'1'})           # 流标
                # {state: '0', time: '2022-04-01 10:09:52', price: '107.7749', fun1: '0'}       # 拍卖成功

                fun1_id = get_fun1_id(state_response)
                price = get_price(state_response)
                e_time = get_end_time(state_response)
                if fun1_id == 1:    # 流拍， 获取流标结果报告
                    AbortiveResults = get_AbortiveResults(item_id,proxies)
                    sql_updata_list = [{"item_status": "流拍","price":price,"e_time":e_time, "status_Mongo": '0', "status_Update": '0',"update_time": update_time}]
                    mongo_save_dict = {"item_id": item_id, "item_status": "流拍","html_response": html_response, "Results_Book": AbortiveResults, "update_time": update_time}

                else:           # 已成交， 获取成交确认书
                    BidResults,proxies = get_BidResults(html_response,proxies)
                    sql_updata_list = [{"item_status": "已成交", "price": price, "e_time": e_time, "status_Mongo": '0',"status_Update": '0', "update_time": update_time}]
                    mongo_save_dict = {"item_id": item_id, "item_status": "流拍", "html_response": html_response,"Results_Book": BidResults, "update_time": update_time}

        time.sleep(random.randint(200, 500) / 1000)
        # Mongo:   # item_id,item_status,html_response,Results_Book,down_time,update_time
        if status_Mongo == 1 and status_Update == 1:  # 还未入库
            mongo_save_dict['down_time'] = down_time
            manage_mongo.save_mongodb_data(Mongo_table, mongo_save_dict)
            logger_get_data.info(f"进度：{index} / {len(data_list)} item_id:{item_id} --- Mongo数据入库成功")
        elif status_Mongo == 0 and status_Update == 1:      # 已入库且待更新
            mongo_where_dict = {"item_id": item_id}
            manage_mongo.Update_mongodb_data(Mongo_table,mongo_where_dict,mongo_save_dict)      # 更新
            logger_get_data.info(f"进度：{index} / {len(data_list)} --- item_id:{item_id} --- Mongo数据更新成功")

        index += 1
        sql_where_data = [{"item_id": item_id}]
        manage_mysql.update_data(MySql_table, sql_updata_list, sql_where_data)


if __name__ == '__main__':
    data_list = get_data_list()
    if data_list:
        run(data_list)


