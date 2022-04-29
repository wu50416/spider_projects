# http://webapi.cninfo.com.cn/#/marketDataDate
import requests
import execjs
import js2py
def get_mcode():
    with open('123.js','r',encoding='utf-8')as f:
        read_js=f.read()
    return_js=execjs.compile(read_js) #
    # 用来获取time参数
    time1 = js2py.eval_js('Math.floor(new Date().getTime()/1000)')
    mcode = return_js.call('missjson','{}'.format(time1))
    return mcode

def get_data(mcode):
    url = 'http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1007'
    headers = {
        'mcode': mcode,
        'Referer': 'http://webapi.cninfo.com.cn/',
    }
    params = {
        'tdate': '2022-04-12',
        'market': 'SZE',
    }
    response = requests.get(url=url, headers=headers, params=params).text
    print(response)
if __name__ == '__main__':
    mcode = get_mcode()
    get_data(mcode)