from datetime import datetime,timedelta
import time

'''
    已停止更新
    请勿引用本模块！！！！！
    请使用Dispose_Data 文件下的 Dispose_time
'''

def split_time(startdate,enddate):
    '''
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
            startdate = datetime(2022,1,1)
            enddate = datetime(2022,1,30)
        output：[[one_time,two_time],[two_time,three_time]]
    '''
    byday_time_list = split_time(startdate, enddate)
    time_list = []
    between_index = int(len(byday_time_list)/2)
    one_time = byday_time_list[0]
    two_time = byday_time_list[between_index]
    three_time = byday_time_list[-1]
    time_list = [[one_time,two_time],[two_time,three_time]]
    return time_list

def get_sf_time(time_data):
    '''
    s_time = datetime(2017, 10, 1)
    sf = get_sf_time(s_time)
    '''
    sf_time = str(int(time.mktime(time_data.timetuple()))*1000)
    print(sf_time)
    return sf_time

if __name__ == '__main__':
    startdate = datetime(2022,8,1)
    enddate = datetime(2022,11,11)
    time_data = get_three_time(startdate,enddate)
    print(time_data)
    s_time = datetime(2017, 10, 1)
    sf = get_sf_time(s_time)





