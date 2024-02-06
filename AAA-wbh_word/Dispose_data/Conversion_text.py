# -*- coding: UTF-8 -*-
'''
@Project ：yj_pj 
@File ：Conversion_text.py
@Author ：hao
@Date ：2023/5/18 17:34 
'''
import opencc
# 繁体转简体
def Traditional_to_Simplified(text):
    '''
    traditional_str = '這是一個繁體字字符串'
    Traditional_to_Simplified(traditional_str)
    '''
    converter = opencc.OpenCC('t2s.json')
    # 使用OpenCC对象进行繁体字转简体字
    simplified_str = converter.convert(text)
    # 输出结果
    print(f'繁体转简体： {text} -> {simplified_str}')  # 这是一个繁体字字符串 的简体字形式
    return simplified_str



if __name__ == '__main__':
    traditional_str = '這是一個繁體字字符串'
    Traditional_to_Simplified(traditional_str)
