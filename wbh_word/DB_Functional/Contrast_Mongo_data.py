# -*- coding: UTF-8 -*-
'''
@Project ：yj_pj 
@File ：Contrast_Mongo_data.py
@Author ：hao
@Date ：2023/2/1 9:43
功能：
'''
from wbh_word.manage_data import manage_mongo

# 读取 table_one 数据去对比 table_two ，返回table_two中不存在的table_one值
Mongo_table_one = 'Ali_FP_Detail_YB_20230118'
Mongo_table_two = 'wbh_Ali_FP_Detail'
contrast_field_one = 'ItemID'
contrast_field_two = 'ItemID'           # 待对比的字段


def get_old_sql():
    # sql = '''SELECT * FROM {Mysql_old_table} LIMIT 5'''.format(Mysql_old_table=Mysql_old_table)
    all_old_data = manage_mongo.read_mongodb_data(Mongo_table_one)
    return all_old_data


def contrast_data(data_list):
    results = manage_mongo.contrast_mongo_data(Mongo_table_two,contrast_field_two,data_list)
    # print(results)
    return results


def run():
    data_list = get_old_sql()
    contrast_id_list = []       # 待对比的输入数据
    for data in data_list:
        contrast_id = data[f'{contrast_field_one}']
        contrast_id_list.append(contrast_id)
    print(contrast_id_list)    # contrast_id_list = ['688110777781', '688785670654', '689122403025']
    results = contrast_data(contrast_id_list)
    # print(results)
    exist_id_list = []       # 存在的id部分
    for data2 in results:
        exist_id = data2[f'{contrast_field_two}']
        exist_id_list.append(exist_id)

    print(f"{Mongo_table_two} 存在 {Mongo_table_one}---{contrast_field_one} 字段的数据有： {exist_id_list}")
    '''
    a = [1,2,3,4,5,6]   # 待对比的输入数据
    b = [5,6,7,8,9]     # 对比后输出的数据（存在则输出）
    c = [x for x in [y for y in b if y not in a]]
    c : [7, 8, 9]
    '''
    absent_list = [x for x in [y for y in exist_id_list if y not in contrast_id_list]]    # 不存在的列表
    print(f'不存在 {Mongo_table_one}---{contrast_field_one} 字段的数据有： {absent_list}')


if __name__ == '__main__':
    run()
    # a = [1,2,3,4,5,6]
    # b = [5,6,7,8,9]
    # c = [x for x in [y for y in b if y not in a]]
    # print(c)

