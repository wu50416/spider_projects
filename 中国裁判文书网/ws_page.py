# -*- coding: UTF-8 -*-
import json
import random
import time

import execjs
import requests
import uuid

def pageId():
    return str(uuid.uuid1()).replace('-', '')


def __RequestVerificationToken():
    a = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    num = ''
    for i in range(24):
        num += random.choice(a)
    return num

headers = {
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "sec-ch-ua-platform": "\"Windows\"",
    "Origin": "https://wenshu.court.gov.cn",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html?pageId=38457c49ef5e3f747a3bbc8fe7b5829a&s8=02",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

with open('wenshu.js', 'r', encoding='utf8') as f:
    js_data = f.read()


def login(user, password):
    password = execjs.compile(js_data).call("encodePassword", password)
    print("password:", password)
    data = {
        "username": user,
        "password": password,
        "appDomain": "wenshu.court.gov.cn"
    }
    response = session.post("https://account.court.gov.cn/api/login", data=data)
    print("登录请求:", response.text)
    r = session.post('https://wenshu.court.gov.cn/tongyiLogin/authorize', headers=headers)
    print(f'验证链接：{r.text}')
    session.get(r.text, headers=headers)


def get_data(case_type, pageNum):
    ciphertext = execjs.compile(js_data).call("cipher")
    print("输出", ciphertext)
    case_value = case_map[case_type]
    data = {
        "pageId": pageId(),
        "s8": case_value,
        "sortFields": "s50:desc",
        "ciphertext": ciphertext,
        "pageNum": pageNum,
        "pageSize": "10",
        "queryCondition": "[{\"key\":\"s8\",\"value\":\"%s\"}]" % case_value,
        "cfg": "com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@queryDoc",
        "wh": "1070",
        "ww": "1926",
        "cs": "0",
        '__RequestVerificationToken': __RequestVerificationToken(),
    }
    response = session.post("https://wenshu.court.gov.cn/website/parse/rest.q4w", headers=headers, data=data).json()
    print(response)
    res_secretKey = response['secretKey']
    res_result = response['result']
    decrypt_data = execjs.compile(js_data).call("DES3_decrypt", res_secretKey, res_result)

    decrypt_data = json.loads(decrypt_data)
    resultList = decrypt_data['queryResult']['resultList']
    for result_one in resultList:
        print("pageNum -----", pageNum, result_one)


if __name__ == "__main__":
    session = requests.session()
    session.headers = headers
    case_map = {
        "刑事案件": "02",
        # "民事案件": "03",
        # "行政案件": "04",
        # "赔偿案件": "05",
        # "执行案件": "10",
    }
    login("17108935363", "YO!1YH1AP3")
    for case_type in case_map:
        for pageNum in range(1, 15):
            time.sleep(2)
            get_data(case_type, pageNum)

