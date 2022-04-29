# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class GupiaoPipeline:
    conn = None
    cursor = None
    def open_spider(self,spider):
        print('爬虫开始！！！')
        # 登录sql
        self.conn=pymysql.Connection(host='localhost',user='root',passwd='123456',db='juchao')

    def process_item(self,item,spider):
        print(list(item.values()))
        self.cursor=self.conn.cursor()
        # 写入数据库
        sql2 = "insert into gupiao(Transaction_date,Opening_price,Number_of_transactions,Closing_price,minimum_price,Highest_price,Securities_code,Securities_abbreviation) value(%s,%s,%s,%s,%s,%s,%s,%s);"
        # 这一块用来测试输出一下
        '''        
        for i in a:
            print(i)
        '''
        self.cursor.execute(sql2,list(item.values()))   # 执行sql语句，将item的值赋予sql中
        self.conn.commit()


    def close_spider(self,spider):
        print('爬虫结束！！！')
        self.cursor.close()