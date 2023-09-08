# but4
收藏一些自己平时用的脚本，but4是beautiful的意思

## fast_host.py
平时访问github和huggingface非常头疼，写个脚本通过各方DNS服务器汇总分析，检测出TCP建立到关闭耗时最短的IP

## scan_server.py
dhcp分配IP很有可能找不到局域网内的测试设备地址，可以划定IP范围及端口范围，扫描出局域网的服务器，
```python
# address_generater传入两个参数，分别为ips, ports
# ips可以为一下两种写法
ips = ip_generater('192.168.3.2', '192.168.3.255')
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