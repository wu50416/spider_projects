# -*- coding: utf-8 -*-
"""
 A simple connection pool for relational databases using dbutils.pooled_db
"""
import json
import time

from dbutils.pooled_db import PooledDB
import logging
import wbh_word.manage_database.setting as setting


class DbTool(object):
    # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    mincached = 1
    # 链接池中最多闲置的链接，0表示不限制
    maxcached = 20
    # 连接池允许的最大连接数，0表示不限制连接数
    maxconnections = 200
    # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    blocking = True

    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(DbTool, cls).__new__(cls)
        return cls.instance

    def __init__(self, dbtype, loc ):
        if dbtype == 'postgresql':
            import psycopg2
            self.__pool = PooledDB(creator=psycopg2,
                                   mincached=self.mincached,
                                   maxcached=self.maxcached,
                                   maxconnections=self.maxconnections,
                                   blocking=self.blocking,
                                   host=setting.db_settings[loc]['host'],
                                   port=setting.db_settings[loc]['port'],
                                   user=setting.db_settings[loc]['user'],
                                   password=str(setting.db_settings[loc]['password']),
                                   database=setting.db_settings[loc]['database']
                                   )
            logging.info('SUCCESS: create postgresql success.\n')
        elif dbtype == 'mysql':
            import pymysql
            self.__pool = PooledDB(creator=pymysql,
                                   mincached=self.mincached,
                                   maxcached=self.maxcached,
                                   maxconnections=self.maxconnections,
                                   blocking=self.blocking,
                                   autocommit=1,
                                   # charset='UTF8',
                                   charset='utf8mb4',
                                   host=setting.db_settings[loc]['host'],
                                   port=setting.db_settings[loc]['port'],
                                   user=setting.db_settings[loc]['user'],
                                   password=str(setting.db_settings[loc]['password']),
                                   database=setting.db_settings[loc]['database']
                                   )
            logging.info('SUCCESS: create mysql success.\n')

    @staticmethod
    def __dict_datetime_obj_to_str(result_dict):
        """把字典里面的datatime对象转成字符串，使json转换不出错"""
        if result_dict:
            result_dict = {_: v.__str__() for _,v in enumerate(result_dict)}.values()
            return tuple(result_dict) 
    
    def get_conn(self):
        conn = self.__pool.connection()
        cursor = conn.cursor()
        return cursor, conn             

    def selectall(self, sql, param=()):
        cursor, conn = None, None
        try:
            cursor, conn = self.execute(sql, param)
            result = cursor.fetchall()
            return [self.__dict_datetime_obj_to_str(row_dict) for row_dict in result]
        except Exception as e:
            logging.exception("failed to select many %s, params %s", sql, param, exc_info=e)            
        finally:
            self.close(cursor, conn)

    def run_sql(self, sql, param=()):
        cursor, conn = None, None
        try:
            cursor, conn = self.execute(sql, param)
        except Exception as e:
            logging.exception("failed to select one %s, params %s", sql, param, exc_info=e)
        finally:
            self.close(cursor, conn)

    def selectone(self, sql, param=()):
        cursor, conn = None, None
        try:
            cursor, conn = self.execute(sql, param)
            result = self.__dict_datetime_obj_to_str(cursor.fetchone())
            return result
        except Exception as e:
            logging.exception("failed to select one %s, params %s", sql, param, exc_info=e)    
        finally:
            self.close(cursor, conn)

    def insert(self, sql, param=()):
        cursor, conn = None, None
        try:
            cursor, conn = self.execute(sql=sql, param=param)
            _id = cursor.lastrowid
            conn.commit()
            return _id
        except Exception as e:
            logging.exception("failed to insert %s, params %s", sql, param, exc_info=e)
            conn.rollback()
            raise e
        finally:
            self.close(cursor, conn)

    def update(self, sql, param=()):
        cursor, conn = None, None
        try:
            cursor, conn = cursor.execute(sql, param)
            rowcount = cursor.rowcount
            conn.commit()
            return rowcount
        except Exception as e:
            logging.exception("failed to update %s, params %s", sql, param, exc_info=e)
            conn.rollback()
            raise e
        finally:
            self.close(cursor, conn)

    def insertmany(self, sql, param=()):
        cursor, conn = self.get_conn()
        try:
            cursor.executemany(sql, param)
            rowcount = cursor.rowcount
            conn.commit()
            return rowcount
        except Exception as e:
            logging.exception("failed to insert many %s, params %s", sql, param, exc_info=e)
            conn.rollback()
            raise e
        finally:
            self.close(cursor, conn)

    def delete(self, sql, param=()):
        cursor, conn = None, None
        try:
            cursor, conn = self.execute(sql=sql, param=param)
            return True
        except Exception as e:
            logging.exception("failed to delete %s, params %s", sql, param, exc_info=e)
            conn.rollback()
        finally:
            self.close(cursor, conn)

    def execute(self, sql='', param=(), auto_close=False):
        cursor, conn = self.get_conn()
        try:
            cursor.execute(sql, param)
            rowcount = cursor.rowcount
            conn.commit()
            if auto_close:
                self.close(cursor, conn)
        except Exception as e:
            logging.exception("failed to execute %s, params %s", sql, param, exc_info=e)
            conn.rollback()          
            raise e
        self.close(cursor, conn)
        return cursor, conn
    
    def execute_many(self, sql_list=None):
        if sql_list is None:
            sql_list = []
        cursor, conn = self.get_conn()
        try:
            for order in sql_list:
                sql = order['sql']
                param = order['param']
                if param:
                    cursor.execute(sql, param)
                else:
                    cursor.execute(sql)
            conn.commit()
            self.close(cursor, conn)
            return True
        except Exception as e:
            logging.exception("failed to execute %s", sql_list, exc_info=e)
            conn.rollback()
            self.close(cursor, conn)
            return False 
    

    def new_transaction_conn(self):
        connection = self.__pool.connection()
        connection.begin()
        return connection


    def close(self, cursor, conn):
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()  


if __name__ == '__main__':
    print(DbTool('mysql','test_mysql_wbh').selectone('select * from wbh_ZGPMXH_id WHERE id = 1139969 and meetId = 146830'))
    # abcd = DbTool('mysql','test_mysql')
    # abcd.run_sql('UPDATE wangdong_test.wbh_ZGPMXH_id set status=1 WHERE id = 1139969 and meetId = 146830')




#     start = time.time()
#     print(DbTool('postgresql', 'test_postgresql').selectone("select * from company where company_name='佛山市南海鸿泰兴饮食服务有限公司'"))
#     print(json.dumps(DbTool('postgresql', 'test_postgresql').selectall("select * from company limit 30"),ensure_ascii=True))
#     print(time.time() -start)
