# -*- coding: UTF-8 -*-
'''
@Project ：yj_pj 
@File ：get_html.py
@Author ：hao
@Date ：2023/3/7 10:19 
'''
import re
import time
import requests

from wbh_word.manage_data import manage_mysql
from wbh_word.spider import Get_response
from wbh_word.spider import Get_ip
from wbh_word.Monitor_Robot import Wx_Robot

Mysql_table = 'YWF_Legalref_1997'

def get_headers():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'JSESSIONID=14B390D2BBFBE149D22660BCC563EE2E; TS01f243ce=019fbe4eec39fa86d33655351f22973ca7228f39b682bcd941a1d2816261a1b525c291c025787d2f6d7a33f57983cacc7c1a95690ed84cca5e2131bf556be45dd27133d272; BIGipServerpool_dc1_legalref.judiciary.hk_ext01_http=561062154.20480.0000; ispopup=0; curl=; jbudes=; fontsize=0; LrsLan=tc; TS01203efd=019fbe4eec4ffdf1f8789ec1d94067da9b3a03b645d6709ebf1c660d5a90a67b1b8cc8bb6502508f4ec5689ee92a7245d6c577ef3be309925811608e1ab953121bb87fa239b4937a342a5ebff9e0b5b331994cba4c',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    return headers
headers = get_headers()

def get_F1_url_list():     # 获取第一层列表页url
    '''
    # EX=T  显示全部日期的url
    婚姻訴訟	    : L2=MC
    家事雜項案件	: L2=MP
    離婚共同申請	: L2=JA
    '''
    F1_url_list = [
        'https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&AR=1#A1',
        'https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MP&AR=2#A2',
        'https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=JA&AR=3#A3'
    ]
    return F1_url_list


def get_response_html(url,proxies):           # 列表页html
    response,_ = Get_response.get_html_response(url,headers=headers,timeout=30,time_sleep=(1.5,3))
    response_html = response.text
    return response_html


