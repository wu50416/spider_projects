# -*- coding: UTF-8 -*-
'''
@Project ：法拍 
@File ：Add_Field.py
@Author ：hao
@Date ：2023/1/9 15:20 
功能： 给Mongo全部数据新增字段，并赋值
'''
import re

from wbh_word.manage_data import manage_mongo

Mongo_table = "wbh_GPW_detail"
def read_data():
    Mongo_data_list = manage_mongo.read_mongodb_data(Mongo_table)
    return Mongo_data_list

def run():
    Mongo_data_list = read_data()
    index = 1
    for Mongo_dict in Mongo_data_list:
        print(f"当前共执行： {index} 条数据")
        index += 1

        '''
        样例模板：
        url = Mongo_dict['url']
        Mongo_where_dict = {'url': url}         # 查询匹配条件
        Mongo_update_dict = {'status_analysis':1}   # 新增字段
        '''

        # item_id = Mongo_dict['item_id']
        url = Mongo_dict['url']
        Mongo_where_dict = {'url': url}         # 查询条件
        Mongo_update_dict = {'status_analysis':1}   # 新增字段


        # url = Mongo_dict['url']
        # rule = 'Web_Item_ID=(.*)'
        # item_id = re.findall(rule, url)[0]
        # Mongo_update_dict = {'ItemID':item_id}
        # Mongo_where_dict = {'url': url}  # 查询匹配条件


        manage_mongo.Update_mongodb_data(Mongo_table,where_dict=Mongo_where_dict,updata_dict=Mongo_update_dict)
        # time.sleep(10)

if __name__ == '__main__':
    run()





