# -*- coding: UTF-8 -*-
'''
@Project ：yj_pj 
@File ：demo.py
@Author ：hao
@Date ：2023/3/2 16:13
备注：澳大利亚域外法，通过读取csv来访问
'''


import pandas as pd
from lxml import html
from datetime import datetime
from wbh_word.spider import Get_response
from wbh_word.manage_data import manage_mysql

etree = html.etree
Pd_input_Path = 'D:/yj_pj/YWF/Australia/111.csv'
Mysql_table = 'ods_law_regulations'
source = 'Australia'    # 数据来源，一个程序中为固定值


def get_headers():
    headers = {
        'authority': 'www.legislation.gov.au',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        # 'cookie': 'C2018C00341SelectedNodeID=MainContent_ctl17_trTOCn8; C2022C00260SelectedNodeID=MainContent_ctl17_trTOCn0; F2023C00074SelectedNodeID=MainContent_ctl17_trTOCn0; F2023L00022SelectedNodeID=MainContent_ctl17_trTOCn1; F2023C00085SelectedNodeID=MainContent_ctl17_trTOCt2; F2021C01076SelectedNodeID=MainContent_ctl17_trTOCt43; F2021L01200SelectedNodeID=MainContent_ctl17_trTOCt100; C2022C00260=d17a8149-29d0-43c5-b2b3-ca4cd9cfdd9b; _ga=GA1.3.689505925.1677634770; _gid=GA1.3.365423045.1677634770; _hjSessionUser_1389221=eyJpZCI6IjBhMTBlM2RiLTkxMDYtNTg2Yy1iNTcyLWU1N2RlZjM5M2UzOCIsImNyZWF0ZWQiOjE2Nzc2MzQ3NzAzNzIsImV4aXN0aW5nIjp0cnVlfQ==; F2023C00108=a02bca23-333b-477e-ba7e-5d7785688aa0; _hjIncludedInSessionSample_1389221=1; _hjIncludedInPageviewSample=1; C2018C00341=5f37bd54-4576-4757-8af3-75f0a0ca30f5; F2023C00074=acbddc32-f604-48e0-872f-ec8977b96793; F2023L00022=df204e03-d0e7-4f43-81bf-0f39658c090f; F2021L01211=fa168968-1d3f-4b44-8e9c-d0b95341eb6e; C2021C00513=40721aa6-b507-4d65-8d55-3a57b7331fd5; F2021C01076=5851cb4e-9623-43f7-a898-af71e025bf66; F2023C00085=e8d5bb3a-ac32-48dc-81f6-86a4cc5cce09; F2021L01200=1ee86309-7095-49aa-9903-c29ae92cd1ce',
        'referer': 'http://localhost:63342/',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }
    return headers
headers = get_headers()


def read_pd_data():
    pd_data_list = pd.read_csv(Pd_input_Path, encoding='gbk')           # 法律名、法律文号、url
    print(pd_data_list)
    # print(pd_data_list['法律文号'])
    return pd_data_list


def get_detail_html(url):
    html_response,_ = Get_response.get_html_response(url,headers=headers)
    detail_html = html_response.text.replace('\xa0', '')
    return detail_html


def get_Volume_url_list(detail_html):
    '''
    防止出现多个链接拆分 ： Volume 1 、 Volume 2  导致缺少数据的bug
    '''
    Volume_url_list = []
    etr = etree.HTML(detail_html)
    volume_xp_list = etr.xpath(r'//div[@id="MainContent_ctl17_trTOC"]/table')  # 是否分上下卷
    if volume_xp_list:
        for volume_xp in volume_xp_list:
            volume_url = volume_xp.xpath(r'.//tr/td[2]/a/@href')
            Volume_url_list.append(volume_url[0])
    return Volume_url_list


