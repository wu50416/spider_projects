# -*- coding: UTF-8 -*-
'''
@Project ：法拍 
@File ：Mysql_data_move.py
@Author ：hao
@Date ：2022/12/15 17:02
功能说明： 两个 Mysql 数据合并,将旧表数据插入新表中
'''
import time
from tqdm import *
from wbh_word.manage_data import manage_mysql

# 两个 Mysql 数据合并,将旧表数据插入新表中
Mysql_old_table = 'wbh_JD_id_Update'
Mysql_new_table = 'wbh_JD_id'

def get_old_Sql():
    sql = '''SELECT * FROM {Mysql_old_table}'''.format(Mysql_old_table=Mysql_old_table)
    all_old_data = manage_mysql.get_sql_dict(Mysql_new_table,sql)
    return all_old_data

def get_save_update(item_id):
    # 判断是需要更新数据还是保存数据
    sql = '''SELECT * FROM {Mysql_new_table} WHERE item_id = {item_id}'''.format(Mysql_new_table=Mysql_new_table,item_id=item_id)
    rest = manage_mysql.run_sql(sql)
    if rest:
        choice_bool = 'update'
    else:
        choice_bool = 'save'
    # print(f"item_id : {item_id} -> {Sql_choice}")
    return choice_bool

def Move_sql_data():
    all_old_data = get_old_Sql()
    '''('395991', '天河区黄埔大道西尚雅街2号301房房产的三分之一产权份额', '290893276', '2022-09-28 10:00:00',
     '2022-11-28 09:33:23', '广州市', '1601', '诉讼资产', '1027', '住宅用房', '101', '已结束', '2', '无异常', '1',
     '变卖', '4', '广州市番禺区人民法院', '1726502', '966842', '天河区天河区黄埔大道西尚雅街2号301房',
     '2022-11-29 11:40:03', '2022-11-29 11:40:03', '0', '0')'''
    # print(all_old_data)
    num = len(all_old_data)
    pbar = tqdm(total=num)
    for old_dict in all_old_data:
        pbar.update(1)
        item_id = old_dict['item_id']
        Mysql_where_dict = [{"item_id": item_id}]

        Mysql_data = [old_dict]
        # print(old_dict)
        choice_bool = get_save_update(item_id)
        if choice_bool == 'save':
            manage_mysql.save_data(Mysql_new_table, Mysql_data)
        elif choice_bool == 'update':
            manage_mysql.update_data(Mysql_new_table, Mysql_data, where_data=Mysql_where_dict)

        # time.sleep(5)

if __name__ == '__main__':
    Move_sql_data()




