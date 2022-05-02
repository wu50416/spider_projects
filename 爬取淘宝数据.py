import requests
import pandas as pd
import random
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By


# -----------获取cookie信息(首次登录)------   ---------
def get_cookie_list():
    url1 = 'https://login.taobao.com/member/login.jhtml'
    # ---------# 下面这一大块东西都是用来隐藏selenium的特征值---------------------
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension',False)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                           {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
    # ---------# 隐藏特征值----------------------------
    time.sleep(2)
    driver.get(url1)

    # -------------------这个方法爬多了会出现验证码(建议这块代码注释掉然后手动)-------------
    driver.maximize_window()
    time.sleep(2.1)
    name = "17688688515"
    for i in name:      # 模拟人工输入
        driver.find_element(By.XPATH, '//*[@id="fm-login-id"]').send_keys(i)
        time.sleep(float(random.randint(1000,2000)/10000))     # 0.1~0.2秒的速度输入一个字符
    time.sleep(1.4)
    keyword = 'wu504168539'
    for i in keyword:
        driver.find_element(By.XPATH, '//*[@id="fm-login-password"]').send_keys(i)
        time.sleep(float(random.randint(1000,2000) / 10000))
    time.sleep(1.7)

    # 如果这里出现了验证码需要手动一下，试过了模拟加速度滑动还是过不去，这里暂时空着，学到了新技能再更新
    driver.find_element(By.XPATH, '//*[@id="login-form"]/div[4]/button').click()

    # -------通过检测有无进入界面,出现搜索框按钮来确认是否登录成功-------
    while True:
        try:    # 直到出现搜索框,否则一直等待
            driver.find_element(By.XPATH, '//*[@id="J_SearchForm"]/button')

            cookie_list = driver.get_cookies()
            return cookie_list
        except:
            continue


# -----当爬取到验证码的时候，携带旧的cookie访问通过验证后更新cookie------
def up_cookies_list(cookie_list):
    url1 = 'https://s.taobao.com/'  # 先进入淘宝的界面
    url2 = 'https://s.taobao.com/search?q=%E8%A3%A4%E5%AD%90'  # 旧的cookie搜索关键词后就会弹出验证码界面

    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument('--disable-blink-features=AutomationControlled')  # 重点代码：去掉了webdriver痕迹
    option.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(chrome_options=option)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                           {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
    driver.get(url1)  # 先进入登陆前界面后加载cookie再进入登陆后的界面
    time.sleep(2)
    for i in cookie_list:
        driver.add_cookie({"name": i["name"], "value": i["value"]})
    driver.get(url2)    # 一般这个时候会跳出验证
    driver.refresh()  # 刷新一下
    time.sleep(5)
    # ----------------进入验证阶段（手动）--------------
    while True:
        try:
            driver.find_element(By.XPATH, '//*[@id="J_SearchForm"]/button')
            cookie_list = driver.get_cookies()
            return cookie_list  # 获取到新的cookie_list用来继续爬取
        except:
            continue

def dispose_cookie_list(cookie_list):
    cookie = ""
    for cookies in cookie_list:
        name = cookies["name"]
        value = cookies["value"]
        cookies = "{}={};".format(name, value)
        cookie += cookies
    return cookie

# ------------# 获取随机的UA头-------------
def get_UA():
    ua = [
        'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
        'Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1',
        'Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)',  # 这个是ie浏览器
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
        # WebKit搜索引擎
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; ja-JP) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
        'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
    ]
    return random.choice(ua)

# -------# 从ip池获取随机的一个ip地址（没有ip池这步可以省略）----------
def get_proxies():
    file = pd.read_csv("优质ip999.csv")       # 如果ip代理不稳定的话建议注释掉这一块
    df = pd.DataFrame(file)
    i = random.randint(0, len(df)-1)
    ip_port = str(df["ip"][i]) + ":" + str(df["port"][i])
    proxies = {
        'http': 'http://'+ip_port,
        'https': 'https://'+ip_port
    }
    return proxies

# ---------# 获取当前页所有物品的html-------------
def get_all_goods_html(cookie,page,kw):
    headers = {
        'user-agent': get_UA(),
        'referer': 'https://www.taobao.com/',
        'cookie': str(cookie)
    }
    url = 'https://s.taobao.com/search?'
    index = str(int(page)*44)       # 爬取指定的页数
    params = {
        'q': kw,
        's': index
    }
    proxies = get_proxies()     # 从ip池获取随机的一个ip地址（没有ip池或ip代理不稳定的话这步可以省略，删掉proxies即可）
    response = requests.get(url=url,headers=headers,params=params,proxies=proxies)
    response.encoding = 'utf-8'
    all_goods_html = response.text
    return all_goods_html

