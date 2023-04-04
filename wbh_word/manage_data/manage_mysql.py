import time

import pymysql
from pymysql.converters import escape_string
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

# DB = DbTool('mysql', 'YWF_Spider')        # 域外法运行环境库
DB = DbTool('mysql', 'test_mysql_wbh')

def save_data(table, data_list):
    """
    data_list ：  [{"开始时间": '123123123',"结束时间": '12412412'},{"开始时间": 'asdas',"结束时间": 'asdasd'}]
    """
    data_list = [{k: v for k, v in data.items()} for data in data_list]
    keys = ', '.join(data_list[0].keys())
    values = ', '.join(['%s'] * len(data_list[0]))
    val_list = [tuple(data.values()) for data in data_list]
    # value_list = [tuple([str(val).replace('%', '%%') for val in val_tup]) for val_tup in val_list]
    # print(val_list)
    sql = """INSERT INTO {table}({keys}) VALUES ({values})""".format(table=table, keys=keys, values=values)
    # print(sql)
    # sql = f"""INSERT INTO {table}({keys}) VALUES ({values})"""
    # cur.executemany(sql,val_list)
    # print(sql)
    DB.insertmany(sql, val_list)

def save_data2(table, data_list):
    """
    data_list ：  [{"开始时间": '123123123',"结束时间": '12412412'},{"开始时间": 'asdas',"结束时间": 'asdasd'}]
    """
    data_list = [{k: v for k, v in data.items()} for data in data_list]
    keys = ', '.join(data_list[0].keys())
    # values = ', '.join(['%s'] * len(data_list[0]))
    val_list = [tuple(data.values()) for data in data_list]
    print(val_list)
    valu = ''
    for val in val_list:
        valu += str(val) + ','
    value = valu[:-1]
    print(value)
    sql = """INSERT INTO {table}({keys}) VALUES ({value})""".format(table=table, keys=keys, value=value)
    sql = sql.replace('%', '%%')        # % -> %%
    print(sql)
    DB.run_sql(sql)




def read_data(table,data_list):
    '''
    data_list：需要访问的字段列表 [id，meetid]
    '''
    key_data = ''       # `abc`,`bdc`
    for data in data_list:
        d1 = f'`{data}`,'
        key_data += d1
    key_data = key_data[:-1]        # 此时末位多出一个逗号,剔除
    sql = '''SELECT {key_data} FROM ods_data.{table}'''.format(key_data=key_data,table=table)
    # sql = '''SELECT * FROM ods_data.{table}'''.format(table=table)
    rest = DB.selectall(sql)

    return rest

# 获取没有重复值的数据，并按某字段排序
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

    sql = '''SELECT {key_data} FROM ods_data.{table} group by {key_data} ORDER BY {order_key}'''.format(key_data=key_data,table=table,order_key=order_data)
    rest = DB.selectall(sql)
    return rest

# 按照条件查询
def read_where_data(table,select_list,where_data):
    '''
    按照条件查询
    select_list：需要访问的字段列表 [id，meetid]
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
    sql = '''SELECT {key_data} FROM ods_data.{table} WHERE {where_sql}'''.format(key_data=data_sql,table=table,where_sql=where_sql)
    # print(f'请求sql：{sql}')
    rest = DB.selectall(sql)
    return rest

def get_sql_columns(table):
    '''
        # 获取Mysql数据的索引
        本函数主要与get_sql_dict搭配使用，按照本函数字段查询全部数据  防止数据 键-值 出现混乱
    '''
    sql_getname = '''select COLUMN_NAME from information_schema.COLUMNS where table_name = "{table}"'''.format(table=table)
    rest_name = DB.selectall(sql_getname)  # [('auctionStatus',), ('auctionStatus_id',), ('cid',), ('city_id',), ('city_Name',)]
    name_list = [name[0] for name in rest_name]  # ['auctionStatus', 'auctionStatus_id', 'cid', 'city_id', 'city_Name']
    return name_list

def get_sql_dict(table,sql):
    '''
        将 * -> 按照顺序的字段名     用于导出数据时防止数据排序出错
        SELECT * FROM ods_data.wbh_JD_id_Update  ->>  SELECT `auctionStatus`,`auctionStatus_id`,`cid`,`city_id` FROM ods_data.wbh_JD_id_Update

        传入table,字段必须是 * ，获取dict格式数据
        input sql = SELECT * FROM ods_data.wbh_JD_id_Update LIMIT 5
        return : [{'auctionStatus': '已结束', 'auctionStatus_id': '2', 'cid': '395995'}, {'auctionStatus': 'abc ', 'auctionStatus_id': '123', 'cid': '321'}]

        sql_getname =   select COLUMN_NAME from information_schema.COLUMNS where table_name = 'wbh_JD_id_Update'
        name_str = `auctionStatus`,`auctionStatus_id`,`cid`,`city_id`,`city_Name`
        sql_getdata = SELECT `auctionStatus`,`auctionStatus_id`,`cid`,`city_id`,`city_Name` FROM ods_data.wbh_JD_id_Update LIMIT 5
    '''
    # 先获取字段名
    name_list = get_sql_columns(table)
    name_st = '`,`'.join(name_list)
    name_str = "`" + name_st + "`"          # `auctionStatus`,`auctionStatus_id`,`cid`,`city_id`,`city_Name`
    # sql_getdata = '''SELECT {name_str} FROM ods_data.wbh_JD_id_Update LIMIT 5'''.format(name_str=name_str)
    sql = sql.replace("*",name_str)         # 将 * 替换成 读取的字段
    rest_data = DB.selectall(sql)

    rest_dict = [dict(zip(name_list,rest_data_one)) for rest_data_one in rest_data]
    # print(rest_dict)
    return rest_dict



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
            where_sql += f'{key}="{where_[key]}" and '
    where_sql = where_sql[:-5]
    sql = '''UPDATE ods_data.{table} set {updata_sql} WHERE {where_sql}'''.format(table=table,updata_sql=updata_sql,where_sql=where_sql)
    # print(sql)
    sql = sql.replace('"None"','null')
    DB.run_sql(sql)
    print(f'Mysql 更新成功！{where_data} --> {updata_sql}')
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
    '''
    # 通过某条件读取数据
    where_table = 'wbh_ZGPM_SF_id'
    data_list = ['item_id']
    where_list = [{"item_id": 0}]
    read_where_data(where_table,data_list,where_list)
    '''
    sql = '''SELECT * FROM ods_data.wbh_JD_id_Update LIMIT 5'''
    get_sql_dict('wbh_JD_id_Update',sql)


