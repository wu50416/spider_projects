
# -*- coding: utf-8 -*-
'''=================================================
@Project -> File   ：爬虫项目 -> demo
@IDE    ：PyCharm
@Author ：Mr. Hao
@Date   ：2022/10/10 11:31
=================================================='''
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import pandas as pd

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
    driver.find_element(By.XPATH,'//*[@id="fm-login-id"]').click()
    for i in name:      # 模拟人工输入
        time.sleep(float(random.randint(1000,2000)/10000))     # 0.1~0.2秒的速度输入一个字符
        driver.find_element(By.XPATH, '//*[@id="fm-login-id"]').send_keys(i)
    time.sleep(1.4)
    driver.find_element(By.XPATH,'//*[@id="fm-login-password"]').click()
    keyword = 'wu504168539'
    for i in keyword:
        time.sleep(float(random.randint(1000,2000) / 10000))
        driver.find_element(By.XPATH, '//*[@id="fm-login-password"]').send_keys(i)
    time.sleep(1.7)

    # 如果这里出现了验证码需要手动一下，试过了模拟加速度滑动还是过不去，这里暂时空着，学到了新技能再更新
    driver.find_element(By.XPATH, '//*[@id="login-form"]/div[4]/button').click()

    # -------通过检测有无进入界面,出现搜索框按钮来确认是否登录成功-------
    while True:
        try:    # 直到出现搜索框,否则一直等待
            driver.find_element(By.XPATH, '//*[@id="J_TSearchForm"]/div[1]/button')

            cookie_list = driver.get_cookies()
            print('登录成功！！cookie_list:',cookie_list)
            break

            # return cookie_list
        except:
            continue


    input_filename = 'data/力诚食品旗舰店.xlsx'
    data = pd.read_excel(input_filename)
    print(list(data['商品id']))
    df = {'商品名称': [], '商品id': [], '价格': [], '类目id': [], '类目': [], '总销量': [], '月销量': []}
    for index in range(len(data)):
        id = data["商品id"][index]
        url2 = f'https://detail.tmall.com/item_o.htm?id={id}'

        driver.get(url2)  # 一般这个时候会跳出验证
        time.sleep(float(random.randint(5000,7000)/1000))
        # html = driver.page_source
        # print(html)
        try:        # 第一次找不到数据（可能下架可能验证码）
            sellCount = driver.find_element(By.XPATH, '//*[@id="J_DetailMeta"]/div[1]/div[1]/div/ul/li[1]/div/span[2]').text
        except Exception as e:
            # 输入1验证码更新cookie，输入2为无数据
            try:
                xiajia = driver.find_element(By.XPATH, '//*[@id="J_Sold-out-recommend"]/div[1]/div[1]/strong').text
                sellCount = xiajia
            except:     # 此时需要人工判断是否遇到验证码
                a = int(input('遇到验证码！输入 1 刷新cookie，输入2为商品下架了， 输入三为后面手动写入！：'))
                if a == 1:      # 刷新cookie
                    try:
                        sellCount = driver.find_element(By.XPATH,'//*[@id="J_DetailMeta"]/div[1]/div[1]/div/ul/li[1]/div/span[2]').text
                    except Exception as e:
                        sellCount = '请手动填入！'
                        # cookie_list = driver.get_cookies()
                        # driver = up_cookies_list(cookie_list)
                        # driver.get(url2)  # 一般这个时候会跳出验证
                        # time.sleep(float(random.randint(5000,7000)/1000))
                        # sellCount = driver.find_element(By.XPATH,'//*[@id="J_DetailMeta"]/div[1]/div[1]/div/ul/li[1]/div/span[2]').text
                elif a == 2:
                    sellCount = '商品下架了！'
                elif a == 3:
                    sellCount = '请手动填入！'



        df['商品名称'].append(data['商品名称'][index])
        df['商品id'].append(data['商品id'][index])
        df['价格'].append(data['价格'][index])
        df['类目id'].append(data['类目id'][index])
        df['类目'].append(data['类目'][index])
        df['总销量'].append(data['总销量'][index])
        df['月销量'].append(sellCount)
        print('正在获取商品：', data['商品名称'][index], '  id为：', data['商品id'][index], '  月销量为：', sellCount)

    df = pd.DataFrame(df)
    print(df)
    df.to_excel('data/力诚食品旗舰店详情商品数据3.xlsx',index=False)






