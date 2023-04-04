# -*- coding: UTF-8 -*-
'''
@Project ：法拍 
@File ：Mysql_data_move.py
@Author ：hao
@Date ：2022/12/15 17:02
功能说明：两个 Mongo 数据合并,将旧表数据插入新表中
'''
import time
from tqdm import *
from wbh_word.manage_data import manage_mongo



# 两个Mongo 数据合并,将旧表数据插入新表中 Mongo_old_table -> Mongo_new_table
Mongo_old_table = 'Ali_FP_Detail_YB_20230118'
Mongo_new_table = 'wbh_Ali_FP_Detail'

def get_old_Sql():
    all_old_data = manage_mongo.read_mongodb_data(Mongo_old_table)
    return all_old_data

def get_save_update(item_id):
    # 判断是需要更新数据还是保存数据
    find_data = {"ItemID": item_id}        # 读取新表数据
    rest = manage_mongo.read_one_where_data(Mongo_new_table,find_data)

    for i in rest:      # 当有数据，会给choice复制
        choice_bool = 'update'
    try:                # 当无数据，此处报错  choice -> save
        abc = choice_bool+"123123abcaqweqweasdasd"
    except:
        choice_bool = 'save'
    print(f"ItemID : {item_id} -> {choice_bool}")


    return choice_bool

def Move_sql_data():
    all_old_data = get_old_Sql()
    '''
    {'_id': ObjectId('63858eda966945c407e72b70'), 'item_id': '291886944',
     'title': '【第1次拍卖】阳春市阳春大道与育德路交界处豪景宛（豪景苑）地块四9幢首层56号商铺（含二层）',
     'city_Name': '阳江市', 'searchLabel_Name': '破产资产', 'searchCategory_Name': '商业用房'}
    '''
    for old_dict in all_old_data:
        # print(old_dict)

        item_id = old_dict['ItemID']
        Mongo_where_dict = {"ItemID": item_id}
        choice_bool = get_save_update(item_id)

        if choice_bool == 'save':
            manage_mongo.save_mongodb_data(Mongo_new_table, old_dict)
        elif choice_bool == 'update':
            # manage_mongo.Update_mongodb_data(Mongo_new_table, Mongo_where_dict, updata_dict=old_dict)     # 更新数据，以新表
            continue



        # time.sleep(5)

if __name__ == '__main__':
    Move_sql_data()




