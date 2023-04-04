# -*- coding: UTF-8 -*-
'''
@Project ：yj_pj 
@File ：demo.py
@Author ：hao
@Date ：2023/2/22 11:29 
'''


import re
import time
from datetime import datetime

import pandas as pd
from lxml import html
from wbh_word.spider import Get_response
from wbh_word.manage_data import manage_mysql

etree = html.etree

Pd_input_Path = 'D:/yj_pj/YWF/Macao/111.csv'
Mysql_table = 'ods_law_regulations'
source = 'Macao'

def get_header():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'ASPSESSIONIDQGSRBDSB=NOAILAHCBJPKIDEKFNCFKIHI; cookiesession1=678A8C35B99C7FA1EA7A74A004731BDD; ASPSESSIONIDQUBTDTSR=HLMMAEGCACGBKFCBEPPDOEHL; __utmc=17830817; __utmz=17830817.1676540205.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=17830817.2116556585.1676540205.1676540205.1676875979.2; ASPSESSIONIDAUTSRQDD=PNGMKCHBMJMPKJFHNBHAOFBF; __utmb=17830817.4.10.1676875979',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    return headers
headers = get_header()


def read_pd_data():
    pd_data_list_ = pd.read_csv(Pd_input_Path, encoding='gbk')           # 法律名、法律文号、url
    pd_data_list = disopse_url_data(pd_data_list_)
    print(pd_data_list)
    # print(pd_data_list['法律文号'])
    return pd_data_list


def disopse_url_data(pd_data_list):
    '''
    https://bo.io.gov.mo/bo/i/99/31/codcivcn/default.asp
    链接处理（目录页 -> 详情页）  ->        第39/99/M號法令
    https://bo.io.gov.mo/bo/i/99/31/codcivcn/declei39.asp
    '''
    for pd_index in range(len(pd_data_list)):
        pd_url = pd_data_list['url'][pd_index]
        pd_document_number = pd_data_list['法律文号'][pd_index]
        if 'declei' in pd_url:
            url = pd_url

        else:       #
            url_rule = r'.*/'       # 贪婪匹配  https://bo.io.gov.mo/bo/i/99/31/codcivcn/default.asp -> https://bo.io.gov.mo/bo/i/99/31/codcivcn/
            url_ = re.findall(url_rule, pd_url)[0]
            law_number_rule = r'第(.*?)/'        # '第48/96/M號法令' -> 48
            document_number = re.findall(law_number_rule, pd_document_number)[0]
            # print(law_number)
            url = url_ + f'declei{document_number}.asp'
        # print(url)
        pd_data_list['url'][pd_index] = url     # 修改url
        # print(pd_data_list['url'][pd_index])
    return pd_data_list


def get_detail_html(url):
    detail_html_response,_ = Get_response.get_html_response(url,headers=headers)
    # aaa = cchardet.detect(response.content)['encoding']       #  通过 cchardet 获取返回数据的编码
    detail_html_response.encoding = 'BIG5'
    detail_html = detail_html_response.text
    return detail_html


