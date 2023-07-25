# -*- coding: UTF-8 -*-
'''
@Project ：wbh_pj 
@File ：get_token_zlip.py
@Author ：hao
@Date ：2023/7/12 14:18 
'''
import time
import zlib
import base64

import requests


def get_headers(Cookie):
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': '_lxsdk_cuid=1867cfc8710c8-0ccc4798af58f2-26031951-1fa400-1867cfc8710c8; WEBDFPID=v6458z57295u5y1wy8446092y77552x08132xux1vwz97958833y625x-1992494171006-1677134170380MIYQEICfd79fef3d01d5e9aadc18ccd4d0c95072824; ci=30; cityname=%E6%B7%B1%E5%9C%B3; meishi_ci=30; cityid=30; IJSESSIONID=node09fofl71if6co1xz1atgasovtx38150619; iuuid=88884E59DA62E860363655FF3DB0972F98B618AAE01135F4541522E978CE4654; _hc.v=57a9ac31-2454-a561-5442-f409ca27e6e6.1685590507; _lxsdk=88884E59DA62E860363655FF3DB0972F98B618AAE01135F4541522E978CE4654; uuid=28725e29921749e7a78f.1685590514.1.0.0; webp=1; __utmc=74597006; ci3=30; userTicket=TFRipXdtZHZcaXGCJNwgKlSyAQeFGbVUTFsLWYIc; u=754270772; n=%E6%B5%A95452; lt=AgH5JVjijdYO4DXxQE0hyOXfoFij2igqFDX0QU6-QZ7ocfYswYhFpdj7yTbi--4Ty9jygKUuWBy12QAAAADFGAAAT-9qTDZyzQCziF3t3HbK_-hsLSlh1KeX803QnU4OkBjC2orbSDIAlaKSCh3gBaPN; mt_c_token=AgH5JVjijdYO4DXxQE0hyOXfoFij2igqFDX0QU6-QZ7ocfYswYhFpdj7yTbi--4Ty9jygKUuWBy12QAAAADFGAAAT-9qTDZyzQCziF3t3HbK_-hsLSlh1KeX803QnU4OkBjC2orbSDIAlaKSCh3gBaPN; token=AgH5JVjijdYO4DXxQE0hyOXfoFij2igqFDX0QU6-QZ7ocfYswYhFpdj7yTbi--4Ty9jygKUuWBy12QAAAADFGAAAT-9qTDZyzQCziF3t3HbK_-hsLSlh1KeX803QnU4OkBjC2orbSDIAlaKSCh3gBaPN; token2=AgH5JVjijdYO4DXxQE0hyOXfoFij2igqFDX0QU6-QZ7ocfYswYhFpdj7yTbi--4Ty9jygKUuWBy12QAAAADFGAAAT-9qTDZyzQCziF3t3HbK_-hsLSlh1KeX803QnU4OkBjC2orbSDIAlaKSCh3gBaPN; unc=%E6%B5%A95452; lat=22.611867; lng=114.108897; isid=AgH5JVjijdYO4DXxQE0hyOXfoFij2igqFDX0QU6-QZ7ocfYswYhFpdj7yTbi--4Ty9jygKUuWBy12QAAAADFGAAAT-9qTDZyzQCziF3t3HbK_-hsLSlh1KeX803QnU4OkBjC2orbSDIAlaKSCh3gBaPN; oops=AgH5JVjijdYO4DXxQE0hyOXfoFij2igqFDX0QU6-QZ7ocfYswYhFpdj7yTbi--4Ty9jygKUuWBy12QAAAADFGAAAT-9qTDZyzQCziF3t3HbK_-hsLSlh1KeX803QnU4OkBjC2orbSDIAlaKSCh3gBaPN; logintype=normal; __utma=74597006.1043013044.1685590547.1685590547.1688970758.2; __utmz=74597006.1688970758.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; p_token=AgH5JVjijdYO4DXxQE0hyOXfoFij2igqFDX0QU6-QZ7ocfYswYhFpdj7yTbi--4Ty9jygKUuWBy12QAAAADFGAAAT-9qTDZyzQCziF3t3HbK_-hsLSlh1KeX803QnU4OkBjC2orbSDIAlaKSCh3gBaPN; wm_order_channel=mtib; utm_source=60030; au_trace_key_net=default; openh5_uuid=88884E59DA62E860363655FF3DB0972F98B618AAE01135F4541522E978CE4654; isIframe=false; latlng=22.541406,114.019232,1688971342443; i_extend=C_b1Gimthomepagecategory11H__a; client-id=659f823f-4280-4e6f-a4df-9c2243e3d67b; firstTime=1689147921602; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=18948f0dbc1-1c0-7a0-375%7C%7C17',
        'Pragma': 'no-cache',
        'Referer': 'https://gz.meituan.com/meishi/pn2/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'mtgsig': '{"a1":"1.1","a2":1689147930783,"a3":"v6458z57295u5y1wy8446092y77552x08132xux1vwz97958833y625x","a5":"D3qBLxO5Z7V9mLAzbL812zuTFqCIjpGW","a6":"h1.3Okq+j9CT3sA100ij0GqIh84zTM1zVFqKhl21lFWblklaKmE0Wt4SHfiVYIe/8QGbvPTfTE1sy5nBRQqdTWxei2+LYagWPh4fOENcE1orVcPHburDGib9H0U3poz6BuRwVdyQR8jqgmvR0lo3o3pxkerCRseTw/tTmY7bkO5S7lw7RMcvziVBL882D+yNIpgaDdmlFxX9pYq9CakXvTlg+FlBwLLDqIPTICtrI1CoGhv2p2iO8EJBU7kJ9kkD3SGMEhuVCDkTwZcoZxbr6/+VBHrYYeMcOMCO8HoL5BKU+9qJVcl9Xt/Bbl3DoZ7YHJpVpzeAwwWMcIij/ng88ML8JHvYnYGV1k9kSZbnWsgT4Hg=","x0":4,"d1":"07fe917c59fefad2d8a2da395e006bac"}',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    return headers

