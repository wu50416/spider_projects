import time

import pymysql
from dbutils.pooled_db import PooledDB

# connect = pymysql.connect(host='192.168.2.140',
#                           port=3308,
#                           user='luowen',
#                           password='GLVAYHBWnIsUril2',
#                           db='wangdong_test',
#                           charset='utf8',
#                           maxconnections=30,
#                           autocommit=1  # 自动提交
#                           )


'''
    该文件即将删除   请勿调用！！！！！！

'''


pool = PooledDB(creator=pymysql, maxconnections=30, host='192.168.1.105',
                user="wbh", port=3306, password="wbh!#123456",
                db="ods_data", autocommit=1)


content = pool.connection()
cur = content.cursor()



def save_data(table, data_list):
    """
    data_list ：  [{"开始时间": '123123123',"结束时间": '12412412'}]
    """
    data_list = [{k: v for k, v in data.items()} for data in data_list]
    keys = ', '.join(data_list[0].keys())
    values = ', '.join(['%s'] * len(data_list[0]))
    val_list = [tuple(data.values()) for data in data_list]
    sql = """INSERT INTO {table}({keys}) VALUES ({values})""".format(table=table, keys=keys, values=values)
    cur.executemany(sql,val_list)

def read_data(table,data_list):
    '''
    data_list：需要访问的字段列表 [id，meetid]
    '''
    key_data = ''       # `abc`,`bdc`
    for data in data_list:
        d1 = f'`{data}`,'
        key_data += d1
    key_data = key_data[:-1]        # 此时末位多出一个逗号,剔除
    sql = '''SELECT {key_data} FROM wangdong_test.{table}'''.format(key_data=key_data,table=table)
    cur.execute(sql)
    rest = cur.fetchall()
    print(rest)
    cur.close()
    return rest


if __name__ == '__main__':
    table = 'wbh_test'
    # val_list = [{"abc": 'sdfsd',"bdc": 'qwerqw'}]
    '''
    # 保存
    val_list = []
    a = {"abc": '123',"bdc": '3453','efg':'sad'}
    b = {"abc": '34634',"bdc": '412341','efg':'wsdasd'}
    val_list.append(a)
    val_list.append(b)
    print(val_list)
    save_data(table, val_list)
    '''
    # 读取
    key_list = []
    a = ['abc','bdc']
    read_data(table, a)


