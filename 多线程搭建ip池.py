# -*- coding: gbk -*-    # 防止出现乱码等格式错误
# ip代理网站：http://www.66ip.cn/areaindex_19/1.html

import requests
from fake_useragent import UserAgent
import pandas as pd
from lxml import etree # xpath
import threading    # 多线程

# ---------先获取url列表----------
def get_url():
    url_list = []
    url = 'http://www.66ip.cn/index.html'
    data_html = requests.get(url)
    data_html.encoding = 'gbk'
    data_html = data_html.text
    html = etree.HTML(data_html)
    page = html.xpath('//*[@id="PageList"]/a[12]/text()')      # 获取全球代理的页码
    for i in range(int(page[0])):
        country_url = 'http://www.66ip.cn/{}.html'.format(i+1)
        url_list.append(country_url)
    for i in range(1,35):       # 因为那个网站只有35个城市
        city_url = 'http://www.66ip.cn/areaindex_{}/1.html'.format(i)
        url_list.append(city_url)
    return url_list

# ---------------爬取该网站城市ip----------------
def get_all_ip(url_list):
    headers = {
        'User-Agent': UserAgent().random,
    }
    test_ip = []    # 用于存放爬取下来的ip
    for url in url_list:
        try:        # 防止有时访问异常抛出错误
            data_html = requests.get(url=url, headers=headers)
            data_html.encoding = 'gbk'
            data_html = data_html.text
            html = etree.HTML(data_html)
            etree.tostring(html)
            response = html.xpath('//div[@align="center"]/table/tr/td/text()')      # 获取html含有ip信息的那一行数据
            test_ip += dispose_list_ip(response)       # 调用下面的处理函数，将不必要的数据筛掉
        except:
            continue
    print("本次获取ip信息的数量：",len(test_ip))
    return test_ip

# --------------将爬取的list_ip关键信息进行提取、方便后续保存----------------
def dispose_list_ip(list_ip):
    num = int((int(len(list_ip)) / 5) - 1)  # 5个一行，计算有几行，其中第一行是标题直接去掉
    test_list = []

    for i in range(num):
        a = i * 5
        ip_index = 5 + a  # 省去前面的标题，第5个就是ip，往后每加5就是相对应ip
        location_index = 6 + a
        place_index = 7 + a

        items = []
        items.append(list_ip[ip_index])
        items.append(list_ip[location_index])
        items.append((list_ip[place_index]))
        test_list.append(items)
    return test_list

# -----------将列表的处理结果保存在csv-------------
def save_list_ip(list,file_path):
    columns_name=["ip","port","place"]
    test=pd.DataFrame(columns=columns_name,data=list)         # 去掉索引值，否则会重复
    test.to_csv(file_path,mode='a',encoding='utf-8')
    print("保存成功")

# ------------读取文件，以df形式返回--------------
def read_ip(file_path):
    file = open(file_path,encoding='utf-8')
    df = pd.read_csv(file,usecols=[1,2,3])      # 只读取2,3,4,列（把第一列的索引去掉）
    df = pd.DataFrame(df)
    return df

# -----------读取爬取的ip并验证是否合格-----------
def verify_ip(ip_list):
    verify_ip = []

    for ip in ip_list:
        ip_port = str(ip[0]) + ":" + str(ip[1])  # 初步处理ip及端口号
        headers = {
            "User-Agent": UserAgent().random
        }
        proxies = {
            'http': 'http://' + ip_port,
            'https': 'https://'+ip_port
        }
        '''http://icanhazip.com访问成功就会返回当前的IP地址'''
        try:
            p = requests.get('http://icanhazip.com', headers=headers, proxies=proxies, timeout=3)
            item = []  # 将可用ip写入csv中方便读取
            item.append(ip[0])
            item.append(ip[1])
            item.append(ip[2])
            verify_ip.append(item)
            print(ip_port + "验证成功！")
        except Exception as e:
            print(ip_port,"验证失败")
            continue
    return verify_ip

