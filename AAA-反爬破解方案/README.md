## 参数逆向技巧及解决方案
#### 1、RPC远程调用
#### 2、Hook案例
#### 3、Ja3 三种解决方案
#### 4、selenium(当实在破解不了的时候的兜底技能)
#### 5、中间人代理（抓包软件）使用案例
#### 6、五秒盾及解决方案


## 爬虫快速定位技巧

### 一、搜索加密函数常用关键词及说明 ：

    1、MD5 ：
    搜索关键词 ：1732584193、271733879、1732584194、271733878、md5
    原生MD5加密源码生成
    
    2、SHA1 ：
    搜索关键词 ：1732584193、271733879、1732584194、271733878、1009589776
    SHA1源码加密源码生成
    
    3、Base64 ：
    ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 +/=
    往往与其它加密函数结合使用
    
    4、AES ：
    搜索关键词 ：crypto、AES、encrypt
    往往与其它加密函数结合使用
    
    5、DES ：
    搜索关键词 ：crypto、DES、encrypt、mode、padding
    crypto官方网站
    
    6、RSA ：
    搜索关键词 ：setPublicKey、rsa
    jsencrypt官方网站
    
    7、websocket ：
    搜索关键词 ：onopen、onmessage、onsent ，WebSocket
    协议ws和wss ，类似http和https

    8、JS编码 ：
    搜索关键词 ：encodeURI、encodeURIComponent、btoa、escape
    前面两种方式最为常见
    
    9、加密函数导出 ：
    搜索关键词 ：module.exports、exports
    导出加密函数常用方法
    
    10、FROM表单 ：
    搜索关键词 ：password、pwd、sign、userid。加密或非加密 ，关键词 ，搜索词后面加冒号、等于号、前面加点 ，例如pwd:、pwd =、pwd =、.pwd
    搜索表单键值对中值被加密的键 ，表单提交方式为POST ，不同表单搜索关键词不同
    
    11、十六进制 ：
    搜索关键词 ：0123456789ABCDEF、0123456789abcdef

### 二、主要加密解密算法简介 ：

    1、对称性加密算法 ：对称式加密就是加密和解密使用同一个密钥 （AES、DES、3DES）
    
    2、非对称算法 ：非对称式加密就是加密和解密所使用的不是同一个密钥 ，通常有两个密钥 ，称为公钥、私钥，它们两个必需配对使用 ，否则不能打开加密文件 （RSA、DSA、ECC）
    
    3、散列算法 ：又称哈希函数 ，是一种单向加密算法 ，不可逆 ，目前无法解密 （MD5、SHA1、HMAC）
    
    4、Base64 ：算是一个编码算法 ，通常用于把二进制数据编码为可写的字符形式的数据 ，对数据内容进行编码来适合传输。这是一种可逆的编码方式。编码后的数据是一个字符串 ，其中包含的字符为 ：A - Z、a - z、0 - 9、+、/，共64个字符(26 +26 +10 +1 +1 =64 ，其实是65个字符 ，“=”是填充字符 （HTTPS、 HTTP +SSL层）

### 三、各种加密格式 ：
    1、MD5常见16、32、40位
    
    123456 加密 （16位以49开头、32位e10或E10开头 ）:
    49BA59ABBE56E057  E10ADC3949BA59ABBE56E057F20F883E
    
    2、SHA1常见40、64、125位
    123456 加密 （40位以7c开头 ）:
    7c4a8d09ca3762af61e59520943dc26494f8941b
    
    3、AES其中data 是字符串 ，若是对象则用JSON.stringify(data)转化:
    varCryptoJS=require("crypto-js ");vardata='my message ';
    
    secret密钥：
    
    varsecret='secret key 123 ';// Encryptvarciphertext=CryptoJS.AES.encrypt(data,secret).toString();// Decryptvarbytes=CryptoJS.AES.decrypt(ciphertext,'secret key 123 ');
    varoriginalText=bytes.toString(CryptoJS.enc.Utf8);
