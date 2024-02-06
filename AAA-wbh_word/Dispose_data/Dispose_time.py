# -*- coding: UTF-8 -*-
'''
@Project ：yj_pj -> wbh_word
@File ：Dispose_time.py
@Author ：hao
@Date ：2022/12/5 16:07 
'''
import time
from datetime import datetime,timedelta

def get_sf_time(time_data):
    '''
    time_data = datetime(2017, 10, 1)
    return = 1506787200000
    '''
    sf_time = str(int(time.mktime(time_data.timetuple()))*1000)
    # print(sf_time)
    return sf_time

def get_time_data(sf_time):
    '''
    sf_time = 1506787200000
    return = 2017-10-01 00:00:00
    '''
    time_datas = int(sf_time) / 1000
    time_data1 = time.localtime(time_datas)
    time_data = time.strftime("%Y-%m-%d %H:%M:%S", time_data1)
    # print(time_data)
    return time_data


def change_str_to_datetime(date_str):
    '''
    datetime_data = '2019-06-20'
    return = 2019-06-20 00:00:00            datetime格式
    '''
    dt_str = datetime.strptime(date_str, '%Y-%m-%d')
    return dt_str


def change_en_to_datetime(date_str):
    '''
    英文转datetime
    datetime_data = 'April 8, 2019'
    return = 2019-06-20 00:00:00            datetime格式
    '''
    dt_str = datetime.strptime(date_str, '%B %d, %Y')
    return dt_str


def change_datetime_to_str(datetime_data):
    '''
    datetime_data = datetime(2022, 1, 1)
    return = 2022-01-01
    '''
    dt_str = datetime_data.strftime("%Y-%m-%d %H:%M:%S")
    return dt_str


def split_time(startdate,enddate):
    '''
        startdate = datetime(2022,1,1)
        enddate = datetime(2022,1,30)
        输入起始时间，获取 byday 的时间列表
    '''
    time_list = []
    startdate = datetime.strptime(str(startdate)[:10], '%Y-%m-%d')
    enddate = datetime.strptime(str(enddate)[:10], '%Y-%m-%d')
    while 1:
        tempdate = startdate + timedelta(days=1)
        if tempdate > enddate:
            time_list.append((startdate))
            break
        time_list.append((startdate))
        # startdate = tempdate + timedelta(days=1)
        startdate = tempdate + timedelta()
    # print(time_list)
    return time_list


def get_three_time(startdate, enddate):
    '''
        输入起始时间，获取 开始时间、中间时间、结束时间
        可以传入两种格式
        startdate = datetime(2022, 1, 1) or "2022-01-01"
        enddate = datetime(2022, 1, 30)  or "2022-01-30"
        output：[[one_time,two_time],[two_time,three_time]]
        [[datetime.datetime(2022, 1, 1, 0, 0), datetime.datetime(2022, 1, 16, 0, 0)], [datetime.datetime(2022, 1, 16, 0, 0), datetime.datetime(2022, 1, 30, 0, 0).....]]
    '''
    byday_time_list = split_time(startdate, enddate)
    between_index = int(len(byday_time_list)/2)
    one_time = byday_time_list[0]
    two_time = byday_time_list[between_index]
    three_time = byday_time_list[-1]
    time_list = [[one_time,two_time],[two_time,three_time]]
    return time_list


def get_three_time_str(startdate, enddate):
    '''
        输入起始时间，获取 开始时间、中间时间、结束时间
        可以传入两种格式
        startdate = datetime(2022, 1, 1)
        enddate = datetime(2022, 1, 30)
        # startdate = "2022-01-01"
        # enddate = "2022-01-30"
        output：[['2022-01-01 00:00:00', '2022-01-16 00:00:00'], ['2022-01-16 00:00:00', '2022-01-30 00:00:00']]
    '''
    byday_time_list = split_time(startdate, enddate)
    between_index = int(len(byday_time_list)/2)
    one_time = byday_time_list[0]
    two_time = byday_time_list[between_index]
    three_time = byday_time_list[-1]


    one_time = change_datetime_to_str(one_time)         # datetime.datetime(2022, 1, 1, 0, 0) -> 2022-01-01
    two_time = change_datetime_to_str(two_time)
    three_time = change_datetime_to_str(three_time)
    time_list = [[one_time,two_time],[two_time,three_time]]
    return time_list


if __name__ == '__main__':
    a = get_time_data(1673597615000)
    print(a)
    startdate = datetime(2022, 1, 1)
    enddate = datetime(2022, 1, 30)
    # startdate = "2022-01-01"
    # enddate = "2022-01-30"
    aa = get_three_time(startdate, enddate)
    print(aa)
    bb = get_three_time_str(startdate, enddate)
    print(bb)
    # dt_str = startdate.strftime("%Y-%m-%d %H:%M:%S")
    # print(dt_str)

    print(change_en_to_datetime(' April 8, 2019'))

