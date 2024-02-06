# -*- coding: UTF-8 -*-
'''
@Project ：yj_pj 
@File ：Move_Mysql_Different_DB.py
@Author ：hao
@Date ：2023/4/18 16:53
# 将一个库的表迁移到另外一个库的表中
old_DB.old_Table -> new_DB.new_Table
'''
from wbh_word.manage_database.db_connection_pool import DbTool


def read_data(table,data_list,DB):
    '''
    data_list：需要访问的字段列表 [id，meetid]
    '''
    key_data = ''       # `abc`,`bdc`
    for data in data_list:
        d1 = f'`{data}`,'
        key_data += d1
    key_data = key_data[:-1]        # 此时末位多出一个逗号,剔除
    # if old_or_new == 'old':
    #     sql = '''SELECT {key_data} FROM ods_data.{table}'''.format(key_data=key_data,table=table)
    # elif old_or_new == 'new':
    sql = '''SELECT {key_data} FROM {table}'''.format(key_data=key_data, table=table)

    # sql = '''SELECT * FROM ods_data.{table}'''.format(table=table)
    rest = DB.selectall(sql)

    return rest


def save_data(table, data_list,DB):
    """
    data_list ：  [{"开始时间": '123123123',"结束时间": '12412412'},{"开始时间": 'asdas',"结束时间": 'asdasd'}]
    """
    data_list = [{k: v for k, v in data.items()} for data in data_list]
    keys = ', '.join(data_list[0].keys())
    values = ', '.join(['%s'] * len(data_list[0]))
    val_list = [tuple(data.values()) for data in data_list]
    sql = """INSERT INTO {table}({keys}) VALUES ({values})""".format(table=table, keys=keys, values=values)
    DB.insertmany(sql, val_list)



def run():
    # 读取的字段名
    old_name_list = ['law_code', 'law_name', "chapter_id","chapter_level1","chapter_level2", "chapter_level3",
                        "chapter_level4", "chapter_level5","chapter_level6","law_content", "law_summary",
                        "law_url", "source","load_time", "update_time"]

    old_Table = 'ods_law_regulations_HongKong'
    old_DB = DbTool('mysql', 'test_mysql_wbh')  # wbh测试环境


    old_data_list = read_data(old_Table,old_name_list,old_DB)       # [(x,xx,xxx,xx),(x,xx,xxx,xx),(x,xx,xxx,xx)]

    new_Table = 'ods_law_regulations'
    new_DB = DbTool('mysql', 'YWF_Spider')  # 域外法运行环境库

    for old_data in old_data_list:
        one_dict = {}
        for name_index in range(len(old_name_list)):
            this_data = old_data[name_index]
            if str(old_data[name_index]) == 'None':         # 空值处理
                this_data = ''
            one_dict[old_name_list[name_index]] = this_data
        print(one_dict)

        data_list = [one_dict]
        save_data(new_Table,data_list,new_DB)

if __name__ == '__main__':
    run()

