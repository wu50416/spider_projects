# -*- coding: UTF-8 -*-
'''
@Project ：yj_pj 
@File ：Encryption_MD5.py
@Author ：hao
@Date ：2023/4/19 17:04 
'''
import hashlib
# md5加密

def get_md5_data(data):
    md5 = hashlib.md5()
    md5.update(data.encode("utf8"))
    result = md5.hexdigest()
    return result


if __name__ == '__main__':
    str_in = '加密前的数据'
    print("加密后：", get_md5_data('https://legalref.judiciary.hk/lrs/common/ju/ju_body.jsp?DIS=146881'))
