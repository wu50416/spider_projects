# -*- coding: UTF-8 -*-
'''
@Project ：yj_pj 
@File ：text.py
@Author ：hao
@Date ：2023/2/24 11:27 
'''
from selenium import webdriver

def demo_run():
    url1 = 'https://login.taobao.com/member/login.jhtml'
    # ---------# 下面这一大块东西都是用来隐藏selenium的特征值---------------------

    # chrome_options.add_argument("--proxy-server=http://114.230.23.140:3658")       # 新增ip代理
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension',False)
    driver = webdriver.Chrome(chrome_options=chrome_options)

    with open('123.js') as f:
        js = f.read()

    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                           {'source': js})

    # ---------# 隐藏特征值----------------------------
    driver.get(url1)

if __name__ == '__main__':
    demo_run()
