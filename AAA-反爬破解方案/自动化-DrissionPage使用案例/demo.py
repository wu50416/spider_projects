#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/6 15:41
# @Author  : Harvey
# @File    : demo.py
'''
目前发现能过 五秒盾反爬，谷歌无感验证 ，比 selenium 更加强大
说明文档：https://drissionpage.cn/advance/ini
'''
from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions().set_paths()
value = '确认您是真人'

co.headless(True)  # 设置无头加载  无头模式是一种在浏览器没有界面的情况下运行的模式，它可以提高浏览器的性能和加载速度
co.incognito(True)  # 无痕隐身模式打开的话，不会记住你的网站账号密码的
co.set_argument('--no-sandbox')  # 禁用沙箱 禁用沙箱可以避免浏览器在加载页面时进行安全检查,从而提高加载速度 默认情况下，所有Chrome 用户都启用了隐私沙盒选项  https://zhuanlan.zhihu.com/p/475639754
co.set_argument("--disable-gpu")  # 禁用GPU加速可以避免浏览器在加载页面时使用过多的计算资源，从而提高加载速度
co.set_user_agent(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')  # 设置ua

browser = ChromiumPage(co)  # 创建对象

browser.set.window.max()
browser.get("https://cn.airbusan.com/content/common/customercenter/noticeList", retry=3, interval=2, timeout=15)   # 五秒盾
# browser.get("https://www.exporthub.com/semak-for-cosmetics/", retry=3, interval=2, timeout=15)  # 五秒盾
# browser.get("https://hunter.io/try/search/abc.com?locale=en", retry=3, interval=2, timeout=15)   # 谷歌无感验证
browser.wait(2)
for i in range(20):
    if browser.ele(f'x://input[@value="{value}"]', timeout=3):
        print(f"retry {i + 1} times, Verify you are human click now")
        browser.ele(f'x://input[@value="{value}"]').click()
        browser.wait(2)
    if not (browser.cookies(as_dict=True).get('cf_clearance') or browser.cookies(as_dict=True).get('js_errors_cache_3')):
        '''
        cf_clearance: 五秒盾
        js_errors_cache_3：谷歌无感验证3
        '''
        print(f"retry {i + 1} times, browser_cookie is {browser.cookies(as_dict=True)}")
        continue
    else:
        print(f"retry {i + 1} times, browser_cookie is {browser.cookies(as_dict=True)}")
        break
browser.wait(2)

browser.wait.ele_displayed('x://td[@class="subject"]/a', timeout=3)
for tr in browser.eles('x://div[@class="boardList mgt60"]//tr', timeout=3)[1:]:
    tds = [td.text for td in tr.eles("x://td", timeout=3)]
    detail_url = tr.ele('x://td[@class="subject"]/a').attr('href')
    print(f"list_page_company is {tds} , a_href is {detail_url}")

# 对整页截图并保存
browser.get_screenshot(path=r'./headless_True.png', full_page=True)

browser.quit()
