
前提：需要在网页端启动油猴脚本！

设置端口：
修改 conf/config.properties 文件 sekiro.port=6001  修改端口    与 油猴的脚本代码的端口保持一致

在运行之前：
1、需要先打开 浏览器 对应的网站
2、在油猴上修改头信息   Ag：       // @match        https://www.taobao.com/*
3、修改需要执行的js代码：默认为：            var result = document.cookie;
                                          resolve(result);
4、打开RPC连接通信并挂起，  bin/sekiro.bat
5、刷新浏览器并检查 是否有 sekiro: begin of connect to wsURL: xxx等等信息  有就是成功
