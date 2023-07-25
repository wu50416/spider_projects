# -*- coding: UTF-8 -*-
'''
@Project ：yj_pj 
@File ：Convert_number.py
@Author ：hao
@Date ：2023/5/23 16:36 
'''
num_to_cn = {
    0: '零', 1: '一', 2: '二', 3: '三', 4: '四',
    5: '五', 6: '六', 7: '七', 8: '八', 9: '九'
}
unit_to_cn = {
    10: '十', 100: '百', 1000: '千', 10000: '万'
}

def num_to_cn_str(num):
    # 将整数转换为字符串并反转
    num_str = str(num)[::-1]
    # 定义结果字符串
    cn_str = ''
    # 遍历每一位数字
    for i in range(len(num_str)):
        digit = int(num_str[i])
        # 处理个位数
        if i == 0 and digit != 0:
            cn_str += num_to_cn[digit]
        # 处理十位数
        elif i == 1:
            if digit != 0:
                cn_str += unit_to_cn[10]
            if digit != 1 and digit != 0:
                cn_str += num_to_cn[digit]
        # 处理其他位数
        else:
            if digit != 0:
                cn_str += num_to_cn[digit] + unit_to_cn[10 ** i]
    # 将结果字符串反转并返回
    return cn_str[::-1]