def get_params():
    get_token_params = {
        "cityName": "广州",
        "cateId": "0",
        "areaId": "0",
        "sort": "",
        "dinnerCountAttrId": "",
        "page": "1",
        "userId": "754270772",
        "uuid": "28725e29921749e7a78f.1685590514.1.0.0",
        "platform": "1",
        "partner": "126",
        "originUrl": "https://gz.meituan.com/meishi/pn1/",
        "riskLevel": "1",
        "optimusCode": "10"
    }
    return get_token_params

def zlip_data(zlip_params):            # 对数据压缩加密
    paraa = str(zlip_params).encode()  # 将 get_token_params 字典转换为字节数组
    compress = zlib.compress(paraa)  # 使用 zlib 压缩 paraa 变量的内容
    b_encode = base64.b64encode(compress)  # 使用 base64 进行压缩后的内容进行编码
    rest = str(b_encode, encoding='utf-8')
    return rest


def get_Ip_data(Ip_sign):
    Ip_dict =  {
        "rId": 100900,
        "ver": "1.0.6",
        "ts": 1689150994096,
        "cts": 1689154364296,
        "brVD": [
            1920,
            937
        ],
        "brR": [
            [
                1920,
                1080
            ],
            [
                1920,
                1040
            ],
            24,
            24
        ],
        "bI": [
            "https://gz.meituan.com/meishi/pn1/",
            "https://gz.meituan.com/meishi/pn2/"
        ],
        "mT": [],
        "kT": [],
        "aT": [],
        "tT": [],
        "aM": "",
        "sign": "eJwljUtKBDEURffSgwzzo9KpEjJoeiSIMxcQul5XP6x8eHkRdDFuQxy5mt6HEUf3cLmfQySIj2vQ4hIZ/gH5/TkmCPfvn/vXp1gxZ6Bz6ZlPzDQyolTG1Nu5rBCMFoVww/xCe7gx1/ag1PYhEyD3mOWlJDW43VDVbJSocRulIcRjNhh7FHWPfC2Uhk3YXp/gDfbBrRAH0Rv8fXo3Wa+9t6J3XIOdvXVgl8UaPy3go5+v0hxn5xbtzCSN1FIffgFuNEqT"
    }
    Ip_data = zlip_data(Ip_dict)
    return Ip_data


def run(cookie):
    headers = get_headers(cookie)
    token_params = get_params()
    aa = "areaId=0&cateId=0&cityName=广州&dinnerCountAttrId=&optimusCode=10&originUrl=https://gz.meituan.com/meishi/pn1/&page=1&partner=126&platform=1&riskLevel=1&sort=&userId=754270772&uuid=28725e29921749e7a78f.1685590514.1.0.0"

    Ip_sign = zlip_data(aa)               # 第一次加密
    print(Ip_sign)
    _token = get_Ip_data(Ip_sign)                                # 第二次加密
    print(_token)
    token_params['_token'] = _token
    params = token_params
    print(params)

    url = 'https://gz.meituan.com/meishi/api/poi/getPoiList'
    response = requests.get(url=url, headers=headers, params=params)
    print(response.text)


