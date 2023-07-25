# -*- coding: UTF-8 -*-
'''
@Project ：yj_pj 
@File ：manage_clickhouse.py
@Author ：hao
@Date ：2023/4/21 15:27 
'''
from clickhouse_driver import Client

client = Client(host='192.168.1.103', port='9000',
                user="default", password="7I2bHFLv",
                database='oodliadb')

# database = default 用于测试
# database = oodliadb 应用表


def save_data(table, data_list):
    """
    data_list ：  [{"id": '123',"name": '123','age':'123'},{"id": '321',"name": '321','age':'321'}]
    sql : INSERT INTO test_table2(id, name, age) VALUES
    """
    data_list = [{k: v for k, v in data.items()} for data in data_list]
    keys = ', '.join(data_list[0].keys())
    sql = ("""INSERT INTO {table}({keys}) VALUES""".format(table=table, keys=keys))
    print(sql)
    client.execute(sql,data_list)

if __name__ == '__main__':
    pass
    # table = 'test_table2'
    # # save_data(client,'case',all_dict_list)
    # data_list = [{'id':'asdasdasdaddcxca09db3423d2ea18fd','name':'asdasdasd','age':14},
    #              {'id':'000106ce123123rsd9db3423d2ea18fd','name':'abcd','age':22312}]
    # save_data(table, data_list)

