import asyncio, os

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

# 迭代生成器
def address_generater(ip_a, ip_b, port_a, port_b):
    a, b = ip_str2num(ip_a), ip_str2num(ip_b)
    for ip in range(a,b):
        ipstr =ip_num2str(ip)
        for port in range(port_a, port_b):
            yield ipstr, port


# 验证地址
async def test_socket(ip, port, f, openweb=False, timeout = 1):
    print(f'{ip}:{port}')
    try:
        t = asyncio.open_connection(ip,port)
        reader, writer = await asyncio.wait_for(t,timeout)
        writer.close()
        await writer.wait_closed()
        if f: f.write(f'{ip}:{port}\n')
        if openweb:
            try:
                opt = 'start' if os.name == 'nt' else 'open'
                os.system(f'{opt} http://{ip}:{port}')
            except: pass
        return ip, port
    except: return None,None

# 批处理器
async def batch_press(it,f):
    for ip, port in it:
        await test_socket(ip, port, f, openweb=True)

if __name__ == '__main__':
    batch = 40
    ip_a, ip_b, port_a, port_b = '192.168.0.2', '192.168.0.255', 80, 81
    it = address_generater(ip_a, ip_b, port_a, port_b)
    with open('ips.txt', 'w+', encoding='utf-8') as f:
        tasks = [batch_press(it, f) for i in range(batch)]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(*tasks))





