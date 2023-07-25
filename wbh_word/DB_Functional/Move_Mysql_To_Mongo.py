# -*- coding: UTF-8 -*-
'''
@Project ：法拍 
@File ：Move_Mysql_To_Mongo.py
@Author ：hao
@Date ：2023/1/17 11:16 
'''
import time

'''
将Mysql某些字段同步到Mongo中
Mysql -> Mongo
'''
from wbh_word.manage_data import manage_mysql
from wbh_word.manage_data import manage_mongo


Mysql_Table = 'wbh_GPW_id'
Mongo_Table = 'wbh_GPW_detail'

def read_Mysql_data():
    Mysql_read = ['url','status_Update']
    rest = manage_mysql.read_data(Mysql_Table,Mysql_read)
    return rest

def run():
    Mysql_data = read_Mysql_data()
    index = 1
    for data in Mysql_data:
        print(f"当前共执行： {index} 条数据")
        index += 1
        url = data[0]
        status_Update = data[1]
        Mongo_Updata_dict = {'status_Update':status_Update}         # 需要同步的字段
        Mongo_where_dict = {'url':url}

        manage_mongo.Update_mongodb_data(Mongo_Table,where_dict=Mongo_where_dict,updata_dict=Mongo_Updata_dict)

if __name__ == '__main__':
    run()



