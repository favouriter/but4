import asyncio, os, aiohttp

# IP字符串转数字
def ip_str2num(ip:str):
    num = 0
    for n in [int(i) for i in ip.split('.')]:
        num = (num << 8) + n
    return num

# IP数字转字符串
def ip_num2str(ip: int):
    ipstr = []
    for i in range(4):
        ipstr.append(f'{ip & 0xff}')
        ip = ip >> 8
    ipstr.reverse()
    return '.'.join(ipstr)

# 多批IP端生成器
def ips_generater(*args):
    for a, b in args:
        for ip in ip_generater(a,b):
            yield ip

# ip生成器
def ip_generater(ip_a, ip_b):
    a, b = ip_str2num(ip_a), ip_str2num(ip_b)
    a, b = sorted([a, b])
    for ip in range(a,b):
        yield ip_num2str(ip)

# 端口生成器
def port_generater(port_a, port_b):
    port_a, port_b  = sorted([port_a, port_b])
    for port in range(port_a, port_b):
        yield port

# 地址生成器
def address_generater(ips, ports):
    for ip in ips:
        for port in ports:
            yield ip, port

# 验证地址
async def test_socket(ip, port, f, do=None, timeout = 1):
    print(f'{ip}:{port}')
    try:
        t = asyncio.open_connection(ip,port)
        reader, writer = await asyncio.wait_for(t,timeout)
        writer.close()
        await writer.wait_closed()
        if f: f.write(f'{ip}:{port}\n')
        if do is not None: asyncio.create_task(do(ip, port))
        return ip, port
    except: return None,None

# 动作，打开web浏览器
async def openweb(ip, port):
    try:
        opt = 'start' if os.name == 'nt' else 'open'
        os.system(f'{opt} http://{ip}:{port}')
    except: pass

global session
session = None

# 检测打开web
async def checkout_web(ip, port):
    try:
        global session
        session = session or aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))
        print(session)
        async with session.get(f'http://{ip}:{port}') as response:
            if response.status < 500: await openweb(ip, port)
    except Exception as e:
        print(str(e))
        pass

# 批处理器
async def batch_press(it,f, do):
    for ip, port in it:
        await test_socket(ip, port, f, do)

if __name__ == '__main__':
    batch = 400
    # ips = ip_generater('192.168.3.2', '192.168.3.255')
    ips = ips_generater(('192.168.0.2','192.168.0.254'),('192.168.3.2', '192.168.3.255'))
    # ports = port_generater(20,65535)
    ports = [80]

    # 传入IP和端口生成器
    it = address_generater(ips, ports)
    with open('ips.txt', 'w+', encoding='utf-8') as f:
        # 批量检测，检测端口为打开状态，动作为打开web浏览器
        tasks = [batch_press(it, f, checkout_web) for i in range(batch)]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(*tasks))