def analysis_html_data(detail_html,pd_dict):
    Mysql_save_data = []
    load_time = str(datetime.now())  # 首次入库时间
    update_time = str(datetime.now())  # 首次入库时间
    index_id = 1000     # 从1000开始，步长为1000
    html_data = detail_html.replace('\xa0', '')  # 剔除NBSP
    # print(html_data)
    etr = etree.HTML(html_data)
    WordSection_data_list = etr.xpath(r'//div[@id="MainContent_pnlHtmlControls"]/div/div[starts-with(@class,WordSection)]')
    for WordSection_index in range(len(WordSection_data_list)):  # 1 为简介 、 2为目录
        # print(f" ===================== WordSection_data : {WordSection_data_list[WordSection_index]}  ===================== ")
        # main_data_list = WordSection_data.xpath(r'//div[@class="WordSection3"]/p | //div[@class="WordSection3"]/div | //div[@class="WordSection3"]/table')
        if int(WordSection_index) == 1:  # 0、1   ，第二个为目录，跳过
            print(" -----------------  跳过目录  -----------------")
            continue
        main_data_list = WordSection_data_list[WordSection_index].xpath(r'./p | ./div | ./table')
        '''
        div搜索： The process is carried out for the purpose of identifying any persons at risk
        '''
        all_content_str = ""
        all_special_str = ""
        chapter_level1 = ""
        chapter_level2 = ""
        chapter_level3 = ""
        chapter_level4 = ""
        chapter_level5 = ""
        # next_end_bool = False  # 当前小节  结束
        # special_bool = False  # 特殊的字段     # 放在special_data 字段中
        for main_index in range(len(main_data_list)):
            continue_bool = main_data_list[main_index].xpath(r'./self::p[@class="MsoHeader"]')  # 特殊处理、空白行
            if continue_bool:
                if main_index + 1 == len(main_data_list):  # 溢出判断
                    next_end_bool = True  # 防止出现最后一行为空白行，被直接continue掉的bug
                else:
                    continue  #
            '''
            注释部分：
            ENotesHeading1  对应 ActHead2
            ENotesHeading2  对应 ActHead3
            '''
            # Schedule2—State
            chapter_level1_data = main_data_list[main_index].xpath(r'./self::p[@class="ActHead1"]')
            # Part I—Preliminary
            chapter_level2_data = main_data_list[main_index].xpath(
                r'./self::p[@class="ActHead2"] | ./self::p[@class="ENotesHeading1"]')
            # Division 2—Protection of family
            chapter_level3_data = main_data_list[main_index].xpath(
                r'./self::p[@class="ActHead3"] | ./self::p[@class="ENotesHeading2"]')
            # Subdivision A—What this Division does
            chapter_level4_data = main_data_list[main_index].xpath(r'./self::p[@class="ActHead4"]')
            # 60A  What this Division does
            chapter_level5_data = main_data_list[main_index].xpath(r'./self::p[@class="ActHead5"]')
            LongT_data = main_data_list[main_index].xpath(r'./self::p[@class="LongT"]')  # 开头介绍

            hint_data = main_data_list[main_index].xpath(r'./self::div')  # 提示语
            table_data = main_data_list[main_index].xpath(r'./self::table')  # 表格，这个与文本一起存储
            # p标签（content）：  subsection : (1) xxx          paragraph : (a)         paragraphsub : (i) (ii)         notetext : 备注
            this_data = ("".join(main_data_list[main_index].xpath(r'.//text()'))).replace('\xa0', '')
            # print(f"this_data : {this_data}")

            if LongT_data or (WordSection_index == 0):
                special_bool = True
            else:
                special_bool = False

            if main_index + 1 == len(main_data_list):  # 溢出判断
                next_end_bool = True  # 即将溢出，当前小节结束
            else:
                next_level1_data = main_data_list[main_index + 1].xpath(r'./self::p[@class="ActHead1"]')
                next_level2_data = main_data_list[main_index + 1].xpath(
                    r'./self::p[@class="ActHead2"] | ./self::p[@class="ENotesHeading1"]')
                next_level3_data = main_data_list[main_index + 1].xpath(
                    r'./self::p[@class="ActHead3"] | ./self::p[@class="ENotesHeading2"]')
                next_level4_data = main_data_list[main_index + 1].xpath(r'./self::p[@class="ActHead4"]')
                next_level5_data = main_data_list[main_index + 1].xpath(r'./self::p[@class="ActHead5"]')
                if next_level1_data or next_level2_data or next_level3_data or next_level4_data or next_level5_data:
                    next_end_bool = True  # 下一个标签为标题，即、当前小节  结束
                else:
                    next_end_bool = False

            if chapter_level1_data:
                chapter_level1 = this_data
            elif chapter_level2_data:
                chapter_level2 = this_data
            elif chapter_level3_data:
                chapter_level3 = this_data
            elif chapter_level4_data:
                chapter_level4 = this_data
            elif chapter_level5_data:
                chapter_level5 = this_data
            else:  # this_data = content
                if special_bool == True:  # 特殊字段，没有content ， content -> special_list
                    # special_list.append(this_data)
                    all_special_str = all_special_str + '\n' + this_data
                else:
                    if ((table_data) or (hint_data)):  # 特殊处理，table 与 hint 要保存html格式
                        if table_data:
                            this_html = etree.tostring(table_data[0], encoding='utf-8')
                        elif hint_data:
                            this_html = etree.tostring(hint_data[0], encoding='utf-8')
                        content = this_html.decode()  # 保存html  ,   比特流转字符串
                    else:
                        content = this_data
                    # content_list.append(content)
                    all_content_str = all_content_str + content + '\n'

                if next_end_bool == True:  # 当本标签为文本 、 而下一个标签为标题时，说明当前小节结束、
                    law_code = pd_dict['pd_document_number']
                    if str(law_code) == 'nan':    # 这里可能会出现nan的情况，Mysql无法识别
                        law_code = ''
                    print(f"law_code : {law_code}")

                    sql_one_dict = {"law_url":pd_dict['pd_url'],'law_code':law_code,'law_name':pd_dict['pd_law_name'],
                                    "chapter_level1": chapter_level1, "chapter_level2": chapter_level2,"chapter_level3": chapter_level3,
                                    "chapter_level4": chapter_level4,"chapter_level5": chapter_level5, "law_content": all_content_str,
                                    "law_summary": all_special_str,"chapter_id":index_id,"source":source,"load_time":load_time,
                                    "update_time":update_time}
                    print(str(sql_one_dict)[:600], " \n\n ")
                    next_end_bool = False
                    special_bool = False
                    index_id += 1000       # 步长为1000
                    all_content_str = ""
                    all_special_str = ""
                    Mysql_save_data.append(sql_one_dict)
    return Mysql_save_data