def get_myMenu_data(list_html):
    '''
    return: myMenu_data ： imgsrc="https://legalref.judiciary.hk/lrs/images/expand.gif"alt="">,<spanclass=bigsize>CourtofFinalAppeal</a><aname=#H1></a></span>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?L1=FA#H1,null,,],[<imgsrc="https://legalref.judiciary.hk/lrs/images/expand.gif"alt="">,<spanclass=bigsize>CourtofAppealoftheHighCourt</a><aname=#H2></a></span>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?L1=CA#H2,null,,],[<imgsrc="https://legalref.judiciary.hk/lrs/images/expand.gif"alt="">,<spanclass=bigsize>CourtofFirstInstanceoftheHighCourt</a><aname=#H3></a></span>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?L1=HC#H3,null,,],[<imgsrc="https://legalref.judiciary.hk/lrs/images/expand.gif"alt="">,<spanclass=bigsize>CompetitionTribunal</a><aname=#H4></a></span>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?L1=CT#H4,null,,],[<imgsrc="https://legalref.judiciary.hk/lrs/images/expand.gif"alt="">,<spanclass=bigsize>DistrictCourt</a><aname=#H5></a></span>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?L1=DC#H5,null,,],[<imgsrc="https://legalref.judiciary.hk/lrs/images/expand.gif"alt="">,<spanclass=bigsize>FamilyCourt</a><aname=#H6></a></span>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?L1=FC#H6,null,,[null,Jointapplication</a><aname=#A1></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?L1=FC&L2=JA&AR=1#A1,null,,],[null,MatrimonialCauses</a><aname=#A2></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?L1=FC&L2=MC&AR=2#A2,null,,[null,2022</a><aname=#A2_1></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2022&AR=2_1#A2_1,null,,],[null,2021</a><aname=#A2_2></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2021&AR=2_2#A2_2,null,,],[null,2020</a><aname=#A2_3></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2020&AR=2_3#A2_3,null,,],[null,2019</a><aname=#A2_4></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2019&AR=2_4#A2_4,null,,],[null,2018</a><aname=#A2_5></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2018&AR=2_5#A2_5,null,,],[null,2017</a><aname=#A2_6></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2017&AR=2_6#A2_6,null,,],[null,2016</a><aname=#A2_7></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2016&AR=2_7#A2_7,null,,],[null,2015</a><aname=#A2_8></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2015&AR=2_8#A2_8,null,,],[null,2014</a><aname=#A2_9></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2014&AR=2_9#A2_9,null,,],[null,2013</a><aname=#A2_10></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2013&AR=2_10#A2_10,null,,],[null,2012</a><aname=#A2_11></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2012&AR=2_11#A2_11,null,,],[null,2011</a><aname=#A2_12></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2011&AR=2_12#A2_12,null,,],[null,2010</a><aname=#A2_13></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2010&AR=2_13#A2_13,null,,],[null,2009</a><aname=#A2_14></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2009&AR=2_14#A2_14,null,,],[null,2008</a><aname=#A2_15></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2008&AR=2_15#A2_15,null,,],[null,2007</a><aname=#A2_16></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2007&AR=2_16#A2_16,null,,],[null,2006</a><aname=#A2_17></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2006&AR=2_17#A2_17,null,,],[null,2005</a><aname=#A2_18></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2005&AR=2_18#A2_18,null,,],[null,2004</a><aname=#A2_19></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2004&AR=2_19#A2_19,null,,],[null,2003</a><aname=#A2_20></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2003&AR=2_20#A2_20,null,,],[null,2002</a><aname=#A2_21></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2002&AR=2_21#A2_21,null,,],[null,2001</a><aname=#A2_22></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2001&AR=2_22#A2_22,null,,],[null,2000</a><aname=#A2_23></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2000&AR=2_23#A2_23,null,,],[null,1999</a><aname=#A2_24></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1999&AR=2_24#A2_24,null,,],[null,1998</a><aname=#A2_25></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1998&AR=2_25#A2_25,null,,],[null,1997</a><aname=#A2_26></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1997&AR=2_26#A2_26,null,,],[null,1996</a><aname=#A2_27></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1996&AR=2_27#A2_27,null,,],[null,1995</a><aname=#A2_28></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1995&AR=2_28#A2_28,null,,],[null,1994</a><aname=#A2_29></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1994&AR=2_29#A2_29,null,,],[null,1993</a><aname=#A2_30></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1993&AR=2_30#A2_30,null,,],[null,1992</a><aname=#A2_31></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1992&AR=2_31#A2_31,null,,],[null,1991</a><aname=#A2_32></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1991&AR=2_32#A2_32,null,,],[null,1990</a><aname=#A2_33></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1990&AR=2_33#A2_33,null,,],[null,1988</a><aname=#A2_34></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1988&AR=2_34#A2_34,null,,],[null,1987</a><aname=#A2_35></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1987&AR=2_35#A2_35,null,,],[null,1984</a><aname=#A2_36></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1984&AR=2_36#A2_36,null,,],[null,1983</a><aname=#A2_37></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1983&AR=2_37#A2_37,null,,],[null,1982</a><aname=#A2_38></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1982&AR=2_38#A2_38,null,,],[null,1981</a><aname=#A2_39></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1981&AR=2_39#A2_39,null,,],[null,1980</a><aname=#A2_40></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1980&AR=2_40#A2_40,null,,],[null,1979</a><aname=#A2_41></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1979&AR=2_41#A2_41,null,,],[null,1978</a><aname=#A2_42></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1978&AR=2_42#A2_42,null,,],[null,1976</a><aname=#A2_43></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1976&AR=2_43#A2_43,null,,],[null,1975</a><aname=#A2_44></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1975&AR=2_44#A2_44,null,,],[null,1974</a><aname=#A2_45></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1974&AR=2_45#A2_45,null,,],[null,1972</a><aname=#A2_46></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=1972&AR=2_46#A2_46,null,,]],[null,MiscellaneousProceedings</a><aname=#A3></a>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?L1=FC&L2=MP&AR=3#A3,null,,]],[<imgsrc="https://legalref.judiciary.hk/lrs/images/expand.gif"alt="">,<spanclass=bigsize>LandsTribunal</a><aname=#H7></a></span>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?L1=LD#H7,null,,],[<imgsrc="https://legalref.judiciary.hk/lrs/images/expand.gif"alt="">,<spanclass=bigsize>Miscellaneous</a><aname=#H8></a></span>,https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?L1=OT#H8,null,,
    '''
    url_list_rule = r",\['<(.*)\]"
    myMenu_data_ = re.findall(url_list_rule, list_html)[0]
    myMenu_data = myMenu_data_.replace("'", '').replace(" ", '')
    return myMenu_data


