# -*- coding: UTF-8 -*-
'''
@Project ：yj_pj 
@File ：demo.py
@Author ：hao
@Date ：2023/2/15 17:12
'''
# 将lxml模块改为parsel
import re
import time
from datetime import datetime

import pandas as pd
from loguru import logger
from parsel import Selector
from wbh_word.spider import Get_response
from wbh_word.manage_data import manage_mysql


# Mysql_table = 'ods_law_regulations_HongKong'
Mysql_table = 'ods_law_regulations'
Pd_input_Path = 'D:/yj_pj/YWF/HongKong_elegislation/111.csv'
source = 'HongKong'    # 数据来源，一个程序中为固定值

def get_headers():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'TaJM6jvsmH6aaGE39F7o7inO=v1LMI1JQSDxFt; CLIENT_URL_FORWARD=UBIeSAUCHhxHERwTWFQDDVEFVFBHWQkFE1pXEERQHRdZWB8FCk0MAFQ=; TaJM6jvsmH6aaGI39F7o7inO=v1LMIxJQSDi2f; CLIENT_CONFIG_RESULT_ATTRIBUTE=%7B%22isOSSupported%22%3Atrue%2C%22isJvmVersionSupported%22%3Afalse%2C%22isBrowserSupported%22%3Atrue%2C%22isJvmSupported%22%3Afalse%2C%22isOSVersionSupported%22%3Atrue%2C%22isBrowserVersionSupported%22%3Atrue%7D; CLIENT_CONFIG_ATTRIBUTE=%7B%22branchCode%22%3A%2200%22%2C%22jvmVendor%22%3A%22%22%2C%22osVersion%22%3A%22Windows+10%22%2C%22jvmVersion%22%3A%22%22%2C%22browserVersion%22%3A%22109.0%22%2C%22isJavascriptEnabled%22%3Atrue%2C%22browserName%22%3A%22Chrome%22%2C%22userAgent%22%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F109.0.0.0+Safari%2F537.36%22%2C%22applicationId%22%3A%22RA001%22%2C%22osName%22%3A%22Windows%22%2C%22isJvmEnabled%22%3Afalse%2C%22isCookieEnabled%22%3Atrue%7D; CLIENT_REDIRECT_URL_ATTRIBUTE=https://www.elegislation.gov.hk/client-check; clientCheckStatus=S; fontSize=default; JSTP2=DE31B766456B299130887D4DD1BB75F7; JSWP2=EF043D285078425AAB8CFDBFADCEAC27',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    return headers
def get_cookies():
    cookies = {
        'clientCheckStatus': 'S',
    }
    return cookies

headers = get_headers()
cookies = get_cookies()


def read_pd_data():
    pd_data_list = pd.read_csv(Pd_input_Path, encoding='gbk')          # 法律名、法律文号、url
    # print(pd_data_list['法律文号'])
    return pd_data_list


def get_lvid(url):
    # response = requests.get(url,cookies=cookies, headers=headers)
    response,_ = Get_response.get_html_response(url, headers=headers,cookies=cookies)
    # print(response.text)
    html_data = response.text
    etr = Selector(text=html_data)
    # etr = etree.HTML(html_data)
    lvid = etr.xpath('//input[@name="_ae"]/@value').getall()  # 这里有id说明是章节页，有整个章节数据，，没有说明是具体的某一条
    if lvid[0] != '':
        return_data = lvid[0]
        lvid_or_jsurl = 'lvid'
        print(f'lvid: {return_data}')
    else:
        hash_rule = '/vlisscript\?(.*)"'        # https://www.elegislation.gov.hk/vlisscript?skipHSC=true&hash=cbc32e72e53f3289c13ca2d43101cc36&_os=0
        hash_data = re.findall(hash_rule, html_data)
        js_url = 'https://www.elegislation.gov.hk/vlisscript?' + hash_data[0]
        lvid_or_jsurl = 'js_url'
        print(f'js_url: {js_url}')
        return_data = js_url
    return return_data,lvid_or_jsurl

def get_chapter_html(lvid):         # 通过 lvid 获取整个章节数据
    params = {
        'skipHSC': 'true',  # 当LANGUAGE 为C（繁体）时，这里选择true
        # 'translateSC' : 'true',     # 是否翻译，当LANGUAGE 为S（简体）时，这里选择true
    }
    data = {
        'LANGUAGE': 'C',  # S 为简体， C为繁体 ， E为英语
        'BILINGUAL': '',
        'QUERY': '.',
        'INDEX_CS': 'N',
        'PUBLISHED': 'true',
        'lvid': lvid,
        #     30067     1
        #     30977     2       有 部数、附表
        #     39276     3
    }
    chapter_url = 'https://www.elegislation.gov.hk/xml'
    # response = requests.post('https://www.elegislation.gov.hk/xml', params=params,data=data, cookies=cookies, headers=headers)
    chapter_html,_ = Get_response.post_html_response(chapter_url,headers=headers,params=params,data=data, cookies=cookies)
    chapter_html = chapter_html.text
    return chapter_html