if __name__ == '__main__':
    cookie = '_lxsdk_cuid=1867cfc8710c8-0ccc4798af58f2-26031951-1fa400-1867cfc8710c8; WEBDFPID=v6458z57295u5y1wy8446092y77552x08132xux1vwz97958833y625x-1992494171006-1677134170380MIYQEICfd79fef3d01d5e9aadc18ccd4d0c95072824; ci=30; cityname=%E6%B7%B1%E5%9C%B3; meishi_ci=30; cityid=30; IJSESSIONID=node09fofl71if6co1xz1atgasovtx38150619; iuuid=88884E59DA62E860363655FF3DB0972F98B618AAE01135F4541522E978CE4654; _hc.v=57a9ac31-2454-a561-5442-f409ca27e6e6.1685590507; _lxsdk=88884E59DA62E860363655FF3DB0972F98B618AAE01135F4541522E978CE4654; uuid=28725e29921749e7a78f.1685590514.1.0.0; webp=1; __utmc=74597006; ci3=30; userTicket=TFRipXdtZHZcaXGCJNwgKlSyAQeFGbVUTFsLWYIc; u=754270772; n=%E6%B5%A95452; lt=AgH5JVjijdYO4DXxQE0hyOXfoFij2igqFDX0QU6-QZ7ocfYswYhFpdj7yTbi--4Ty9jygKUuWBy12QAAAADFGAAAT-9qTDZyzQCziF3t3HbK_-hsLSlh1KeX803QnU4OkBjC2orbSDIAlaKSCh3gBaPN; mt_c_token=AgH5JVjijdYO4DXxQE0hyOXfoFij2igqFDX0QU6-QZ7ocfYswYhFpdj7yTbi--4Ty9jygKUuWBy12QAAAADFGAAAT-9qTDZyzQCziF3t3HbK_-hsLSlh1KeX803QnU4OkBjC2orbSDIAlaKSCh3gBaPN; token=AgH5JVjijdYO4DXxQE0hyOXfoFij2igqFDX0QU6-QZ7ocfYswYhFpdj7yTbi--4Ty9jygKUuWBy12QAAAADFGAAAT-9qTDZyzQCziF3t3HbK_-hsLSlh1KeX803QnU4OkBjC2orbSDIAlaKSCh3gBaPN; token2=AgH5JVjijdYO4DXxQE0hyOXfoFij2igqFDX0QU6-QZ7ocfYswYhFpdj7yTbi--4Ty9jygKUuWBy12QAAAADFGAAAT-9qTDZyzQCziF3t3HbK_-hsLSlh1KeX803QnU4OkBjC2orbSDIAlaKSCh3gBaPN; unc=%E6%B5%A95452; lat=22.611867; lng=114.108897; isid=AgH5JVjijdYO4DXxQE0hyOXfoFij2igqFDX0QU6-QZ7ocfYswYhFpdj7yTbi--4Ty9jygKUuWBy12QAAAADFGAAAT-9qTDZyzQCziF3t3HbK_-hsLSlh1KeX803QnU4OkBjC2orbSDIAlaKSCh3gBaPN; oops=AgH5JVjijdYO4DXxQE0hyOXfoFij2igqFDX0QU6-QZ7ocfYswYhFpdj7yTbi--4Ty9jygKUuWBy12QAAAADFGAAAT-9qTDZyzQCziF3t3HbK_-hsLSlh1KeX803QnU4OkBjC2orbSDIAlaKSCh3gBaPN; logintype=normal; __utma=74597006.1043013044.1685590547.1685590547.1688970758.2; __utmz=74597006.1688970758.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; p_token=AgH5JVjijdYO4DXxQE0hyOXfoFij2igqFDX0QU6-QZ7ocfYswYhFpdj7yTbi--4Ty9jygKUuWBy12QAAAADFGAAAT-9qTDZyzQCziF3t3HbK_-hsLSlh1KeX803QnU4OkBjC2orbSDIAlaKSCh3gBaPN; wm_order_channel=mtib; utm_source=60030; au_trace_key_net=default; openh5_uuid=88884E59DA62E860363655FF3DB0972F98B618AAE01135F4541522E978CE4654; isIframe=false; latlng=22.541406,114.019232,1688971342443; i_extend=C_b1Gimthomepagecategory11H__a; client-id=659f823f-4280-4e6f-a4df-9c2243e3d67b; firstTime=1689147396242; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=18948f0dbc1-1c0-7a0-375%7C%7C13'
    run(cookie)