# --------- 通过正则表达式匹配物品相应id-----------------
def get_goods_list(all_goods_html):
    rule = r'(?<="auctionNids":\[).*?(?=])'
    a = re.findall(rule, all_goods_html)
    goods_list = a[0].split('"')
    while True:
        if '' in goods_list:
            goods_list.remove('')
        elif ',' in goods_list:
            goods_list.remove(',')
        else:
            break
    return goods_list

# -----# 通过上面获取的物品id来合成一个详情页的url列表-------
def get_detail_url_list(all_goods_html):
    url_list = []
    goods_list = get_goods_list(all_goods_html)

    for i in goods_list:
        url = 'https://detail.tmall.com/item.htm?id='+i
        url_list.append(url)
    return url_list         # 到这里就可以获取到各个物品的详情url了，可以直接进入详情页中

# ---------# 获取当前页物品的名称、价格、销量、地址并转成dataframe格式----------
def get_df_data(all_goods_html):
    a = all_goods_html

    url_list = get_detail_url_list(all_goods_html)  # 商品url

    name_rule = r'(?<=raw_title":").*?(?=",)'       # 名称
    name = re.findall(name_rule, a)

    price_rule = r'(?<="view_price":").*?(?=",)'    # 价格
    price = re.findall(price_rule, a)

    sales_rule = r'(?<=view_sales":").*?(?=人付款)'  # 销量
    sales = re.findall(sales_rule, a)

    region_rule = r'(?<=item_loc":").*?(?=",)'      # 发货地址
    region = re.findall(region_rule, a)

    nick_rule = r'(?<="nick":").*?(?=",)'   # 店铺名称
    nick = re.findall(nick_rule, a)         # 只取前面的，后面有部分会是其他东西
    nick = nick[:len(name)]

    df_data = {
        "商品链接":url_list,
        "商品名称":name,
        "价格":price,
        "销量":sales,
        "地址":region,
        "店铺名称":nick
    }
    df = pd.DataFrame(df_data)
    return df

# ---------# 合并获取的df_data信息------
def get_all_df_data(new_df,old_df):
    # 把旧的合并到新的df中
    new_df = pd.concat([new_df,old_df])
    new_df = new_df.reset_index(drop=True)      # 重置一下索引（不然会混乱）
    return new_df

# ---------# 保存df入csv文件中---------
def save_df(df,name):
    test = pd.DataFrame(df)  # 去掉索引值，否则会重复
    test.to_csv('{}.csv'.format(name), mode='w', encoding='utf-8')
    print("保存成功")

# ----------# 进入详情页开始抓取数据----------
def get_detail_response(url_list):
    pass

if __name__== "__main__":
    kw = input("需要爬取的物品：")
    page = int(input("爬取的页数："))
    all_df_data = {}        # 定义一个空表用于
    all_df_data = pd.DataFrame(all_df_data)
    cookie_list = get_cookie_list()         # 首次登录
    cookie = dispose_cookie_list(cookie_list)       # 将cookie列表处理成可用的字符串形式
    print(cookie_list)
    print(cookie)
    time.sleep(1.3)
    for i in range(page):   # 开始爬取
        try:        # 这里检测是否能正常访问
            html = get_all_goods_html(cookie=cookie,page=i,kw=kw)
            try:
                df = get_df_data(html)      # 尝试能否获取需要的数据，不能则说明出现了验证码
                print(df)
                all_df_data = get_all_df_data(new_df=all_df_data,old_df=df)     # 合并数据表
                sleeptime = float(random.randint(4000,7000)/1000)      # 随机睡4~10秒
                time.sleep(sleeptime)
            except:     # 出现验证码
                print("出现验证码，爬取需要先更新cookie")
                cookie_list = up_cookies_list(cookie_list)       # 通过旧的cookie来通过验证码来更新cookie
                cookie = dispose_cookie_list(cookie_list)
                print(cookie)
                time.sleep(2.1)
                continue
        except Exception as e:
            print("不能正常访问淘宝")
            print(e)
            break

# 保存
    save_df(all_df_data,kw)
