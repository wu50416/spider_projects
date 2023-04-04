# -*- coding: UTF-8 -*-
'''
@Project ：法拍 
@File ：Backups_Start.py
@Author ：hao
@Date ：2023/1/5 9:43 
'''
import sys
sys.path.append("..")
import Download_MySql_data
import Download_Mongo_data
import Upload_Data

def Backups_MYSQL_ALL():
    Mysql_table_list = ['wbh_GDFY_data', 'wbh_BJHL_id', 'wbh_BJHL_data', 'wbh_GPW_id', 'wbh_ICBC_id','wbh_ICBC_data', 'wbh_JD_id',
                        'wbh_JD_data','wbh_RMFYSS_id', 'wbh_ZGPM_SF_id']
    Mysql_Local_path = r'/home/wangdong/fp_spider/DB_Backups/Backups_MysqlData'
    Minio_path = 'Backups_Mysql'            # Minio的路径
    Download_MySql = Download_MySql_data.Download(Mysql_table_list, Mysql_Local_path)
    Download_MySql.run()          # 从Mysql下载数据
    Upload_Data.Upload_Backups(Mysql_table_list,Minio_path, Mysql_Local_path)  # 数据备份上传
    print("\n\n ================== 上传成功！！ ==================\n")

def Backups_Mongo_ALL():
    Mongo_table_list = ['wbh_BJHL_detail','wbh_GPW_detail','wbh_ICBC_detail','wbh_RMFYSS_detail','wbh_Ali_FP_Detail',
                        'wbh_ZGPM_SF_detail','wbh_JD_details_new']
    Mongo_Local_path = r'/home/wangdong/fp_spider/DB_Backups/Backups_MongoData'
    Minio_path = 'Backups_Mongo'  # Minio的路径
    Download_Mongo = Download_Mongo_data.Download(Mongo_table_list,Mongo_Local_path)
    Download_Mongo.run()          # 从Mongo下载数据
    Upload_Data.Upload_Backups(Mongo_table_list, Minio_path, Mongo_Local_path)  # 数据备份上传

if __name__ == '__main__':
    Backups_MYSQL_ALL()
    Backups_Mongo_ALL()