def get_detail_html(jsurl,_Query):          # 具体某一条的数据,先获取 _u 参数后 再去访问详情页具体数据
    '''
    jsurl --> _u        获取 _u (law_code)参数
    pd_url --> QUERY    pd_url正则匹配出搜索关键词
    _u + QUERY  ==>>   detail_data
    '''
    headers2 = {
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'Referer': 'https://www.elegislation.gov.hk/hk/cap336H!zh-Hant-HK@2017-11-16T00:00:00?c.EX_CHAPTER_NO=&k.SER_KWD=%E5%A9%9A%E5%A7%BB&pmc=0&k.WTXT=Y&m=0&pm=1&k.PTYPE=C&k.SER_FLD=E&k.SER_MODE=P',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
    }
    # response = requests.get(jsurl, headers=headers,cookies=cookies)
    js_response,_ = Get_response.get_html_response(url=jsurl, headers=headers2,cookies=cookies)
    # js_response = 'var provisions=[{_ac:"22/07/2021 00:00:00",_ab:"22/07/2021 00:00:00",_ae:36823,_ad:2,_af:"2021-07-22 00:00:00.0",ORDER_NO:1,BILINGUAL_TITLE:"釋義",HAS_IND_RTF:"Y",CAP_NO:"336F",_a:"22/07/2021 00:00:00",PROV_TYPE:"S",_b:"22/07/2021 00:00:00",_c:375619,_d:"",_e:"N",_f:"2",_g:"第2條",_h:"N",_i:"s2",_j:"ID_1438403028020_003",_k:"22/07/2021 00:00:00",ENG_CAP_TITLE:"District Court (Fixed Costs in Matrimonial Causes) Rules",_l:375605,_m:"",_n:"N",CHI_CAP_TITLE:"《區域法院(婚姻訴訟定額訟費)規則》",_o:"2",PROV_TITLE:"釋義",_p:"Rule 2",ENG_TITLE:"Interpretation",_q:"N",_r:"s2",_s:"ID_1438403028020_002",_t:375619,_u:2573235,_w:"N",_z:"ID_1438403028020_003",END_DT:"9999-12-31 23:59:59.0",_aa:"31/12/9999 23:59:59",CHI_TITLE:"釋義"}];'
    js_response = js_response.text
    js_list_rule = ',_u:(.*?),'
    js_list_ = re.findall(js_list_rule, js_response)
    _u_data = js_list_[0]
    print(f'_u_data : {_u_data}')       # '2125701'

    data = {
        'LANGUAGE': 'C',
        'BILINGUAL': '',
        'LEG_PROV_MASTER_ID': _u_data,      # '2125701'
        'QUERY': _Query,                    # 这个关键字一定要改！！  %E5%A9%9A%E5%A7%
        'INDEX_CS': 'N',
        'PUBLISHED': 'true',
    }
    params = {
        'skipHSC': 'true',
    }
    detail_url = 'https://www.elegislation.gov.hk/xml'
    # response = requests.post('https://www.elegislation.gov.hk/xml', params=params, cookies=cookies, headers=headers, data=data)
    detail_response,_ = Get_response.post_html_response(url=detail_url,params=params, data=data, cookies=cookies, headers=headers)
    detail_html = detail_response.text
    return detail_html,_u_data


def append_content_data(change_bool,content_data,this_data):
    '''
        change_bool：是否换行
        content_data：原本的数据
        this_data：当前需要拼接的数据
    '''
    if change_bool:
        content_data = content_data + '\n' + this_data
    else:
        content_data = content_data + this_data
    return content_data


def dispose_referencenote(content_data,this_floor):
    # # ./paragraph/content/referencenote       [比照1882c.75s.18U.K.]
    referencenote_html = this_floor.xpath(r'./referencenote/text()').getall()
    if referencenote_html:
        referencenote_text = (''.join(referencenote_html).replace(' ', '').replace('\n', ''))
        content_data = content_data.replace(referencenote_text, f'\n{referencenote_text}')  # 在前面添加 \n
    return content_data


