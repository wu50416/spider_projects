# -*- coding: UTF-8 -*-
'''
@Project ：法拍 
@File ：demo.py
@Author ：hao
@Date ：2023/1/3 14:53 
'''

from wbh_word.manage_data import manage_mysql
from tqdm import tqdm
import csv
from minio import Minio
# from minio.error import ResponseError
import os

class Download():
    def __init__(self,Mysql_table_list,Local_path):
        self.Mysql_table_list = Mysql_table_list
        # self.Mysql_table = 'wbh_JD_id'
        # self.Csv_Name = f'{self.Mysql_table}.csv'
        self.path = Local_path

    def get_sql_dict(self,Mysql_table):
        sql = f'''Select * from {Mysql_table}'''
        sql_dict = manage_mysql.get_sql_dict(Mysql_table,sql)
        return sql_dict

    def run(self):
        index = 1
        for Mysql_table in self.Mysql_table_list:
            Csv_Name = f'{Mysql_table}.csv'
            print(f"========== 正在保存 {Csv_Name} ==========")
            sql_dict_list = self.get_sql_dict(Mysql_table)
            sql_columns = manage_mysql.get_sql_columns(Mysql_table)        # 获取第一行索引
            print(f'     进度：{index} / {len(self.Mysql_table_list)} 本数据的长度为： {len(sql_dict_list)}')
            print(f"     {Csv_Name} 的索引为： {sql_columns}    ")          # 第一行索引
            index += 1
            self.del_file(Csv_Name)     # 先清空当前目录下的数据
            pbar = tqdm(sql_dict_list)
            self.save_data(Csv_Name,sql_columns)     # 先保存表头
            for sql_dict in sql_dict_list:           # 保存值    {'down_time': '2022-12-26 11:12:29', 's_price': '23755608'}
                pbar.update(1)
                sql_dict_value = list(sql_dict.values())
                self.save_data(Csv_Name,sql_dict_value)       # ['2022-12-26 11:12:29', '23755608']

            # print(sql_dict_list)
            print(f"========== {Csv_Name}保存成功！！ ==========\n\n")



    def save_data(self,Csv_Name, item):
        '''
        保存文件
        item_list : [('23755608', '0', '1'), ('3169473.3', '0', '1'), ('19600000', '0', '0')]
        '''
        # for item in item_list:
        with open('{}/{}'.format(self.path,Csv_Name), 'a', encoding='utf_8_sig', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(item)

    def del_file(self,Csv_Name):
        try:
            os.remove('{}/{}'.format(self.path,Csv_Name))
            print(f"     删除 {Csv_Name} 成功！！ ********")
        except FileNotFoundError:
            print(f"     当前目录下无{Csv_Name} 开始存储数据")
            pass



if __name__ == '__main__':
    Mysql_table_list = ['wbh_GDFY_data', 'wbh_BJHL_id', 'wbh_GPW_id', 'wbh_ICBC_id', 'wbh_JD_id', 'wbh_JD_data',
                        'wbh_RMFYSS_id','wbh_ZGPM_SF_id']
    Local_path = r'D:\yj_pj\法拍\DB_Backups\Backups_MysqlData'
    Download_MySql = Download(Mysql_table_list,Local_path)
    Download_MySql.run()



    # sql_data = view.get_sql_data()
    # print(sql_data)

