# -*- coding: utf-8 -*-
import re
import sys
sys.path.append("..")
import time

import requests
from parsel import Selector
import random
from datetime import datetime
from pymongo import MongoClient
from loguru import logger
from wbh_word.spider import Get_response
from wbh_word.manage_data import manage_mysql
from wbh_word.spider import Get_ip


"""
    拍卖状态及成交价url：https://www1.rmfysszc.gov.cn/Object/Finish.shtml?jsoncallback=jQuery35908421121231603159_1670297941339&oid=122119&pid=3694351&_=1670297941357
 state:'4'      # 异常状态  可能取消、暂缓、撤回等等异常的原因      状态码为4 时 ， 状态可在html中获取
 state:'0'      # 即走正常的拍卖流程   可能会 流拍、
                1、可能是 流标：   此时会有流标说明  https://www1.rmfysszc.gov.cn/Object/Getlb.shtml?oid=132030
                2、可能是 成交：   此时有成交确认书  https://www1.rmfysszc.gov.cn/GetHtml.aspx?oid=132618
"""


# /home/wangdong/fp_spider/JD_Script/logger/list_num_data.log
logger.add("/home/wangdong/fp_spider/RMFYSS_Script/logger/IDlist_get_data.log", filter=lambda record: record["extra"]["name"] == "IDlist_get_data")
logger_get_data = logger.bind(name="IDlist_get_data")
table = 'wbh_RMFYSS_id'



