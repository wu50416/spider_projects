加密方式：五秒盾 Cloudflare

解决方案：在Linux中使用docker搭建内置浏览器

### Linux服务器命令：
    docker命令（启动8191端口）：
    docker run -d \
      --name=flaresolverr \
      -p 8191:8191 \
      -e LOG_LEVEL=info \
      --restart unless-stopped \
      ghcr.io/flaresolverr/flaresolverr:latest

### Python代码:
    import json
    import requests
     
    url = 'https://www.asxs.com/'
     
    def get_html_data(url):
        sever_url = 'http://localhost:8191/v1'  # 使用docker中的内置浏览器
        payload = json.dumps({
            "cmd": "request.get",
            "url": url,
            "maxTimeout": 6000
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.post(sever_url, headers=headers, data=payload)
        if response.status_code == 200:
            html_content = response.json()['solution']['response']
        else:
            print("================= 访问失败，重新访问中 =================")
            html_data = get_html_data(url)
        return html_data