def dispose_myMenu(myMenu_data):
    '''
    通过字符串切割处理为一个列表
    return : url_list    附上日期的url列表（# 第二层url列表）且在Max_Time时间之后的数据
    '''
    a_list = myMenu_data.split(',[')
    myMenu_list = []
    for i in a_list:
        li_ = i.split(',')
        myMenu_list.append(li_)            # 先切割处理为列表
    return myMenu_list


def get_F2_url_list(myMenu_list,URL_Max_Time,URL_S_Time):
    '''
    return :  F2_url_list : https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2022&AR=2_1#A2_1
    '''
    import_url_list = []
    for i in myMenu_list:
        this_url = i[2]
        '''
        'https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?L1=CT#H4'
        'https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?L1=DC#H5'
        'https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?L1=FC#H6'
          https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2022&AR=1_1#A1_1
         'https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2021&AR=1_2#A1_2'
         'https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2020&AR=1_3#A1_3'
        '''
        if 'EX=T&L1=FC&L2=' in this_url:
            import_url_list.append(this_url)

    F2_url_list = []
    for import_url in import_url_list:          # 筛选时间模块
        url_rule = r'&L3=(.*?)&AR='         # 匹配时间
        url_time = int(re.findall(url_rule,import_url)[0])
        if (url_time == URL_Max_Time) or ((url_time > URL_Max_Time) and (url_time < URL_S_Time)):
        # if (url_time == URL_Max_Time):
            F2_url_list.append(import_url)
    print(F2_url_list)
    return F2_url_list


def get_F3_url_list(F3_myMenu_list):
    '''
    return: 'https://legalref.judiciary.hk/lrs/common/ju/ju_frame.jsp?DIS=150584', 'https://legalref.judiciary.hk/lrs/common/ju/ju_frame.jsp?DIS=149395'
    '''
    F3_url_list = []
    for i in F3_myMenu_list:
        # print(i[1])
        url_data_ = i[1]
        if 'ju_frame.jsp?DIS=' in url_data_:
            url_data = url_data_.split('"href=javascript:matchpop(')[-1]  # 取最后一个
            url_data = url_data.replace("\\", '')
            F3_url_list.append(url_data)
    return F3_url_list


def dispose_F2_url(F2_url,page):
    '''
    在 F2_url 上添加 page 进行翻页
    input : https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2017&AR=2_6#A2_6
    return : https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&page=4&L1=FC&L2=MC&L3=2017&AR=2_6#A2_6
    '''
    if 'page=' in F2_url:
        F2_url = F2_url.replace(f'&page={page-1}&', f'&page={page}&', 1)        # &page=2&   ->   &page=3&
    else:
        F2_url = F2_url.replace('&', f'&page={page}&', 1)
    return F2_url


def get_PDF_html(F3_url,proxies):
    DIS_ID_rule = r'DIS=(.*)'
    DIS_ID = re.findall(DIS_ID_rule,F3_url)[0]         # 134724
    # PDF_headers = {
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    #     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    #     'Connection': 'keep-alive',
    #     # 'Cookie': 'JSESSIONID=FCF1C7E7B4F1EB90AF977748B93625F0; TS01f243ce=019fbe4eecea123d6635fd7a230a44642aef3d823d82bcd941a1d2816261a1b525c291c025787d2f6d7a33f57983cacc7c1a95690e6be6e9965a779ab74304cff3a02a5d22; BIGipServerpool_dc1_legalref.judiciary.hk_ext01_http=561062154.20480.0000; ispopup=0; curl=; jbudes=; fontsize=0; LrsLan=tc; TS01203efd=019fbe4eec22b9fda087b28d5878a7ba27f623693e48a4d7865867c7b6917ea06c4a400335671c7fc4f014a78e98f24b123518f8e0c72e48c4fe86e273a1db8184db4d081597754b09c8909cd87d972ecb9a102367',
    #     'Referer': 'https://legalref.judiciary.hk/lrs/common/ju/ju_frame.jsp?DIS=126056&currpage=',
    #     'Sec-Fetch-Dest': 'frame',
    #     'Sec-Fetch-Mode': 'navigate',
    #     'Sec-Fetch-Site': 'same-origin',
    #     'Upgrade-Insecure-Requests': '1',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    #     'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    #     'sec-ch-ua-mobile': '?0',
    #     'sec-ch-ua-platform': '"Windows"',
    # }
    PDF_url = f'https://legalref.judiciary.hk/lrs/common/ju/ju_body.jsp?DIS={DIS_ID}&AH=&QS=&FN=&currpage='
    # PDF_html = get_response_html(PDF_url,proxies)
    # print(f'正在获取F3_url -> {F3_url}  PDF_URL -> {PDF_url}')
    PDF_html = get_response_html(PDF_url,proxies)
    # print(PDF_html)
    return PDF_url,PDF_html


