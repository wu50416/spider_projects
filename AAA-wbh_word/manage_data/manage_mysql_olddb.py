import time

import pymysql
from wbh_word.manage_database.db_connection_pool import DbTool

# connect = pymysql.connect(host='192.168.1.105',
#                           port=3306,
#                           user='wbh',
#                           password='wbh!#123456',
#                           db='ods_data',
#                           charset='utf8',
#                           autocommit=1  # 自动提交
#                           )
# cur = connect.cursor()

'''
    该文件停止更新！！！！ 请勿调用！！！！
'''

# DB = DbTool('mysql', 'test_mysql_wbh')
DB = DbTool('mysql', 'test_mysql')


def save_data(table, data_list):
    """
    data_list ：  [{"开始时间": '123123123',"结束时间": '12412412'}]
    """
    data_list = [{k: v for k, v in data.items()} for data in data_list]
    keys = ', '.join(data_list[0].keys())
    values = ', '.join(['%s'] * len(data_list[0]))
    val_list = [tuple(data.values()) for data in data_list]
    sql = """INSERT INTO {table}({keys}) VALUES ({values})""".format(table=table, keys=keys, values=values)

    # cur.executemany(sql,val_list)

    DB.insertmany(sql, val_list)




def read_data(table,data_list):
    '''
    data_list：需要访问的字段列表 [id，meetid]
    '''
    key_data = ''       # `abc`,`bdc`
    for data in data_list:
        d1 = f'`{data}`,'
        key_data += d1
    key_data = key_data[:-1]        # 此时末位多出一个逗号,剔除
    # sql = '''SELECT {key_data} FROM wangdong_test.{table}'''.format(key_data=key_data,table=table)
    sql = '''SELECT * FROM {table}'''.format( table=table)
    rest = DB.selectall(sql)

    return rest

def read_Norepeat_data(table,data_list,order_key):
    '''
    获取没有重复值的数据，并按某字段排序
    data_list：需要访问的字段列表 [id，meetid]
    order_key：分组后按照某字段排序关键字
    '''
    key_data = ''       # abc,bdc
    for data in data_list:
        d1 = f'{data},'
        key_data += d1
    key_data = key_data[:-1]        # 此时末位多出一个逗号,剔除
    order_data = ''       # abc,bdc
    for data in order_key:
        d1 = f'{data},'
        order_data += d1
    order_data = order_data[:-1]        # 此时末位多出一个逗号,剔除

    sql = '''SELECT {key_data} FROM {table} group by {key_data} ORDER BY {order_key}'''.format(key_data=key_data,table=table,order_key=order_data)
    rest = DB.selectall(sql)
    return rest

def read_where_data(table,select_list,where_data):
    '''
    获取没有重复值的数据，并按某字段排序
    data_list：需要访问的字段列表 [id，meetid]
    where_data：[{status:0,id:1160926}]  status = 0 and id = 1160926
    '''
    data_sql = ''
    for data in select_list:
        data_sql += f'{data},'
    data_sql = data_sql[:-1]
    where_sql = ''
    for where_ in where_data:
        for key in where_.keys():
            where_sql += f'`{key}`="{where_[key]}" and '
    where_sql = where_sql[:-5]
    sql = '''SELECT {key_data} FROM {table} WHERE {where_sql}'''.format(key_data=data_sql,table=table,where_sql=where_sql)
    print(sql)
    rest = DB.selectall(sql)
    return rest

def run_sql(sql):
    '''
        直接运行
    '''
    rest = DB.selectall(sql)
    return rest



def update_data(table,updata_list,where_data):
    """
    updata_list = [{"status": '1',"update_time": '1234'}]
    where_data = [{"id": '1139969',"meetId": '146830'}]
    UPDATE wangdong_test.wbh_ZGPMXH_id set status=0,update_time=1234 WHERE id = 1139969 and meetId = 146830
    """
    updata_sql = ''
    for update in updata_list:
        for key in update.keys():
            updata_sql += f'{key}="{update[key]}",'
    updata_sql = updata_sql[:-1]
    where_sql = ''
    for where_ in where_data:
        for key in where_.keys():
            where_sql += f'{key}={where_[key]} and '
    where_sql = where_sql[:-5]
    sql = '''UPDATE {table} set {updata_sql} WHERE {where_sql}'''.format(table=table,updata_sql=updata_sql,where_sql=where_sql)
    DB.run_sql(sql)
    print(f'更新成功！{where_data} --> {updata_sql}')
    # cur.close()

if __name__ == '__main__':
    table = 'wbh_ZGPMXH_id'
    '''
    # 保存
    # val_list = [{"abc": 'sdfsd',"bdc": 'qwerqw'}]
    val_list = []
    save_data(table, val_list)
    '''
    '''
    # 读取
    key_list = []
    a = ['id','meetId']
    read_data(table, a)
    '''
    '''
    # 更新
    update_table = 'wbh_ZGPMXH_id'
    updata_list = [{"status": '0'}]
    id = 1139969
    meetId = 146830
    where_data = [{"id": id, "meetId": meetId}]
    update_data(update_table, updata_list, where_data)
    '''
    # 通过某条件读取数据
    where_table = 'wbh_ZGPMXH_id'
    data_list = ['id','meetid']
    where_list = [{"status": 0}]
    read_where_data(where_table,data_list,where_list)