if __name__ == '__main__':
    # cookie_list = get_cookie_list()
    cookie_list = [{'domain': '.taobao.com', 'expiry': 1680941346, 'httpOnly': False, 'name': 'isg', 'path': '/', 'secure': False, 'value': 'BLW1bT01Ojdwsl6LdJPkbULAxDFvMmlEaE8Q6jfacSx7DtUA_4J5FMOMXNI4ToH8'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': 'uc1', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'cookie14=UoeyC73suDKonQ%3D%3D&cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&existShop=false&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&pas=0&cookie21=VFC%2FuZ9ainBZ'}, {'domain': '.taobao.com', 'expiry': 1665994147, 'httpOnly': False, 'name': '_m_h5_tk_enc', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '761cdeb46d9fe644e2ed6b055789ffcc'}, {'domain': '.taobao.com', 'expiry': 1665994147, 'httpOnly': False, 'name': '_m_h5_tk', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '6064f8e3f1d98a52b12e185d4d388f8c_1665399066617'}, {'domain': '.taobao.com', 'expiry': 1680941344, 'httpOnly': False, 'name': 'tfstk', 'path': '/', 'secure': False, 'value': 'cFuCBAvrf9XC0k8l-JOwLEUdkVzRZm9_sHwKOdzRw6hA_7hCiM_4hd4ZqO4zw51..'}, {'domain': '.taobao.com', 'expiry': 1680941344, 'httpOnly': False, 'name': 'l', 'path': '/', 'secure': False, 'value': 'eBxDi5-nTY0WjPHGBOfwourza77OSIRAguPzaNbMiOCPO01B52wXX6PcHMY6C3GVh6SJR3oPty5WBeYBqQd-nxvtOFj_flMmn'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': 'dnk', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'tb338752132'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': 'cancelledSubSites', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'empty'}, {'domain': '.taobao.com', 'httpOnly': True, 'name': 'cookie1', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'B0P4WciUN9P%2BJIXL2RWIuuRmn07Q6XjtEorkkVwGNbg%3D'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': '_l_g_', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'Ug%3D%3D'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': '_nk_', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'tb338752132'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': 'existShop', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'MTY2NTM4OTM0Mg%3D%3D'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': 'csg', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'af852275'}, {'domain': '.taobao.com', 'expiry': 1668010143, 'httpOnly': True, 'name': 'uc3', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'nk2=F5RGNeaApMxV91o%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D&vt3=F8dCv4SvuHzpUwqEHJY%3D&id2=UUphyuwNSQd1rraZSA%3D%3D'}, {'domain': '.taobao.com', 'httpOnly': True, 'name': 'unb', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '2200547271334'}, {'domain': '.taobao.com', 'expiry': 1666022947, 'httpOnly': False, 'name': 'mt', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'ci=38_1'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': 'sg', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '24a'}, {'domain': '.taobao.com', 'expiry': 1668010143, 'httpOnly': False, 'name': 'lgc', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'tb338752132'}, {'domain': '.taobao.com', 'httpOnly': True, 'name': 'skt', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '14dcf98f79e588a4'}, {'domain': '.taobao.com', 'expiry': 1668010143, 'httpOnly': True, 'name': 'uc4', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'nk4=0%40FY4NAAWHs%2BkgB4ryKQXL2OfLr19F3Q%3D%3D&id4=0%40U2grEaqARH0SyxX4vUQrLxcAdPr1bEAQ'}, {'domain': '.taobao.com', 'httpOnly': True, 'name': 'cookie2', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1c3f9a83424d8be2d2df8611411b84f7'}, {'domain': '.taobao.com', 'expiry': 1696954143, 'httpOnly': True, 'name': 'sgcookie', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'E100XU%2BoeOKupLLVy4NNRs%2BtXbRvkUxGVLEyvtSQQk8nov5O87XECGY%2FU8NvZcnjOIZE70c4LAvO0xeuwRVnhuv5LM7FrmTzgW%2Fu5q7DN0jG7lv%2Fj1GcQ%2BwQ5NUXWrmizkA8'}, {'domain': '.taobao.com', 'expiry': 1696954143, 'httpOnly': False, 'name': '_cc_', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'VFC%2FuZ9ajQ%3D%3D'}, {'domain': '.taobao.com', 'httpOnly': True, 'name': 'cookie17', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'UUphyuwNSQd1rraZSA%3D%3D'}, {'domain': '.taobao.com', 'expiry': 1665475725, 'httpOnly': False, 'name': 'xlly_s', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1'}, {'domain': '.taobao.com', 'expiry': 1696954143, 'httpOnly': False, 'name': 'tracknick', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'tb338752132'}, {'domain': '.taobao.com', 'expiry': 1696925347, 'httpOnly': False, 'name': 'thw', 'path': '/', 'secure': False, 'value': 'cn'}, {'domain': '.taobao.com', 'expiry': 2296109324, 'httpOnly': False, 'name': 'cna', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'C8HKGxJHQUsCAXFBoFiB7EGG'}, {'domain': '.taobao.com', 'expiry': 1673194143, 'httpOnly': False, 'name': 't', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'cd2136cd26b3bf4d9627e50e9946a2fa'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': '_tb_token_', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'e8457d17e1b7'}, {'domain': '.taobao.com', 'httpOnly': True, 'name': '_samesite_flag_', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'true'}]

    # get_data(cookie_list,'12123')
    get_cookie_list()




