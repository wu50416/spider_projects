import time

import requests
'''
    访问 url = 'http://192.168.1.100:3659/random/proxy?name=adsl&limit=1' 获取ip池中ip
    检测ip是否用并返回  proxies 形式
'''
def ip_proxies1():
    return None

def ip_proxies():
    print('---- 正在获取代理ip ----')
    while True:
        url = 'http://192.168.1.100:3659/random/proxy?name=16yun&limit=1'
        # url = 'http://192.168.1.100:3659/random/proxy?name=adsl&limit=1'
        req = requests.get(url)
        ipprot = req.text[1:-1]
        herder = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Upgrade-Insecure-Requests': '1'
        }
        # print(req.text)
        proxies = {"http": "http://" + '{}'.format(ipprot), "https": "http://" + '{}'.format(ipprot)}
        thisIP = ''.join(ipprot.split(':')[0:1])
        url = 'http://icanhazip.com/'
        time.sleep(2)
        try:
            request = requests.get(url, headers=herder, proxies=proxies, timeout=3, verify=False)       # verify=False 不验证网站ca证书（忽略安全警告）
            if request.status_code == 200:
                print('代理ip:{}有效'.format(thisIP))
                # time.sleep(0.5)
                return proxies
        except:
            print('不可用代理' + ipprot)


if __name__ == '__main__':
    print(ip_proxies())













