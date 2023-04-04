# -*- coding: UTF-8 -*-
'''
@Project ：yj_pj 
@File ：Analysis_PDF_Html.py
@Author ：hao
@Date ：2023/3/6 15:55 
'''
import time
from datetime import datetime

from lxml import html

from wbh_word.manage_data import manage_mysql

etree = html.etree

source = 'HongKong1997'
read_Table = 'YWF_Legalref_1997'
save_Table = 'ods_legislation'


def read_data():
    read_data_list = ['source_url','PDF_url','PDF_html']
    sql_data_list_ = manage_mysql.read_data(read_Table,read_data_list)

    sql_data = list(sql_data_list_)
    # print(sql_data)
    return sql_data


def analysis_PDF_Html(sql_dict):
    # sql_dict = {'source_url':source_url,'PDF_url':PDF_url,'PDF_html':PDF_html}
    etr = etree.HTML(sql_dict['PDF_html'])
    main_data_list = etr.xpath(r'//tr/td/*')

    First_heading = True
    data_list = []
    heading_title = ''  # 简介的标题
    next_title = ''     # 存储下一段的标题
    Mysql_save_data = []
    title = ''
    heading_html = ''
    content = ''  # 初始化
    load_time = str(datetime.now())
    update_time = str(datetime.now())  # 首次入库时间
    index_id = 1000
    for main_index in range(len(main_data_list)):
        # print(main_data.xpath(r'./text() | .//text()'))
        main_data = main_data_list[main_index]
        if main_index + 1 == len(main_data_list):  # 溢出判断
            next_main_data = ''  # 下一条溢出结束
        else:
            next_main_data = main_data_list[main_index + 1]

        this_text = main_data.xpath(r'./text() | .//text()')
        # print(f"this_text : {this_text}")
        this_str = "".join(this_text)
        save_bool = False  # 是否保存
        blockquote_bool = main_data.xpath(r'./self::blockquote')           # 当遇到表格
        heading_bool = main_data.xpath(r'./self::p[@class="heading"]')  # 当前是否为标题
        if First_heading and heading_bool:  # 当前为标题且第一次出现
            heading_html_list = main_data.xpath('./preceding-sibling::*')       # 显示当前标签的前面所有同级标签
            html_str_list = []
            for heading_html in heading_html_list:
                html_str_list.append(etree.tostring(heading_html, encoding='unicode', method='html'))
            heading_html = "".join(html_str_list)
            # heading_html_str = etree.tostring(heading_html)
            title = ''
            next_title = this_str
            data_list = []  # 清空else中添加的字符串

            print(f'heading_title == {title}')  # 摘要的标题
            print(f"heading_html : {heading_html}")  # 摘要
            First_heading = False
            save_bool = True

        elif heading_bool:  # 该条为标题或结束
            title = next_title  # 遇到标题，说明当前段落已结束
            next_title = this_str

            content = "\n".join(data_list)
            print(f'title == {title}')
            print(f'content == {content}')
            data_list = []
            save_bool = True
        elif next_main_data == '':  # 下一条结束
            title = next_title
            next_title = ''  # 无下一段的标题
            data_list.append(this_str)  # 添加字符串     # 结尾放在最后一节后面
            content = "\n".join(data_list)
            print(f'title == {title}')
            print(f'content == {content}')
            save_bool = True
        else:
            if blockquote_bool:     # 遇到表格保存html
                blockquote_html = etree.tostring(main_data, encoding='unicode', method='html')
                data_list.append(blockquote_html)
            else:
                data_list.append(this_str)  # 添加字符串


        if save_bool:
            if First_heading and heading_bool:  # 当前为标题且第一次出现
                First_heading = False
                title = heading_title
            Mysql_one_dict = {'chapter_id':index_id,'chapter_level':title,'legislation_summary':heading_html,
                              'legislation_content':content,'legislation_url':sql_dict['source_url'],'attachment_link':sql_dict['PDF_url'],
                              'source':source,'load_time':load_time,'update_time':update_time}
            Mysql_save_data.append(Mysql_one_dict)
            index_id += 1000
            title = ''
            heading_html = ''
            content = ''  # 初始化
            data_list = []
            print(f'Mysql_one_dict : {str(Mysql_one_dict)[:300]}')
            print(" =============================== \n")
    return Mysql_save_data

def run():
    sql_data_list = read_data()
    for sql_data in sql_data_list:
        source_url = sql_data[0]        # 数据来源
        PDF_url = sql_data[1]           # PDF连接
        PDF_html = sql_data[2]          # PDF源码
        sql_dict = {'source_url':source_url,'PDF_url':PDF_url,'PDF_html':PDF_html}
        Mysql_save_data = analysis_PDF_Html(sql_dict)


        print(" =============================== \n")
        if Mysql_save_data:
            manage_mysql.save_data(save_Table,Mysql_save_data)
        else:
            print(f'当前页无数据，跳过！！')
        print("\n\n ================ \n\n")



if __name__ == '__main__':
    run()

