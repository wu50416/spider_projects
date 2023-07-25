# -*- coding: UTF-8 -*-
'''
@Project ：wbh_pj 
@File ：meituan_run.py
@Author ：hao
@Date ：2023/7/12 14:15 
'''
# 网站：https://gz.meituan.com/meishi/pn2/
import time
import execjs
import json
import requests
import random
import pandas as pd

# 第一页reqUrlAndParams
# "https://gz.meituan.com/meishi/api/poi/getPoiList?cityName=广州&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1&userId=754270772&uuid=3bcf687243ae42cf94f2.1660875247.1.0.0&platform=1&partner=126&originUrl=https://gz.meituan.com/meishi/&riskLevel=1&optimusCode=10"
# "https://gz.meituan.com/meishi/api/poi/getPoiList?cityName=广州&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=2&userId=754270772&uuid=3bcf687243ae42cf94f2.1660875247.1.0.0&platform=1&partner=126&originUrl=https://gz.meituan.com/meishi/pn2/&riskLevel=1&optimusCode=10"
# "https://gz.meituan.com/meishi/api/poi/getPoiList?cityName=广州&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=3&userId=754270772&uuid=3bcf687243ae42cf94f2.1660875247.1.0.0&platform=1&partner=126&originUrl=https://gz.meituan.com/meishi/pn3/&riskLevel=1&optimusCode=10"
# ****** 获取token ******
def get_token(url1):
    filename_js = 'token.js'
    with open(filename_js, encoding='utf-8', mode='r') as f:
        token_js = f.read()
        f.close()
    js1 = execjs.compile(token_js)

    # url1 = "https://gz.meituan.com/meishi/api/poi/getPoiList?cityName=广州&cateId=0&areaId=0&sort=price_asc&dinnerCountAttrId=&page=1&userId=754270772&uuid=3440f348ca534abea52c.1660792952.1.0.0&platform=1&partner=126&originUrl=https://gz.meituan.com/meishi/price_asc/&riskLevel=1&optimusCode=10"
    print('********* 正在生成 -- token *********')
    token = js1.call('token', url1)         # 获取token
    print(token)
    return token



def sleep_time(star,end):
    time.sleep(float(random.randint(star,end)/1000))

# ****** 获取请求头+参数 ******
def get_headers(Cookie,token,page):
    if page == 1:
        page1 = page
    else:
        page1 = page-1
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': Cookie,
        'Host': 'gz.meituan.com',
        'Referer': f'https://gz.meituan.com/meishi/pn{page1}/',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    }
    params = {
        'cityName': '广州',
        'cateId': '0',          # 分类
        'areaId': '0',          # 区域
        'sort': '',
        'dinnerCountAttrId': '',    # 用餐人数
        'page': page,
        'userId': '754270772',
        'uuid': '3bcf687243ae42cf94f2.1660875247.1.0.0',
        'platform': '1',
        'partner': ' 126',
        'originUrl': f'https://gz.meituan.com/meishi/pn{page}/',  # 类型+地点  11：广州
        'riskLevel': ' 1',
        'optimusCode': '10',
        '_token': token,
    }
    return headers,params



def get_data(Cookie):
    url = 'https://gz.meituan.com/meishi/api/poi/getPoiList'
    dt = {'店铺ID': [], '店铺名称': [], '评分': [], '店铺地址': [], '人均金额': []}
    for page in range(5):
        # 这个url用来获取token，不同的页面后面的参数必须要跟着更新
        url1 = f"https://gz.meituan.com/meishi/api/poi/getPoiList?cityName=广州&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page={page}&userId=754270772&uuid=3bcf687243ae42cf94f2.1660875247.1.0.0&platform=1&partner=126&originUrl=https://gz.meituan.com/meishi/pn{page}/&riskLevel=1&optimusCode=10"
        token = get_token(url1)
        headers,params = get_headers(Cookie,token,page=int(page+1))
        response = requests.get(url=url, headers=headers, params=params).json()
        print(response)
        # sleep_time(2500,5000)
        datas = response['data']['poiInfos']
        for data in datas:
            dt['店铺ID'].append(data['poiId'])
            dt['店铺名称'].append(data['title'])
            dt['评分'].append(data['avgScore'])
            dt['店铺地址'].append(data['address'])
            dt['人均金额'].append(data['avgPrice'])

    print(dt)
    dt = pd.DataFrame(dt)
    print(dt)
    dt.to_excel('美团数据.xlsx', encoding='gbk', index=False)




