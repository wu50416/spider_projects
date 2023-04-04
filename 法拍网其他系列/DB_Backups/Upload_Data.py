# -*- coding: UTF-8 -*-
'''
    @Project ：法拍
    @File ：Upload_Data.py
    @Author ：hao
    @Date ：2023/1/4 17:04
'''

from minio import Minio
from urllib3.exceptions import ResponseError




minioClient = Minio(
        "{0}:{1}".format("192.168.2.119", "32514"),
        secure=False,  # 默认True[https]
        access_key="AIwz9IbgZzyFqpDH",
        secret_key="YHc0mwpTxzQ9rmpuwGJ2v8vDAU541yWU",
    )

# 存储文件到桶对象中或者存储在桶下的某个文件夹下
def save_file(bucket, file_name, file_local_path):
    # 桶名称，minio的文件名，本地数据地址
    # save_file("picture", "f1/f2/p4.png", "C:\\Users\\xxx\\Desktop\\test\\test.png")
    minioClient.fput_object(bucket, file_name, file_local_path)

def Upload_Backups(Table_list,Minio_path,Local_path):       # 上传备份数据
    '''
    DB_table_list:  ['wbh_GDFY_data', 'wbh_BJHL_id', 'wbh_GPW_id', 'wbh_ICBC_id']
    Minio_path:  Backups_Mysql    Backups_Mysql/xxxx    Backups_Mongo     Backups_Mongo/xxxx
    Local_path: wbh_GDFY_data.csv
    '''
    index = 1
    for Table in Table_list:
        Backup_filename = f'{Minio_path}/{Table}.csv'
        print(f"当前进度： {index} / {len(Table_list)} : 正在上传 {Backup_filename.split('/')[-1]} 数据")      # {Mysql_table}.csv
        index += 1
        path = f'{Local_path}/{Table}.csv'     # 本地数据地址
        save_file('ealpha',Backup_filename,path)


if __name__ == "__main__":
    Mysql_table_list = ['wbh_GDFY_data', 'wbh_BJHL_id', 'wbh_GPW_id', 'wbh_ICBC_id', 'wbh_JD_id', 'wbh_JD_data',
                        'wbh_RMFYSS_id','wbh_ZGPM_SF_id']
    Local_path = 'D:\yj_pj\法拍\DB_Backups\Backups_MysqlData'
    Minio_path = 'Backups_Mysql'            # ealpha -> Backups_Mysql
    Upload_Backups(Mysql_table_list,Minio_path,Local_path)

