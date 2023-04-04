# -*- coding: UTF-8 -*-
'''
@Project ：yj_pj 
@File ：Split_task_list.py
@Author ：hao
@Date ：2023/4/4 9:53 
'''
# 平均切割列表 主要用于多线程任务切割
def split_list(list_data,thread_num):
    '''
    list_data : 待切割的任务列表
    thread_num ： 需要切割的数量
    return ： [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]
    '''
    list_total = []
    num = thread_num  # 线程数量
    x = len(list_data) // num  # 将参数进行分批（批数 = 线程数）方便传参
    count = 1  # 计算这是第几个列表
    for i in range(0, len(list_data), x):
        if count < num:
            list_total.append(list_data[i:i + x])
            count += 1
        else:
            list_total.append(list_data[i:])
            break
    return list_total




