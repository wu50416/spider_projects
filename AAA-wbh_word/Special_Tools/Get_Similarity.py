# -*- coding: UTF-8 -*-
'''
@Project ：yj_pj 
@File ：Get_Similarity.py
@Author ：hao
@Date ：2023/6/6 14:50 
'''

import jellyfish

def get_Similarity_num(data1,data2):
    '''
    data1 = "字符串Division4—Arbitration"
    data2 = "Division 4—Arbitration"
    if similarity>0.9:
        print('相似度大于90%！')
    '''
    similarity = jellyfish.jaro_similarity(data1, data2)  # 计算相似度
    print(similarity)
    return similarity


if __name__ == '__main__':
    data1 = "PartI—Preliminary"
    data2 = "Part I—Preliminaryinary"
    get_Similarity_num(data1,data2)







a = [[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]]     # 文档数据
b = [[1,2,3],[2,5],[1,3]]