def get_headers():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'https://www1.rmfysszc.gov.cn/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    return headers
'''
    id地址：广东
    其他：不限
    有数据      response：{"html":"<div id=132030 class='product' ><div class='p_img'><a href='Handle/132030.shtml' title='广东省惠东县稔山镇亚婆角地段海头埔苑20号楼1单元6层05号房屋一套'><img src='https://filegy.rmfysszc.gov.cn/2022/1020/A6CED3EC96B79327810AAB9C0B0D7061/BEE3692DEB56DEF20A886B236CA760D6/BEE3692DEB56DEF20A886B236CA760D6-1.jpg'></a><div class='p_title'><a href='Handle/132030.shtml'>广东省惠东县稔山镇亚婆角地段海…</a></div></div><div class='prod-guj'><p>起拍价<span>50.712946万</span></p><p>评估值<span>66.291433万</span></p><p>开始时间<span class='time-fd'>11月24日10:00</span><s>即将开始</s></p></div><div class='prod-alink'><a title='' href='Handle/132030.shtml'>91次围观</a><a href='Handle/132030.shtml'>我要竞拍</a></div></div><div id=132004 class='product' ><div class='p_img'><a href='Handle/132004.shtml' title='广州市天河区天河路93号601房三分之一的产权份额'><img src='https://filegy.rmfysszc.gov.cn/2022/1020/967A8530006D86526A40E95740E2D0C7/C64343D66C10BB0BDE38B44145A8CC6F/C64343D66C10BB0BDE38B44145A8CC6F-1.jpg'></a><div class='p_title'><a href='Handle/132004.shtml'>广州市天河区天河路93号601房三…</a></div></div><div class='prod-guj'><p>起拍价<span>138.9055万</span></p><p>评估值<span>173.6318万</span></p><p>开始时间<span class='time-fd'>11月24日10:00</span><s>即将开始</s></p></div><div class='prod-alink'><a title='' href='Handle/132004.shtml'>230次围观</a><a href='Handle/132004.shtml'>我要竞拍</a></div></div><div id=131987 class='product' ><div class='p_img'><a href='Handle/131987.shtml' title='惠州市惠阳区淡水大埔村昶园2幢1单元20层03号房'><img src='https://filegy.rmfysszc.gov.cn/2022/1020/B48DDBE0CD05AA7FFBE176C7FE8FE3EA/FBC3A0D207E86090D5BCA6570BC0DFAE/FBC3A0D207E86090D5BCA6570BC0DFAE-1.jpg'></a><div class='p_title'><a href='Handle/131987.shtml'>惠州市惠阳区淡水大埔村昶园2幢…</a></div></div><div class='prod-guj'><p>起拍价<span>105.1万</span></p><p>评估值<span>150.090248万</span></p><p>开始时间<span class='time-fd'>12月7日10:00</span><s>即将开始</s></p></div><div class='prod-alink'><a title='' href='Handle/131987.shtml'>504次围观</a><a href='Handle/131987.shtml'>我要竞拍</a></div></div><div id=131986 class='product' style='margin-right:0px;'><div class='p_img'><a href='Handle/131986.shtml' title='惠州仲恺高新区惠风六路36号兴伦府3单元11层02号房'><img src='https://filegy.rmfysszc.gov.cn/2022/1020/BF3BC1CF8CAB30EA0D1E527D1D293234/0EA933EA37CBC04D999E4E0B792B3F74/0EA933EA37CBC04D999E4E0B792B3F74-1.JPG'></a><div class='p_title'><a href='Handle/131986.shtml'>惠州仲恺高新区惠风六路36号兴伦…</a></div></div><div class='prod-guj'><p>起拍价<span>43.843万</span></p><p>评估值<span>68.5046万</span></p><p>开始时间<span class='time-fd'>11月28日10:00</span><s>即将开始</s></p></div><div class='prod-alink'><a title='' href='Handle/131986.shtml'>441次围观</a><a href='Handle/131986.shtml'>我要竞拍</a></div></div><div id=131593 class='product' ><div class='p_img'><a href='Handle/131593.shtml' title='广州市天河区员村四横路美林街64号902房二分之一的产权份额'><img src='https://filegy.rmfysszc.gov.cn/2022/1020/68805530F23C2C0ECF2848CF4EB54201/B25434BA6C4EAC9BA38BA3FC165EECF3/B25434BA6C4EAC9BA38BA3FC165EECF3-1.jpg'></a><div class='p_title'><a href='Handle/131593.shtml'>广州市天河区员村四横路美林街6…</a></div></div><p style='color:#535353;height:23px' class='prod-price'><img src='//www.rmfysszc.gov.cn/2017version/images/lb.png'> <strong>177.0816</strong>万</p><div class='prod-guj'><p>评估值<span>281.0818万</span></p><p>流标时间<span class='time-fd'>2022年11月8日10:00</span></p></div><div class='prod-alink'><a href='' style='border:0;'>已流标</a></div></div><div id=131237 class='product' ><div class='p_img'><a href='Handle/131237.shtml' title='车牌号码为粤A377V7日产牌车辆一辆(不带车牌拍卖)'><img src='https://filegy.rmfysszc.gov.cn/2022/1020/658722913B511E0937A1BEC74FE2BF9E/7F57F00BD7A0752E66F1E49AC278DEDC/7F57F00BD7A0752E66F1E49AC278DEDC-1.jpg'></a><div class='p_title'><a href='Handle/131237.shtml'>车牌号码为粤A377V7日产牌车辆一…</a></div></div><p style='color:#535353;height:23px' class='prod-price'><img src='//www.rmfysszc.gov.cn/2017version/images/lb.png'> <strong>3.32</strong>万</p><div class='prod-guj'><p>评估值<span>4.15万</span></p><p>流标时间<span class='time-fd'>2022年10月21日10:00</span></p></div><div class='prod-alink'><a href='' style='border:0;'>已流标</a></div></div><div id=131219 class='product' ><div class='p_img'><a href='Handle/131219.shtml' title='房地产'><img src='https://filegy.rmfysszc.gov.cn/2022/1020/F2AA32A5C5F5F52487C299E38773DBB7/BD8E10B6F4A197A62B4E88A86E2C9A62/BD8E10B6F4A197A62B4E88A86E2C9A62-1.jpg'></a><div class='p_title'><a href='Handle/131219.shtml'>房地产</a></div></div><p style='color:#535353;height:23px' class='prod-price'><img src='//www.rmfysszc.gov.cn/2017version/images/cj.png'> <strong>87.719031</strong>万</p><div class='prod-guj'><p>评估值<span>108.2951万</span></p><p>成交时间<span class='time-fd'>2022年 10月29日10:03</span></p></div><div class='prod-alink'><a href='' style='border:0;'>已成交</a></div></div><div id=130990 class='product' style='margin-right:0px;'><div class='p_img'><a href='Handle/130990.shtml' title='惠州仲恺高新区惠风六路36号兴伦府3单元11层02号房'><img src='https://filegy.rmfysszc.gov.cn/2022/1020/1B0701FBED7226995163F68549ADB828/0EA933EA37CBC04D999E4E0B792B3F74/0EA933EA37CBC04D999E4E0B792B3F74-1.JPG'></a><div class='p_title'><a href='Handle/130990.shtml'>惠州仲恺高新区惠风六路36号兴伦…</a></div></div><p style='color:#535353;height:23px' class='prod-price'><img src='//www.rmfysszc.gov.cn/2017version/images/lb.png'> <strong>54.8037</strong>万</p><div class='prod-guj'><p>评估值<span>68.5046万</span></p><p>流标时间<span class='time-fd'>2022年11月2日10:00</span></p></div><div class='prod-alink'><a href='' style='border:0;'>已流标</a></div></div><div id=130935 class='product' ><div class='p_img'><a href='Handle/130935.shtml' title='车牌号码为粤A377V7日产牌车辆一辆(不带车牌拍卖)'><img src='https://filegy.rmfysszc.gov.cn/2022/1020/A8426788EDC69D7E7A72D180914A734C/7F57F00BD7A0752E66F1E49AC278DEDC/7F57F00BD7A0752E66F1E49AC278DEDC-1.jpg'></a><div class='p_title'><a href='Handle/130935.shtml'>车牌号码为粤A377V7日产牌车辆一…</a></div></div><p style='color:#535353;height:23px' class='prod-price'><img src='//www.rmfysszc.gov.cn/2017version/images/lb.png'> <strong>4.15</strong>万</p><div class='prod-guj'><p>评估值<span>4.15万</span></p><p>流标时间<span class='time-fd'>2022年10月10日10:00</span></p></div><div class='prod-alink'><a href='' style='border:0;'>已流标</a></div></div><div id=130720 class='product' ><div class='p_img'><a href='Handle/130720.shtml' title='房地产'><img src='https://filegy.rmfysszc.gov.cn/2022/1020/4585D8825F35F4DA2A0831C229EFC10E/BD8E10B6F4A197A62B4E88A86E2C9A62/BD8E10B6F4A197A62B4E88A86E2C9A62-1.jpg'></a><div class='p_title'><a href='Handle/130720.shtml'>房地产</a></div></div><p style='color:#535353;height:23px' class='prod-price'><img src='//www.rmfysszc.gov.cn/2017version/images/lb.png'> <strong>87.719031</strong>万</p><div class='prod-guj'><p>评估值<span>108.2951万</span></p><p>流标时间<span class='time-fd'>2022年10月11日10:00</span></p></div><div class='prod-alink'><a href='' style='border:0;'>已流标</a></div></div><div id=130568 class='product' ><div class='p_img'><a href='Handle/130568.shtml' title='广东省惠东县稔山镇亚婆角地段海头埔苑20号楼1单元6层05号房屋一套'><img src='https://filegy.rmfysszc.gov.cn/2022/1020/764707AC9D4BB521F506B2B624259419/BEE3692DEB56DEF20A886B236CA760D6/BEE3692DEB56DEF20A886B236CA760D6-1.jpg'></a><div class='p_title'><a href='Handle/130568.shtml'>广东省惠东县稔山镇亚婆角地段海…</a></div></div><p style='color:#535353;height:23px' class='prod-price'><img src='//www.rmfysszc.gov.cn/2017version/images/lb.png'> <strong>56.347718</strong>万</p><div class='prod-guj'><p>评估值<span>66.291433万</span></p><p>流标时间<span class='time-fd'>2022年10月18日10:00</span></p></div><div class='prod-alink'><a href='' style='border:0;'>已流标</a></div></div><div id=130343 class='product' style='margin-right:0px;'><div class='p_img'><a href='Handle/130343.shtml' title='广州市天河区天河路93号601房三分之一的产权份额'><img src='https://filegy.rmfysszc.gov.cn/2022/1020/ADDDE2A3EBB6F99684503F780809B895/C64343D66C10BB0BDE38B44145A8CC6F/C64343D66C10BB0BDE38B44145A8CC6F-1.jpg'></a><div class='p_title'><a href='Handle/130343.shtml'>广州市天河区天河路93号601房三…</a></div></div><p style='color:#535353;height:23px' class='prod-price'><img src='//www.rmfysszc.gov.cn/2017version/images/lb.png'> <strong>173.6318</strong>万</p><div class='prod-guj'><p>评估值<span>173.6318万</span></p><p>流标时间<span class='time-fd'>2022年10月9日10:00</span></p></div><div class='prod-alink'><a href='' style='border:0;'>已流标</a></div></div><div id=130173 class='product' ><div class='p_img'><a href='Handle/130173.shtml' title='深圳市龙岗区平湖镇华南国际纺织服装原辅料物流区二期B1A-444房产'><img src='https://filegy.rmfysszc.gov.cn/2022/1020/FB9B7B4356A2F796E74F5D9CAC354824/D95ACFC7C52281E6C3C1DB4CF44042C6/D95ACFC7C52281E6C3C1DB4CF44042C6-1.jpg'></a><div class='p_title'><a href='Handle/130173.shtml'>深圳市龙岗区平湖镇华南国际纺织…</a></div></div><p style='color:#535353;height:23px' class='prod-price'><img src='//www.rmfysszc.gov.cn/2017version/images/lb.png'> <strong>85.276368</strong>万</p><div class='prod-guj'><p>评估值<span>106.59546万</span></p><p>流标时间<span class='time-fd'>2022年9月9日10:00</span></p></div><div class='prod-alink'><a href='' style='border:0;'>已流标</a></div></div><div id=129976 class='product' ><div class='p_img'><a href='Handle/129976.shtml' title='房地产'><img src='https://filegy.rmfysszc.gov.cn/2022/1020/27B71378392EFB1F2FC4D7F997AA7B3E/BD8E10B6F4A197A62B4E88A86E2C9A62/BD8E10B6F4A197A62B4E88A86E2C9A62-1.jpg'></a><div class='p_title'><a href='Handle/129976.shtml'>房地产</a></div></div><p style='color:#535353;height:23px' class='prod-price'><img src='//www.rmfysszc.gov.cn/2017version/images/lb.png'> <strong>97.46559</strong>万</p><div class='prod-guj'><p>评估值<span>108.2951万</span></p><p>流标时间<span class='time-fd'>2022年9月14日10:00</span></p></div><div class='prod-alink'><a href='' style='border:0;'>已流标</a></div></div><div id=129901 class='product' ><div class='p_img'><a href='Handle/129901.shtml' title='东风标致牌小型轿车（原车牌号为粤AB025K)'><img src='https://filegy.rmfysszc.gov.cn/2022/1020/237EBEF72AF67F3C3F650C261A3E1B55/35109D611E926835DE28E7C60D1CD573/35109D611E926835DE28E7C60D1CD573-1.jpg'></a><div class='p_title'><a href='Handle/129901.shtml'>东风标致牌小型轿车（原车牌号为…</a></div></div><p style='color:#535353;height:23px' class='prod-price'><img src='//www.rmfysszc.gov.cn/2017version/images/cj.png'> <strong>2.4248</strong>万</p><div class='prod-guj'><p>评估值<span>4.33万</span></p><p>成交时间<span class='time-fd'>2022年 8月25日16:13</span></p></div><div class='prod-alink'><a href='' style='border:0;'>已成交</a></div></div><div id=129887 class='product' style='margin-right:0px;'><div class='p_img'><a href='Handle/129887.shtml' title='茂名市茂南区袂花镇后岭管区芬塘村的土地使用权及该地上建筑物'><img src='https://filegy.rmfysszc.gov.cn/2022/1020/6BA9A0B74C9A8C9FB28E5E8B68994D74/CC815F48D0FA24354B46AFCE659BC92D/CC815F48D0FA24354B46AFCE659BC92D-1.jpg'></a><div class='p_title'><a href='Handle/129887.shtml'>茂名市茂南区袂花镇后岭管区芬塘…</a></div></div><p style='color:#535353;height:23px' class='prod-price'><img src='//www.rmfysszc.gov.cn/2017version/images/lb.png'> <strong>40.5224</strong>万</p><div class='prod-guj'><p>评估值<span>56.28万</span></p><p>流标时间<span class='time-fd'>2022年10月21日10:00</span></p></div><div class='prod-alink'><a href='' style='border:0;'>已流标</a></div></div><div id=129769 class='product' ><div class='p_img'><a href='Handle/129769.shtml' title='车辆'><img src='https://filegy.rmfysszc.gov.cn/2022/1020/FE5892B35D1A7451B5AE6142DEB4D91B/0AD91264D39C79984A749907A058D3EC/0AD91264D39C79984A749907A058D3EC-1.jpg'></a><div class='p_title'><a href='Handle/129769.shtml'>车辆</a></div></div><p style='color:#535353;height:23px' class='prod-price'><img src='//www.rmfysszc.gov.cn/2017version/images/cj.png'> <strong>11.81124</strong>万</p><div class='prod-guj'><p>评估值<span>14.76405万</span></p><p>成交时间<span class='time-fd'>2022年 8月16日10:00</span></p></div><div class='prod-alink'><a href='' style='border:0;'>已成交</a></div></div><div id=129731 class='product' ><div class='p_img'><a href='Handle/129731.shtml' title='番禺区沙湾镇沙湾大道17号4座2梯302'><img src='https://filegy.rmfysszc.gov.cn/2022/1020/ACFA7BF81E6ADD93AC3F20C49AD58D06/FDBD22494EBD623935DC3D5D065CCF71/FDBD22494EBD623935DC3D5D065CCF71-1.jpg'></a><div class='p_title'><a href='Handle/129731.shtml'>番禺区沙湾镇沙湾大道17号4座2梯…</a></div></div><p style='color:#535353;height:23px' class='prod-price'><img src='//www.rmfysszc.gov.cn/2017version/images/lb.png'> <strong>122</strong>万</p><div class='prod-guj'><p>评估值<span>173.791133万</span></p><p>流标时间<span class='time-fd'>2022年8月30日10:00</span></p></div><div class='prod-alink'><a href='' style='border:0;'>已流标</a></div></div><div id=129728 class='product' ><div class='p_img'><a href='Handle/129728.shtml' title='80-045-00-04型号高频外科手术系统设备一台'><img src='https://filegy.rmfysszc.gov.cn/2022/1020/8833DD2D0A949C09EBEE3EB085A28D3A/873F18DEFC41D1EA2A686A68B4D8315E/873F18DEFC41D1EA2A686A68B4D8315E-1.jpg'></a><div class='p_title'><a href='Handle/129728.shtml'>80-045-00-04型号高频外科手术系…</a></div></div><p style='color:#535353;height:23px' class='prod-price'><img src='//www.rmfysszc.gov.cn/2017version/images/lb.png'> <strong>63.36</strong>万</p><div class='prod-guj'><p>评估值<span>70.4万</span></p><p>流标时间<span class='time-fd'>2022年10月8日10:00</span></p></div><div class='prod-alink'><a href='' style='border:0;'>已流标</a></div></div><div id=129448 class='product' style='margin-right:0px;'><div class='p_img'><a href='Handle/129448.shtml' title='广州市天河区员村四横路美林街64号902房二分之一的产权份额'><img src='https://filegy.rmfysszc.gov.cn/2022/1020/9AE3B1F8DAE03352C5E1CB978D0D83D6/B25434BA6C4EAC9BA38BA3FC165EECF3/B25434BA6C4EAC9BA38BA3FC165EECF3-1.jpg'></a><div class='p_title'><a href='Handle/129448.shtml'>广州市天河区员村四横路美林街6…</a></div></div><p style='color:#535353;height:23px' class='prod-price'><img src='//www.rmfysszc.gov.cn/2017version/images/lb.png'> <strong>196.7573</strong>万</p><div class='prod-guj'><p>评估值<span>281.0818万</span></p><p>流标时间<span class='time-fd'>2022年8月16日10:00</span></p></div><div class='prod-alink'><a href='' style='border:0;'>已流标</a></div></div>","page":"<a  onclick='post(1)' class='pagecur'>1</a><a  onclick='post(2)' class='pagecur1'>2</a><a  onclick='post(3)' class='pagecur1'>3</a><a  onclick='post(4)' class='pagecur1'>4</a><a  onclick='post(5)' class='pagecur1'>5</a><a  onclick='post(2)' class='next'>下一页</a><a  onclick='post(31)' class='next'>尾页</a>"}
    判断终止条件 response：{"html":"<div class='tip'>暂无您查询的标的物</div>","page":"<a  onclick='post(1)' class='next'>首页</a><a  onclick='post(31)' class='next'>上一页</a><a  onclick='post(29)' class='pagecur1'>29</a><a  onclick='post(30)' class='pagecur1'>30</a><a  onclick='post(31)' class='pagecur1'>31</a><a  onclick='post(32)' class='pagecur'>32</a><a  onclick='post(33)' class='pagecur1'>33</a><a  onclick='post(33)' class='next'>下一页</a><a  onclick='post(31)' class='next'>尾页</a>"}
'''
def get_id_list():
    # 给初始值
    break_bool = True       # 是否向下翻页
    page = 1
    proxies = Get_ip.ip_proxies()
    # proxies = None
    all_save_num = 0
    while break_bool:
        down_time = str(datetime.now())  # 首次入库时间
        update_time = str(datetime.now())  # 更新时间

        data = {
            'type': '0',
            'name': '',
            'area': '广东省',
            'city': '广东省',
            'city1': '==请选择==',
            'city2': '==请选择==',
            'xmxz': '0',
            'state': '0',
            'money': '',
            'money1': '',
            'number': '0',
            'fid1': '',
            'fid2': '',
            'fid3': '',
            'order': '0',
            'page': f'{str(page)}',
            'include': '0',
        }
        headers = get_headers()
        url = 'https://www1.rmfysszc.gov.cn/ProjectHandle.shtml'
        response,proxies = Get_response.post_json_response(url,headers,data=data,proxies=proxies)
        # response = requests.post('https://www1.rmfysszc.gov.cn/ProjectHandle.shtml',headers=headers,data=data,proxies=proxies,timeout=5)
        # print(response.text)
        # response = response.json()
        html = response['html']
        selector = Selector(text=html)
        page_allid = selector.xpath('//div[contains(@class,"product")]/@id').extract()
        logger_get_data.info(f'获取第{page}页成功！！本页id共有{len(page_allid)},本页id为：{page_allid}')

        data_list = []
        for item_id_str in page_allid:
            pattern = r"\d+"
            item_id = int(re.findall(pattern, item_id_str)[0])          # 匹配所有的id
            data_dict = {"item_id":item_id,"down_time":down_time,"update_time":update_time,"status_Mongo":1,"status_Update":1}

            return_data_list = ['item_id']  # 查询后返回的字段
            where_list = [{"item_id": item_id}]
            where_data = manage_mysql.read_where_data(table, return_data_list, where_list)

            if where_data:  # 查询数据表中是否有数据，有就退出，没有就插入
                # print(f"第{page}页 - item_id：{item_id} - 数据重复 跳过！")
                # print(f"item_name：{item_name} - item_id：{item_id} - 数据重复 跳过！")
                # break_bool = False  # 不再进行翻页操作
                continue
            else:
                data_list.append(data_dict)
        if data_list:
            all_save_num += len(data_list)
            logger_get_data.info(f'本页入库数据共{len(data_list)}条 ----- {data_list}')
            manage_mysql.save_data(table, data_list)
        else:
            logger_get_data.info(f'==================   第{page}页 数据全部重复  跳过  ==================\n')
        page += 1
        if '下一页' not in str(response['page']):
            break_bool = False
        time.sleep(random.randint(1000, 3000)/1000)
    logger_get_data.info(f'获取id成功！！本次获取数据{all_save_num}条')

if __name__ == '__main__':
    # id_list = [132030,131997,131995,131993]
    id_list = get_id_list()