def dispose_sourcenote(content_data,this_floor):       # 特殊处理备注问题
    '''
    需要换行：
    (由1975年第92號第59條修訂；由1998年第25號第2條修訂)
    '''
    # (由1975年第92號第59條修訂；由1998年第25號第2條修訂)
    sourcenote_html = this_floor.xpath(r'./sourcenote/text()').getall()
    if sourcenote_html:
        sourcenote_text = (''.join(sourcenote_html).replace(' ', '').replace('\n', ''))
        content_data = content_data.replace(sourcenote_text, f'\n{sourcenote_text}')  # 在前面添加 \n
    return content_data


def dispose_paragraph(paragraph_floor,paragraph_html,content_data):       # 处理paragraph_floor 层级
    '''
    input:[paragraph_html] paragraph的列表，如果有数据代表当前标签为 paragraph
    output: this_data 处理并返回paragraph下的所有数据
    '''
    # for paragraph_floor in paragraph_floor_list:
    #     paragraph_html = paragraph_floor.xpath(r'./self::paragraph')
    if paragraph_html:
        four_floor_list = paragraph_html[0].xpath(r'./*')  # 当前为 paragraph 标签下的所有标签
        for four_floor in four_floor_list:
            change_bool = four_floor.xpath(r'./self::num').getall()  # (a)  (b)  (c)
            this_data = (''.join(four_floor.xpath(r'.//text()').getall())).replace(' ', '').replace('\n', '')
            content_data = append_content_data(change_bool, content_data, this_data)
            content_data = dispose_sourcenote(content_data,this_floor=four_floor)

    else:       # 当前为 paragraph 标签的上一级标签
        this_data = (''.join(paragraph_floor.xpath(r'.//text()').getall())).replace(' ', '').replace('\n', '')
        change_bool = paragraph_floor.xpath(r'./self::num').getall()  # (a)  (b)  (c)
        content_data = append_content_data(change_bool, content_data, this_data)
        content_data = dispose_sourcenote(content_data, this_floor=paragraph_floor)

    return content_data


def get_content_data(main_data):        # 处理获得正文,  # 换行拼接需要细化到 (a),(b),(c)
    '''
    one_floor_list: 第一层为当前标签下所有的标签
    当遇到 subsection 标签时进入，否则直接拼接
    two_floor_list：第二层为subsection下的所有标签
    当遇到 paragraph 标签时进入
    three_floor_list: 第三层为paragraph下的所有标签

    '''
    content_data = ''
    one_floor_list = main_data.xpath(r'./section/*')
    for one_floor in one_floor_list:
        subsection_html = one_floor.xpath(r'./self::subsection')        # (1)  (2)  (3)
        if subsection_html:          # 当前为 subsection 标签，
            two_floor_list = subsection_html[0].xpath(r'./*')   # 当前为 subsection 标签下的所有标签
            for two_floor in two_floor_list:
                def_html = two_floor.xpath(r'./self::def')
                if def_html:            # 进入def标签
                    def_leadin_html = two_floor.xpath(r'./leadin')
                    if def_leadin_html:         # def 下正常格式
                        three_floor_list = def_html[0].xpath(r'./*')  # 当前为 paragraph 标签下的所有标签
                        for three_floor in three_floor_list:
                            paragraph_html = three_floor.xpath(r'./self::paragraph')
                            content_data = dispose_paragraph(three_floor, paragraph_html, content_data)

                    else:       # 不规则，直接获取全部文本
                        def_data = def_html[0].xpath(r'./text() | .//text()').getall()
                        this_data = (''.join(def_data)).replace(' ', '').replace('\n', '')
                        content_data = content_data + this_data

                else:       # 进入 paragraph 标签
                    paragraph_html = two_floor.xpath(r'./self::paragraph')
                    content_data = dispose_paragraph(two_floor, paragraph_html, content_data)
                    content_data = dispose_referencenote(content_data, one_floor)       # subsection 下的 referencenote


        else:            # 当前不为 subsection 标签（直接拼接   换行 + 数据）
            this_data = (''.join(one_floor.xpath(r'.//text()').getall())).replace(' ', '').replace('\n', '')
            # print(f'one_data : {this_data}')
            no_change_bool = one_floor.xpath(r'./self::num | ./self::heading').getall()      # 1.簡稱      2.適用範圍
            if no_change_bool:
                content_data = content_data + this_data         # 这个标题不需要换行，要特殊处理
            else:
                content_data = content_data + '\n' + this_data
            content_data = dispose_referencenote(content_data,one_floor)        # 不为 subsection 也可能直接进入了 paragraph

    content_data = content_data
    return content_data