def run():
    pd_data_list = read_pd_data()
    #     url_list = ['https://www.legislation.gov.au/Details/C2022C00260']
    for pd_index in range(len(pd_data_list)):
        pd_url = pd_data_list['url'][pd_index]
        pd_document_number = pd_data_list['法律文号'][pd_index]
        pd_law_name = pd_data_list['法律名'][pd_index]

        # for url in url_list:
        detail_html = get_detail_html(pd_url)
        Volume_url_list = get_Volume_url_list(detail_html)
        if len(Volume_url_list)<2:      # 0 、 1 # 只有一条链接的时候说明url不需要处理
            print(f"Volume_url_list 小于 1！！！ ： {Volume_url_list}")       # 直接用detail_html
            Volume_url = pd_url
            pd_dict = {'pd_url': Volume_url, 'pd_document_number': pd_document_number, 'pd_law_name': pd_law_name}

            Mysql_save_data = analysis_html_data(detail_html,pd_dict)
            if Mysql_save_data:
                try:
                    manage_mysql.save_data(Mysql_table, Mysql_save_data)
                except Exception as e:
                    raise f"保存失败！！："
        else:           # 有两个链接的时候，通过链接重新访问网址
            print(f"Volume_url_list 大于 1！！！ ： {Volume_url_list}")  # 直接用detail_html
            for Volume_url in Volume_url_list:
                detail_html = get_detail_html(Volume_url)       # 多一个步骤
                pd_dict = {'pd_url': Volume_url, 'pd_document_number': pd_document_number, 'pd_law_name': pd_law_name}

                Mysql_save_data = analysis_html_data(detail_html,pd_dict)
                if Mysql_save_data:
                    try:
                        manage_mysql.save_data(Mysql_table, Mysql_save_data)
                    except Exception as e:
                        raise f"保存失败！！："




if __name__ == '__main__':
    run()
