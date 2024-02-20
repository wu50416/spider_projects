### 1、京东登陆验证码（js） 
![image](https://github.com/wu50416/spider_projects/assets/103317042/fafa6237-4de3-4fd8-9bb1-d09e04ec7d92)

#### 思路：

  首先，复制参数b的轨迹，这个轨迹需要正常滑动和最后来回晃动两个种

  注意：晃动的轨迹x是要从0开始的，可以通过扩大F2的大小，压缩页面的大小

  然后，将计算得到的距离 + 复制的正常滑动轨迹的初始距离来截取正常滑动的区间

  重点，取当前时间戳前9位和复制下的正常轨迹的时间后4位，拼接成完整的时间

  之后，通过复制的晃动轨迹 + 最终轨迹的值来模拟晃动；时间处理和上面差不多
        
![image](https://github.com/wu50416/spider_projects/assets/103317042/4124e952-1bdb-45d5-8acf-5f0de0bc30ad)


### 2、京东法拍网数据采集 + 解析：https://auction.jd.com/sifa.html

![image](https://github.com/wu50416/spider_projects/assets/103317042/d62270d9-f1a4-4ca8-b822-7f3dcc7a8b2f)


![image](https://github.com/wu50416/spider_projects/assets/103317042/26240bba-6459-45e1-84d4-aefb85ec5402)