def analysis_html_data(html_data,pd_dict):
    etr = Selector(text=html_data)
    # etr = etree.HTML(html_data.encode('utf-8'))

    main_data_list = etr.xpath(r'//main')
    chapter_level1 = ''  # 一级标题         第x部
    chapter_level2 = ''  # 二级标题         第x分部
    chapter_level3 = ''  # 二级标题         小标题： 1.
    content = ''
    law_summary = ''
    fubiao_bool = False  # 当前标签是否为附表
    introduction_bool = False  # 出现第xx部的时候，里面没有内容，只有开头的论述/导言
    # properties_master_list = etr.xpath(r'//properties/@master')
    # print(properties_master_list)           # law_code  具体某条法律的id
    load_time = str(datetime.now())  # 首次入库时间
    update_time = str(datetime.now())         # 首次入库时间
    Mysql_save_data = []
    index_id = 1000     # 初始索引为1000，步长1000
    for main_index in range(len(main_data_list)):

        main_data = main_data_list[main_index]
        # all_data_list = main_data.xpath(r'.//text()')
        # all_data = ''
        # for all_data_str in all_data_list:
        #     all_data_ = all_data_str.replace(' ', '').replace('\n', '')
        #     all_data = all_data + '\n' + all_data_
        all_data = (''.join(main_data.xpath(r'.//text()').getall())).replace(' ', '')

        print(str(all_data)[:300])  # 全部数据
        # properties_master = properties_master_list[main_index]
        # print(f'properties_master : {properties_master}')
        # law_code = properties_master  # 具体某条法律id

        one_chapter = ''  # 一级标题章节
        one_chapter_ = main_data.xpath(r'./part/num/text()').getall()  # 第1部、第2部
        print(f"one_chapter_ : {one_chapter_}")
        if one_chapter_:  # ['第III部']  / []      为空说明不需要切换
            introduction_bool = True

        if not one_chapter_:  # 当 没有一级标题，查看是否有附表
            one_chapter_ = main_data.xpath('./schedule/num/text() | ./appendix/text/table/text()').getall()  # 附表1、附表2,有则直接取html数据
            if one_chapter_:
                fubiao_bool = True
            else:
                fubiao_bool = False
            print(f"fubiao_bool : {fubiao_bool}")
        if one_chapter_:
            one_chapter = one_chapter_  # 如果有数据，说明是出现第xxx部  或附表1、附表2

        two_chapter = main_data.xpath(r'./division/num/text()').getall()  # 第x分部        后面还要 + heading
        three_chapter = main_data.xpath(r'./section/num/text()').getall()  # 标题的数字（第几章第几节）

        heading = main_data.xpath(r'.//heading/text() | .//heading//text()').getall()
        if fubiao_bool == True:  # 当有附表时，会有额外的标题，这里只取一个
            if heading:
                heading = heading[0]
            else:
                heading = ""
        else:
            heading = "".join(heading)
        '''
        one_chapter : 第1部 ------ two_chapter :      three_chapter:
        heading : 導言
        leadIn : 
        paragraph : 
        content : 
        sourceNote : 
        '''
        one_chapter = ("".join(one_chapter)).replace(" ", "")
        two_chapter = ("".join(two_chapter)).replace(" ", "")
        three_chapter = "".join(three_chapter)
        if (not one_chapter) and (not two_chapter) and (not three_chapter):  # 都没有，说明是标题  开头的论述/导言
            introduction_bool = True
        '''    
        备注：这三个标题只会出现其中一个，出现了一个另外两个就不会出现
        if not three_chapter:  # 没有三级标题
            if not two_chapter:     # 没有二级标题和三级标题时（说明是一级标题）
                chapter_level1 = one_chapter + " " + heading  # one_chapter : 第1部 导言 ----- two_chapter: 第一分部xxxx  three_chapter: 1. ----- heading : 簡稱
                chapter_level2 = ""
                chapter_level3 = ""  # 切换一级标题的时候，无二级标题
            elif not one_chapter:   # 没有一级标题和三级标题时（说明是二级标题）
                chapter_level2 = two_chapter + " " + heading
                chapter_level3 = ""  # 切换一级标题的时候，无二级标题
        else:   # 切换三级标题
            chapter_level3 = three_chapter + " " + heading  # 60. 離婚不獲第三地方承認並不禁制再婚      (多加一个空格方便后续处理)
        '''

        if one_chapter:
            print(f"我到这里啦 chapter_level1 one_chapter:{one_chapter}==================")
            chapter_level1 = one_chapter + " " + heading
            chapter_level2 = ""
            chapter_level3 = ""  # 切换一级标题的时候，无 二、三 级标题
        if two_chapter:
            chapter_level2 = two_chapter + " " + heading
            chapter_level3 = ""  # 切换一级标题的时候，无二级标题
        if three_chapter:
            chapter_level3 = three_chapter + " " + heading  # 60. 離婚不獲第三地方承認並不禁制再婚      (多加一个空格方便后续处理)

        if fubiao_bool == True:  # 如果是附表，就只有 一级 标签
            chapter_level2 = ""
            chapter_level3 = ""

        print(
            f'chapter_level1 : {chapter_level1} ---chapter_level2 : {chapter_level2}--- chapter_level3 : {chapter_level3}')
        print(f'heading : {heading}')

        content_heard_data_ = three_chapter + heading  # 正文 = 三级标题+标签         60.離婚不獲第三地方承認並不禁制再婚

        '''
        # 文本 = 引入 + 内容
        leadIn = ''.join(main_data.xpath(r'.//leadin//text()'))  # 引入
        # print(f'leadIn : {leadIn}')
        paragraph = ''.join(main_data.xpath(r'.//paragraph//text()'))  # 内容
        # print(f'paragraph : {paragraph}')
        content = leadIn + paragraph
        # content = content.replace(' ', '').replace('\n', '')
        if not content:
            content = ''.join(main_data.xpath(r'.//content//text()'))
        '''



        if fubiao_bool == True:  # 是否为附表,附表直接保存html
            content = main_data.extract()
            # content = etree.tostring(main_data, encoding='utf-8').decode()
        else:
            if introduction_bool == True:       # 是否为论述、导言
                law_summary = all_data  # 论述、导言，直接全部文本储存

                introduction_bool = False  # 令状态变回初始化
            else:       # 正文部分
                content = get_content_data(main_data)

        if law_summary or content:
            Mysql_one_dict = {'law_url':pd_dict['pd_url'],'law_code':pd_dict['pd_law_code'],'law_name':pd_dict['pd_law_name'],'chapter_id':index_id,
                              'chapter_level1':chapter_level1,'chapter_level2':chapter_level2,'chapter_level3':chapter_level3,'law_content':content,
                              "law_summary":law_summary,"source":source,"load_time":load_time,'update_time':update_time}
            Mysql_save_data.append(Mysql_one_dict)
            law_summary = ''
            content = ''
            print(f'Mysql_one_dict : { str(Mysql_one_dict)[:350]}')
            print("\n ================ \n")
            index_id += 1000    # 步长1000

    return Mysql_save_data

