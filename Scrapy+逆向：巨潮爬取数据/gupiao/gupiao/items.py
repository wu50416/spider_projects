# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class GupiaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Transaction_date = scrapy.Field()        # 交易日期
    Opening_price = scrapy.Field()           # 开盘价
    Number_of_transactions = scrapy.Field()  # 成交数量
    Closing_price = scrapy.Field()           # 收盘价
    minimum_price = scrapy.Field()           # 最低价
    Highest_price = scrapy.Field()           # 最高价
    Securities_code = scrapy.Field()         # 证券代码
    Securities_abbreviation = scrapy.Field() # 证券简称
    pass
'''
爬取数据示例
交易所: "SZE"
交易日期: "2022-04-13"
币种: "CNY"
开盘价: 15.89
成交数量: 89062806
成交金额: 1415496125.98
收盘价: 15.8
最低价: 15.72
最高价: 16.08
涨跌: -0.12
涨跌幅: -0.7538
证券代码: "000001-SZE"
证券简称: "平安银行"
'''
