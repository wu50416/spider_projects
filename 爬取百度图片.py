import requests
import json

word = input("输入您需要爬取的关键字：")
page_num = int(input("需要爬取多少页（一页30张）："))
headers = {
    'Referer': 'https://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&dyTabStr=MCwzLDIsMSw2LDQsNSw4LDcsOQ%3D%3D&word=%E8%8B%B9%E6%9E%9C',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
}

url_list = []
for i in range(page_num):
    try:
        url1 = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&fr=&word={}&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&expermode=&nojc=&isAsync=&pn={}&rn=30&gsm=1e&1651226887256='.format(word,word,i*30)
        response = requests.get(url=url1,headers=headers).text
        js = json.loads(response)["data"]       # 转换为js格式，取“data”的值
        for j in js[0:30]:      # 只有0~29有图片数据，第30个数据为空值
            url_list.append(j["thumbURL"])
    except Exception as e:
        print("获取url失败")

count = 1   # 用来给照片命名，并查看当前照片是第几张
fail = 0    # 统计失败的数量
print("正在爬取......")
for url in url_list:
    file_name = 'E:/爬虫爬虫/爬虫项目/爬取百度图片/page/{}({}).jpg'.format(word, count)
    count += 1
    try:
        page = requests.get(url,headers).content    # 返回一个原生的字符串
        with open(file_name,'wb')as f:      # 二进制格式打开
            f.write(page)
    except Exception as e:
        print("第{}张图片下载失败".format(count))
        fail += 1
        print(e)

print("预计爬取数量:",len(url_list))
print("实际爬取数量:",len(url_list)-fail)