# ----------------多线程重写----------------------
class MyThread(threading.Thread):
    def __init__(self,func,args):
        """
        :param func: run方法中的函数名
        :param args: func函数所需的参数
        """
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        print('当前子线程:{}启动'.format(threading.current_thread().name))
        self.result = self.func(self.args)
        return self.func
    def get_result(self):       # 获取返回值
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except:
            return None

# -----将待处理任务进行平均分割为线程数，方便线程执行----
def split_list(list,thread_num):
    list_total = []
    num = thread_num  # 线程数量
    x = len(list) // num  # 将参数进行分批（5批）方便传参
    count = 1  # 计算这是第几个列表
    for i in range(0, len(list), x):
        if count < num:
            list_total.append(list[i:i + x])
            count += 1
        else:
            list_total.append(list[i:])
            break
    return list_total

# -----------多线程访问网址获取ip信息---------------
def create_thread_get_ip_list(list,thread_num):
    list_total = split_list(list,thread_num)    # 调用上面的方法，将任务平均分配给线程
    thread_list =[]     # 线程池
    for url in list_total:      # 添加线程
        t = MyThread(func=get_all_ip,args=url)
        thread_list.append(t)
        # thread1 = MyThread(func=get_all_ip,args=list_total[0])
        # thread2 = MyThread(func=get_all_ip,args=list_total[1])
    for t in thread_list:       # 批量启动线程
        t.start()
    for t in thread_list:       # 主线程等待子线程
        t.join()
    ip=[]                       # 存放爬取的ip
    for t in thread_list:       # 将数据存入ip中
        ip += t.get_result()
    print("总共线程获取ip数量为：",len(ip))
    print(ip)
    return ip

# ------------创建线程验证ip----------------------
def create_thread_verify_ip(list,thread_num):
    list_total = split_list(list, thread_num)
    thread_list = []    # 存放线程池
    ip = []             # 存放验证成功的ip
    for list in list_total:
        t = MyThread(func=verify_ip,args=list)
        thread_list.append(t)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()
    for t in thread_list:
        ip += t.get_result()
    return ip

if __name__ == '__main__':
    # ----------# 获取待爬取的全部url---------
    url_list = get_url()
    print(url_list)
    # ----------# 创建多线程爬取--------------
    thread_num1 = 100     # 第一个线程数量
    test_ip = create_thread_get_ip_list(url_list,thread_num1)
    # ----------保存数据-------------------
    test_path = 'test.csv'
    save_list_ip(test_ip,test_path)

    # -----这里建议先运行上面，结束后再运行下面---------
    # ----------# 读取、初步处理数据--------------
    df = read_ip(test_path)
    print("去重前数据有：",len(df))
    df = df.drop_duplicates()       # 去除重复数据
    print("去重后数据有：",len(df))
    ip_list = df.values.tolist()    # df转列表（方便等会多线程的时候分配任务）
    print(ip_list)

    # ----------# 创建多线程验证ip--------------
    thread_num2 = 100  # 第二个线程的数量
    ip = create_thread_verify_ip(list=ip_list,thread_num=thread_num2)
    print("验证失败ip数量：",len(ip_list)-len(ip))
    print("可用ip数量：",len(ip))

    # 保存
    save_path = "verify_ip.csv"
    save_list_ip(ip,save_path)

'''
    # ----第二次验证（这里可以按自己需求写一个for循环来多验证几次，提高ip池的质量）----
    verify_path = 'verify_ip.csv'
    df = read_ip(verify_path)
    print("去重前数据有：",len(df))
    df = df.drop_duplicates()       # 去除重复数据
    print("去重后数据有：",len(df))
    ip_list = df.values.tolist()    # df转列表（方便等会多线程的时候分配任务）
    print(ip_list)

    # ----------# 创建多线程验证ip--------------
    thread_num3 = 20  # 第三个线程的数量
    ip = create_thread_verify_ip(list=ip_list,thread_num=thread_num3)
    print("验证失败ip数量：",len(ip_list)-len(ip))
    print("可用ip数量：",len(ip))

    # 保存
    save_path = "优质ip.csv"
    save_list_ip(ip,save_path)
'''
