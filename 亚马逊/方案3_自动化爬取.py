# -*- coding: UTF-8 -*-
'''
@Project ：wbh_pj 
@File ：selenium_demo.py
@Author ：hao
@Date ：2023/10/23 16:49 
'''
'''
需要过验证码，暂时不写
'''
import time

from selenium import webdriver


def demo_run():
    url1 = 'https://www.amazon.com/dp/B0CS28ZLWS'
    # ---------# 下面这一大块东西都是用来隐藏selenium的特征值---------------------

    # chrome_options.add_argument("--proxy-server=http://114.230.23.140:3658")       # 新增ip代理
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)  # 核心为下面这几行
    with open('JS_2.js') as f:
        js = f.read()
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                           {'source': js})

    # ---------# 隐藏特征值----------------------------
    driver.get(url1)
    time.sleep(123)


if __name__ == '__main__':
    demo_run()
