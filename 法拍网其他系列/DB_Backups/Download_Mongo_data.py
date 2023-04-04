# -*- coding: UTF-8 -*-
'''
@Project ：法拍 
@File ：Download_Mongo_data.py
@Author ：hao
@Date ：2023/1/5 10:44 
'''

from wbh_word.manage_data import manage_mongo
import csv
import os

class Download():
    def __init__(self,Table_list,Local_path):
        self.Table_list = Table_list
        # self.Mongo_table = 'wbh_JD_details_new_copy2'
        self.path = Local_path

    def run(self):
        table_index = 0
        Table_list_num = len(self.Table_list)
        for Mongo_table in self.Table_list:
            table_index += 1
            Csv_Name = f'{Mongo_table}.csv'
            print(f"========== 正在保存 {Csv_Name} ==========")
            data_dict_list = manage_mongo.read_mongodb_data(Mongo_table)
            self.del_file(Csv_Name)  # 先清空当前目录下的数据
            Mongo_columns = list(data_dict_list[0].keys())
            print('Mongo_columns:  ', Mongo_columns)
            self.save_data(Csv_Name, Mongo_columns)  # 先保存表头
            index = 1
            for data_dict in data_dict_list:
                Mongo_dict_value = list(data_dict.values())
                Mongo_value_list = []
                for Mongo_dict in Mongo_dict_value:
                    Mongo_dict1 = str(Mongo_dict).replace('\n','')
                    Mongo_dict1 = Mongo_dict1.replace('\r', '')
                    Mongo_dict1 = Mongo_dict1.replace('\s', '')
                    Mongo_dict1 = Mongo_dict1.replace('\r\n', '')
                    Mongo_value_list.append(Mongo_dict1)

                self.save_data(Csv_Name,Mongo_value_list)       # ['2022-12-26 11:12:29', '23755608']
                print(f"======== 进度：{table_index} / {Table_list_num} 正在保存 {Csv_Name} 第 {index} 条数据 ========")
                index += 1

    def save_data(self,Csv_Name, item):
        '''
        保存文件
        item_list : [('23755608', '0', '1'), ('3169473.3', '0', '1'), ('19600000', '0', '0')]
        '''
        # for item in item_list:
        with open('{}/{}'.format(self.path,Csv_Name), 'a', encoding='utf-8', newline='') as csvfile:
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
    Mongo_table_list = ['wbh_JD_details_new_copy2']
    Mongo_Local_path = r'D:\yj_pj\法拍\DB_Backups\Backups_MongoData'
    Download_Mongo = Download(Mongo_table_list,Mongo_Local_path)
    Download_Mongo.run()





