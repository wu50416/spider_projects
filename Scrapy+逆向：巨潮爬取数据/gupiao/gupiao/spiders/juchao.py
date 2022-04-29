import scrapy
from gupiao.items import GupiaoItem     # 获取存储的参数列表

class JuchaoSpider(scrapy.Spider):
    name = 'juchao'
    allowed_domains = ['cninfo.com.cn']
    start_urls = ['http://cninfo.com.cn/']

    def start_requests(self):
        data1 = {          # 通过创建的data1字典来构造Form Data表单数据
            'tdate': '2022-04-12',
            'market': 'SZE',
        }
        url = 'http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1007'
        # POST请求，所以使用scrapy.FormRequest()方法来发送网络请求
        # 发送完后通过回调函数callback来将响应内容返回给parse()方法
        yield scrapy.FormRequest(url=url,formdata=data1,callback=self.parse)

    def parse(self, response):
        p = response.json()
        if p != None:       # 防止取到空
            pda = p.get('records')      # 获取json文件下参数的对应位置
            for i in pda:
                item = GupiaoItem()
                item['Transaction_date'] = i.get('交易日期')
                item['Opening_price'] = i.get('开盘价')
                item['Number_of_transactions'] = i.get('成交数量')
                item['Closing_price'] = i.get('收盘价')
                item['minimum_price'] = i.get('最低价')
                item['Highest_price'] = i.get('最高价')
                item['Securities_code'] = i.get('证券代码')
                item['Securities_abbreviation'] = i.get('证券简称')
                yield item