def run():
    F1_url_list = get_F1_url_list()         # https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&AR=1#A1
    URL_S_Time = 2024           # 只取这个之前的
    # URL_Max_Time = 2016
    URL_Max_Time = 1997        # 只获取1997之后的数据
    # Mysql_save_data = []
    F1_index = 0
    proxies = Get_ip.ip_proxies()
    for F1_url in F1_url_list:
        F1_index += 1
        F2_list_html = get_response_html(F1_url,proxies)        # 通过最初始url
        F2_myMenu_data = get_myMenu_data(F2_list_html)          # 获取到一个字符串
        F2_myMenu_list = dispose_myMenu(F2_myMenu_data)         # 将字符串切割为列表
        F2_url_list = get_F2_url_list(F2_myMenu_list,URL_Max_Time,URL_S_Time)      # 筛选符合条件的 F2 url
        F2_index = 0
        for F2_url in F2_url_list:      # https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=T&L1=FC&L2=MC&L3=2022&AR=2_1#A2_1
            F3_page = 1     # 初始化page
            F2_index += 1
            fanye_bool = False      # 是否已翻页
            F3_url_list = []
            First_F3_url_list = []
            while True:
                '''
                先保存当前页数据后 再判断是否有下一页，有的话修改 F2_url 并访问 F2_url 得到 F3_url_list
                '''
                if (fanye_bool == True) and (F3_page == 2):     # 翻到第二页，将第一页数据保存
                    First_F3_url_list = F3_url_list

                F3_list_html = get_response_html(F2_url,proxies)
                F3_myMenu_data = get_myMenu_data(F3_list_html)
                F3_myMenu_list = dispose_myMenu(F3_myMenu_data)
                F3_url_list = get_F3_url_list(F3_myMenu_list)
                print(F3_url_list)
                if (F3_url_list == First_F3_url_list) and (fanye_bool==True):
                    break               # 本页与第一页数据一样，说明没有这一页
                F3_index = 0
                for F3_url in F3_url_list:
                    F3_index += 1
                    print(f"F2_url : {F2_url} F1 -> {F1_index} / {len(F1_url_list)}   F2 -> {F2_index} / {len(F2_url_list)}   F3 -> {F3_index} / {len(F3_url_list)}  F3 page -> {F3_page}")
                    PDF_url,PDF_html = get_PDF_html(F3_url,proxies)
                    Mysql_one_dict = {'source_url': F2_url,'PDF_url':PDF_url, 'PDF_html': PDF_html}
                    # Mysql_save_data.append(Mysql_one_dict)
                    Mysql_save_data = [Mysql_one_dict]
                    manage_mysql.save_data(Mysql_table, Mysql_save_data)
                # Mysql_save_data = []
                proxies = Get_ip.ip_proxies()       # 更新ip

                if len(F3_url_list) == 50:  # 文件刚好为50（一页最大显示数量，说明可能有下一页）
                    F3_page += 1            # 1 -> 2
                    F2_url = dispose_F2_url(F2_url,F3_page)
                    fanye_bool = True
                else:
                    break

    Wx_Robot.send_data("域外法案例运行结束！！")


if __name__ == '__main__':
    run()