def analysis_html_data(html_data,pd_dict):
    html_data = html_data.replace('\xa0', '')  # 剔除NBSP
    # print(html_data)
    etr = etree.HTML(html_data)
    main_data_list = etr.xpath(r'//div[@class="margincontent"]/h2 | //div[@class="margincontent"]/h3 | //div[@class="margincontent"]/p')
    law_name = ''
    law_summary_bool = True  # 是否保存摘要       # 只保存一次
    First_save_h3_nobr = True   # 是否为第一次存储h3_nobr
    save_h3_nobr = False        # 是否需要存储h3_nobr，默认无
    chapter_level1 = ''  # 一级标题
    chapter_level2 = ''  # 二级标题
    chapter_level3 = ''
    p_text = ''
    Mysql_save_data = []
    load_time = str(datetime.now())
    update_time = str(datetime.now())  # 首次入库时间
    index_id = 1000
    for main_index in range(len(main_data_list)):
        # 章 、 節（节） 、 條（条）
        h2_bool = main_data_list[main_index].xpath(r'./self::h2')
        h3_bool = main_data_list[main_index].xpath(r'./self::h3 | ./self::p[@align="center"]')
        h3_nobr = main_data_list[main_index].xpath(r'./nobr')  # [ ^ ] [ 民事登記法典 - 目錄 ] [ 民事登記法典 - 條文目錄 ]....
        if h3_nobr:
            save_h3_nobr = True  # 是否保存h3_nobr       # 只保存一次

        if h3_bool:  # 有h3 ，则无p标签
            p_bool = ''
        else:
            p_bool = main_data_list[main_index].xpath(r'./self::p')
        this_data = "".join(main_data_list[main_index].xpath(r'.//text()'))

        if main_index + 1 == len(main_data_list):  # 溢出判断
            next_data = ""
            next_p_bool = ""
        else:
            next_data = "".join(main_data_list[main_index + 1].xpath(r'.//text()'))
            # next_p_bool = main_data_list[main_index+1].xpath(r'./self::p')
            next_h3_bool = main_data_list[main_index + 1].xpath(r'./self::h3 | ./self::p[@align="center"]')
            # h3:        .xpath(r'./self::p[@align="center"]')
            if next_h3_bool:  # 有h3 ，则一定无p标签
                next_p_bool = ''
            else:  # 无h3标签，判断下一个是否为p标签
                next_p_bool = main_data_list[main_index + 1].xpath(r'./self::p')
        # print(f"\n------------- this_data : {this_data} --------------")

        if h2_bool:  # ['第39/99/M號法令'] ['民法典']
            law_name = this_data
        if h3_nobr:
            pass
        elif h3_bool:  # ['第一編'] ['登記之性質及價值'] ['第一章'] ['一般規定'] ['第一節'] ['一般規則'] ['第一條'] ['（《民法典》之核准）']
            # if '編' in this_data:
            #     chapter_level1 = this_data + next_data           # ['第一編'] ['登記之性質及價值']
            if '章' in this_data:
                chapter_level1 = this_data + next_data  # 本条数据 + 下一条数据         # ['第一章'] ['一般規定']
            if '節' in this_data:
                chapter_level2 = this_data + next_data
            if '條' in this_data:
                chapter_level3 = this_data + next_data

        if p_bool or (h3_nobr and First_save_h3_nobr):
            p_text_ = this_data
            p_text = p_text + p_text_ + '\n'
            if (not next_p_bool) or (save_h3_nobr and First_save_h3_nobr):  # 判断下一行是否有p标签 或 当前为：[ ^ ] [ 民事登記法典 - 目錄 ]
                if save_h3_nobr and First_save_h3_nobr:            # 先判断是否是第一次存储h3_nobr
                    law_summary = p_text
                    content = ""
                    First_save_h3_nobr = False
                elif law_summary_bool:       # 添加摘要
                    law_summary = p_text
                    content = ""
                    law_summary_bool = False       # 一个文章只有一个摘要
                else:
                    law_summary = ""
                    content = p_text
                p_text = ""
                Mysql_one_dict = {'law_url': pd_dict['pd_url'], 'law_code': pd_dict['pd_document_number'],'law_name':  pd_dict['pd_law_name'],
                                  'chapter_level1': chapter_level1,'chapter_level2': chapter_level2, 'chapter_level3': chapter_level3,
                                  'law_content': content,'law_summary':law_summary,'chapter_id':index_id,
                                  'source':source,'load_time':load_time,'update_time': update_time}
                index_id += 1000
                Mysql_save_data.append(Mysql_one_dict)
                print(f'Mysql_one_dict : {str(Mysql_one_dict)[:500]}')
                print(" =============================== \n")
    return Mysql_save_data

def run():
    pd_data_list = read_pd_data()
    for pd_index in range(len(pd_data_list)):
        pd_url = pd_data_list['url'][pd_index]
        pd_document_number = pd_data_list['法律文号'][pd_index]
        pd_law_name = pd_data_list['法律名'][pd_index]
        # url 、 法律文号 、 法律名
        pd_dict = {'pd_url': pd_url, 'pd_document_number': pd_document_number,'pd_law_name': pd_law_name}

        detail_html = get_detail_html(pd_url)
        Mysql_save_data = analysis_html_data(detail_html, pd_dict)
        time.sleep(2)
        print(" =============================== \n")
        if Mysql_save_data:
            manage_mysql.save_data(Mysql_table,Mysql_save_data)
        else:
            print(f'当前页无数据，跳过！！')
        print("\n\n ================ \n\n")


if __name__ == '__main__':
    run()