def run():
    # url_list = ['https://www.elegislation.gov.hk/hk/cap331!zh-Hant-HK@2020-09-10T00:00:00/sch2?k.PTYPE=C&k.SER_KWD=%E5%A9%9A%E5%A7%BB&k.SER_FLD=E&k.WTXT=Y&k.SER_MODE=P&SER_OPT=K&c.EX_CHAPTER_NO=',
    #             'https://www.elegislation.gov.hk/hk/cap16']
    pd_data_list = read_pd_data()
    print(pd_data_list)
    # for url in url_list:
    url_list = pd_data_list['url']
    law_code_list = pd_data_list['法律文号']
    law_name_list = pd_data_list['法律名']
    for pd_index in range(len(pd_data_list)):

        # Mysql_dict = {}
        pd_url = url_list[pd_index]
        pd_law_code = law_code_list[pd_index]
        pd_law_name = law_name_list[pd_index]
        pd_dict = {'pd_url':pd_url,'pd_law_code':pd_law_code,'pd_law_name':pd_law_name}       # 构建一个临时的字典，方便后续调用
        print(pd_dict)


        return_data,lvid_or_jsurl = get_lvid(pd_url)
        if lvid_or_jsurl == 'lvid':             # 一整章数据
            lvid = return_data
            lvid_resposne_html = get_chapter_html(lvid)
            will_analysis_html = lvid_resposne_html
        else:                               # 一小条数据
            jsurl = return_data
            Query_list_rule = 'k.SER_KWD=(.*?)&'
            Query_list_ = re.findall(Query_list_rule, pd_dict['pd_url'])  # 搜索关键词,从url中获取  %E5%A9%9A%E5%A7%
            _Query = Query_list_[0]
            print(f'_Query : {_Query}')  # %E5%A9%9A%E5%A7%   搜索关键词
            detail_html,law_code = get_detail_html(jsurl,_Query)
            will_analysis_html = detail_html


        Mysql_save_data = analysis_html_data(will_analysis_html, pd_dict)

        print(f'Mysql_save_data : {str(Mysql_save_data)[:250]}')

        if Mysql_save_data:
            manage_mysql.save_data(Mysql_table,Mysql_save_data)
        else:
            print(f'当前页无数据，跳过！！')
        print("\n\n ================ \n\n")
        # time.sleep(1)


if __name__ == '__main__':
    run()
