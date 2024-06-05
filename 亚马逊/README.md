## 亚马逊验证码突破

#### 一共有三种方案可以突破亚马逊的反爬机制

#### 1、使用request正面突破
直接正面请求验证码页获取图片后用ddddocr来识别，有一点需要注意的是需要禁用掉request的重定向功能
#### 2、通过修改指纹绕过验证码
经过大量测试后发现，苹果浏览器 safari15_3 与 safari15_5 的 ja3 指纹可以通过亚马逊的检测直接访问到数据，而且比正面突破还要稳定！

#### 3、使用selenium自动化
这部分没什么技术含量，直接获取图片填进去就可以了，暂时不打算写

##### 运行结果：
![1717579353274](https://github.com/wu50416/spider_projects/assets/103317042/62cb57bd-d22d-452b-ac9c-fb6f68a99d9f)

##### 检测点反爬流程图：
![1](https://github.com/wu50416/spider_projects/assets/103317042/a3c246b3-8b86-44fd-89d5-f4fb6eff39d7)

![2](https://github.com/wu50416/spider_projects/assets/103317042/d80405f8-8e0a-49d5-96a9-eee9c83a4984)

