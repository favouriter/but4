# but4
收藏一些自己平时用的脚本，but4是beautiful的意思

## fast_host.py
平时访问github和huggingface非常头疼，写个脚本通过各方DNS服务器汇总分析，检测出TCP打开到关闭耗时最短的IP
```python
# scan_dns.py 中 addresses配置了域名和开放的端口，用于检测打开到关闭的耗时
# get_fast方法中使用asyncio.gather汇聚了一些DNS服务器解析结果，也可以加入第三方API，获取更多的IP信息
python fast_host.py
# 20.205.243.168           api.github.com
# 20.205.243.165           codeload.github.com
# 140.82.114.22            collector.github.com
# 13.107.42.16             pipelines.actions.githubusercontent.com
# 185.199.108.133          media.githubusercontent.com
# 185.199.111.133          cloud.githubusercontent.com
# 185.199.108.133          objects.githubusercontent.com
# 20.205.243.166           github.com
# 185.199.109.133          raw.githubusercontent.com
# 185.199.109.153          assets-cdn.github.com
# 185.199.109.154          github.githubassets.com
# 104.17.25.14             cdnjs.cloudflare.com
# 34.211.9.177             m.stripe.com
# 203.208.40.98            fonts.gstatic.com
# 54.192.18.99             aeiljuispo.cloudimg.io
# 34.202.8.246             hf.co

```

## scan_server.py
dhcp分配IP很有可能找不到局域网内的测试设备地址，可以划定IP范围及端口范围，扫描出局域网的服务器，
```python
# address_generater传入两个参数，分别为ips, ports
# ips可以为一下三种写法,ip_generater为一段IP，ips_generater为多段IP，也可以直接用list
ips = ip_generater('192.168.3.2', '192.168.3.255')
ips = ips_generater(('192.168.0.2','192.168.0.254'),('192.168.3.2', '192.168.3.255'))
ips = ('192.168.3.2', '192.168.3.255')
# ports也可以为以下两种写法
ports = port_generater(20,65535)
ports = [80,443,8080]
# batch_press中do为一个异步方法，用于检测端口处于打开状态后执行的动作
# 比如openweb(打开浏览器)，也可以自定义其他的动作
batch_press(it, f, openweb)
```

## clean_mate.py
可以用于清理图片中的头信息，减小图片体积，去除隐私信息，比如拍照时的时间、地点
```python
# 默认清理当前目录下的所以png
python clean_mate.py

# 也可以清理指定目录
python clean_mate.py --path ./images/
```