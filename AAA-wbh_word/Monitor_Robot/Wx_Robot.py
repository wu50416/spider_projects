# -*- coding: UTF-8 -*-
'''
@Project ：yj_pj 
@File ：wx_robot.py
@Author ：hao
@Date ：2023/2/6 15:08 
'''
from datetime import datetime

import requests


def send_data(text):
    headers = {'Content-Type': 'application/json'}
    params = {'key': 'c7b36b44-7235-48a5-9da2-d5cf21f5e62c',}       # wbh的监控机器人
    json_data = {'msgtype': 'text','text': {'content': text,},}
    response = requests.post('https://qyapi.weixin.qq.com/cgi-bin/webhook/send',
                             params=params, headers=headers, json=json_data)
    # response = {"errcode":0,"errmsg":"ok"}
    if response.json()['errmsg'] == 'ok':
        print("发送企业微信信息成功！！")
    else:
        print("发送企业微信信息失败！！")


if __name__ == '__main__':
    now_time = str(datetime.now())
    text = f"now_time:2023-03-17 10:54:22.5381157 ==== 警告！文书网 运行超时！"
    send_data(text)

    # now_time = str(datetime.now())
    # try:
    #     run()
    # except Exception as e:
    #     data = f'now_time:{now_time},错误响应：{e}'
    #     send_data(data)
    #     raise data





