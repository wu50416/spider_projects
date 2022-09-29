import json
import re
import time

import requests
import execjs


def get_csrfID(timestamp, dynamicToken,headers, key_words=''):
    # key_words = "tuijian"
    if key_words == "zuanshi":
        url_keyword = 'https://zuanshi.taobao.com/loginUser/info.json'
        params = (
            ('r', 'mx_12'),
            ('callback', 'jQuery32104221044489235328_1638847248575'),
            ('timeStr', timestamp),
            ('dynamicToken', dynamicToken),
            ('csrfID', ''),
            ('bizCode', 'zszw'),
            ('_', '1638847248576'),
        )
        print("正在生成 超级钻展 参数")
    elif key_words == "tuijian":
        params = (
            ('r', 'mx_14'),
            ('callback', 'jQuery32103951861895131743_1638857985416'),
            ('bizCode', 'feedFlow'),
            ('invitationCode', ''),
            ('timeStr', '1638857985693'),
            ('dynamicToken', '428476472448452388472480'),
            ('csrfID', ''),
            ('_', ''),
        )
        url_keyword = 'https://tuijian.taobao.com/api/member/getInfo.json'
        print("正在生成 超级推荐 参数")
    else:
        raise Exception("平台关键词不正确")
    csrf_res = requests.get(url_keyword, headers=headers, params=params)
    if csrf_res.status_code == 200:
        json_data = re.findall(r'\((.*)\)', csrf_res.text)
        if json_data:
            json_data = json.loads(json_data[0])
            csrfID = json_data['data']['csrfID']
            pin = json_data['data']['pin']
            seedToken = json_data['data']['seedToken']
            return csrfID, pin, seedToken
        else:
            raise Exception("解析 csrfID为空,可能为cookie失效")
    else:
        raise Exception(f"get_csrfID status_code = {csrf_res.status_code}")


def get_params(cookie, key_words):
    headers = {
        'authority': 'zuanshi.taobao.com',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://zuanshi.taobao.com/index_poquan.jsp?spm=a2322.13920195.cf7687754.ddb5ad158.2477787ehM4Loa&file=index_poquan.jsp',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': cookie,
    }
    timestamp = int(time.time() * 1000)
    # timestamp = 1638857985693
    with open('dynamicToken.js', 'r') as f:
        js_text = f.read()
    ctx = execjs.compile(js_text)  # 获取代码编译完成后的对象
    dynamicToken = ctx.call("get_token", timestamp)
    csrfID, pin, seedToken = get_csrfID(timestamp, dynamicToken, headers, key_words)
    print('dynamicToken', dynamicToken)
    print(csrfID, pin, seedToken)
    timestamp = int(time.time() * 1000)
    # timestamp = 1638857988009
    # 204224224208200224228212 超级钻展受众人群
    # default_str = "224212192228220228204196"

    newdynamicToken = ctx.call("get_dynamicToken", seedToken,  pin, timestamp)
    print("newdynamicToken", newdynamicToken)
    return str(timestamp), newdynamicToken, csrfID


if __name__ == '__main__':
    # cookie = get_cookies_from_chrome()
    cookie = "t=f497dcd958d47e308a700d8182a6d337; thw=cn; enc=6Q6e9fRfEbcDpjkX7Q%2BV5CwfEbkqMINX6OhPtWtG5AEIFMmRKHgP37fF9cNS%2BHdafnCPvQI45gogsQlwUXp9LpDYLQ%2FJO8HgZ3hnAnThzls%3D; _samesite_flag_=true; cookie2=1be84713e288dd4235272f2bd65fbeca; _tb_token_=333e75f5bee5e; c_csrf=6f110411-8d11-48db-964b-f236829faded; xlly_s=1; sgcookie=E100hgArNqNiNXukY6%2FYjMlvzTrCIqjT%2FHJlViEn30du0LIXQu3h5aRUh8KGv2yzneL%2BKU3uiS%2BGmj3lIQV0LvrQqGg4wshSB3rpGKe2CkDBJMc%3D; unb=2212938575405; sn=%E4%BC%8A%E4%B8%BD%E8%8E%8E%E7%99%BD%E9%9B%85%E9%A1%BF%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97%3A%E6%99%A8%E6%9B%A6; csg=f38f9959; cancelledSubSites=empty; skt=8c23153bcb5cb38c; _cc_=VT5L2FSpdA%3D%3D; _m_h5_tk=d2ab3e0c5c90587729c62f307ebaca1a_1664439974919; _m_h5_tk_enc=e6e72f6018e6285e0ba0323171932a46; cna=Fka5GznetQ0CAbc2wK7E7Dim; uc1=cookie14=UoeyChYWPm5AJw%3D%3D&cookie21=U%2BGCWk%2F7oPIg; l=eBEAtNuHTa1eYC86BOfwourza77OSIRAguPzaNbMiOCPOICp5URdW6uS6e89C3GVh6JHR37vCcaaBeYBqImHDuRkbgiplEMmn; tfstk=cumdBy4IRCAh3RAubkLga_WUvl9GZXd819Nl20jh2ztwq5sRimomD3hXR8aWtdC..; isg=BEVFsRuGivGOFa4x5QmTas9QVIF_AvmUjt_bsUeqAXyL3mVQD1IJZNO46AIonhFM"
    print(get_params(cookie, key_words="tuijian"))