if __name__ == '__main__':
    Cookie = '_lxsdk_cuid=1867cfc8710c8-0ccc4798af58f2-26031951-1fa400-1867cfc8710c8; WEBDFPID=v6458z57295u5y1wy8446092y77552x08132xux1vwz97958833y625x-1992494171006-1677134170380MIYQEICfd79fef3d01d5e9aadc18ccd4d0c95072824; ci=30; cityname=%E6%B7%B1%E5%9C%B3; meishi_ci=30; cityid=30; IJSESSIONID=node09fofl71if6co1xz1atgasovtx38150619; iuuid=88884E59DA62E860363655FF3DB0972F98B618AAE01135F4541522E978CE4654; _hc.v=57a9ac31-2454-a561-5442-f409ca27e6e6.1685590507; _lxsdk=88884E59DA62E860363655FF3DB0972F98B618AAE01135F4541522E978CE4654; uuid=28725e29921749e7a78f.1685590514.1.0.0; webp=1; __utmc=74597006; ci3=30; userTicket=TFRipXdtZHZcaXGCJNwgKlSyAQeFGbVUTFsLWYIc; u=754270772; n=%E6%B5%A95452; lt=AgH5JVjijdYO4DXxQE0hyOXfoFij2igqFDX0QU6-QZ7ocfYswYhFpdj7yTbi--4Ty9jygKUuWBy12QAAAADFGAAAT-9qTDZyzQCziF3t3HbK_-hsLSlh1KeX803QnU4OkBjC2orbSDIAlaKSCh3gBaPN; mt_c_token=AgH5JVjijdYO4DXxQE0hyOXfoFij2igqFDX0QU6-QZ7ocfYswYhFpdj7yTbi--4Ty9jygKUuWBy12QAAAADFGAAAT-9qTDZyzQCziF3t3HbK_-hsLSlh1KeX803QnU4OkBjC2orbSDIAlaKSCh3gBaPN; token=AgH5JVjijdYO4DXxQE0hyOXfoFij2igqFDX0QU6-QZ7ocfYswYhFpdj7yTbi--4Ty9jygKUuWBy12QAAAADFGAAAT-9qTDZyzQCziF3t3HbK_-hsLSlh1KeX803QnU4OkBjC2orbSDIAlaKSCh3gBaPN; token2=AgH5JVjijdYO4DXxQE0hyOXfoFij2igqFDX0QU6-QZ7ocfYswYhFpdj7yTbi--4Ty9jygKUuWBy12QAAAADFGAAAT-9qTDZyzQCziF3t3HbK_-hsLSlh1KeX803QnU4OkBjC2orbSDIAlaKSCh3gBaPN; unc=%E6%B5%A95452; lat=22.611867; lng=114.108897; isid=AgH5JVjijdYO4DXxQE0hyOXfoFij2igqFDX0QU6-QZ7ocfYswYhFpdj7yTbi--4Ty9jygKUuWBy12QAAAADFGAAAT-9qTDZyzQCziF3t3HbK_-hsLSlh1KeX803QnU4OkBjC2orbSDIAlaKSCh3gBaPN; oops=AgH5JVjijdYO4DXxQE0hyOXfoFij2igqFDX0QU6-QZ7ocfYswYhFpdj7yTbi--4Ty9jygKUuWBy12QAAAADFGAAAT-9qTDZyzQCziF3t3HbK_-hsLSlh1KeX803QnU4OkBjC2orbSDIAlaKSCh3gBaPN; logintype=normal; __utma=74597006.1043013044.1685590547.1685590547.1688970758.2; __utmz=74597006.1688970758.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; p_token=AgH5JVjijdYO4DXxQE0hyOXfoFij2igqFDX0QU6-QZ7ocfYswYhFpdj7yTbi--4Ty9jygKUuWBy12QAAAADFGAAAT-9qTDZyzQCziF3t3HbK_-hsLSlh1KeX803QnU4OkBjC2orbSDIAlaKSCh3gBaPN; wm_order_channel=mtib; utm_source=60030; au_trace_key_net=default; openh5_uuid=88884E59DA62E860363655FF3DB0972F98B618AAE01135F4541522E978CE4654; isIframe=false; latlng=22.541406,114.019232,1688971342443; i_extend=C_b1Gimthomepagecategory11H__a; client-id=659f823f-4280-4e6f-a4df-9c2243e3d67b; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; firstTime=1689145870462; _lxsdk_s=18948f0dbc1-1c0-7a0-375%7C%7C1'

    get_data(Cookie)
