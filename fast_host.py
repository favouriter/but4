import asyncio, aiohttp, time
import dns.asyncresolver

# 检测IP、端口打开关闭的速度
async def check_ip(domain, ip, session, port=443):
    try:
        start = time.time()
        t = asyncio.open_connection(ip, port)
        reader, writer = await asyncio.wait_for(t, 60)
        writer.close()
        await writer.wait_closed()
        dey = time.time() - start
        print(f'{domain:<25}\t\t{ip:<20}\t\t{dey:.3f}')
        return ip, dey
    except:
        return ip, 60

# 检查web打开速度
async def check_web(domain, ip, session, port=443):
    try:
        headers=dict(Host=domain,Origin=f'https://{domain}')
        start = time.time()
        async with session.get(f'https://{ip}:{port}', headers=headers, ssl=False) as response:
            dey = time.time() - start
            print(f'{domain:<25}\t\t{ip:<20}\t\t{dey:.3f}')
            return ip, dey
        return ip, 60
    except Exception as e:
        print(str(e))
        return ip, 60

# 使用域名服务器解析查询
async def get_ip_by_dns(domain, tcp = False, host=None, port=None):
    try:
        resolve = dns.asyncresolver.Resolver()
        resolve.nameservers=[host]
        answers = await resolve.resolve(domain, 'A')
        return [str(answer) for answer in answers]
    except Exception as e:
        print(str(e))
        return []

# 使用114域名解析服务器
async def get_ip_by_114dns(domain):
    return await get_ip_by_dns(domain, host='114.114.114.114')

# 使用百度域名解析服务器
async def get_ip_by_baidudns(domain):
    return await get_ip_by_dns(domain, host='180.76.76.76')

# 使用腾讯域名解析服务器
async def get_ip_by_tengxundns(domain):
    return await get_ip_by_dns(domain, host='119.29.29.29')

# 使用阿里域名解析服务器
async def get_ip_by_alidns(domain):
    return await get_ip_by_dns(domain, host='223.5.5.5')

# 使用当前域名解析服务器
async def get_ip_by_localdns(domain):
    return await get_ip_by_dns(domain)

# 根据域名查找最快的IP
async def get_fast(domain, session, port = 443, check=check_web):
    # 汇总不同的查询途径
    ips = await asyncio.gather(
        get_ip_by_alidns(domain),
        get_ip_by_114dns(domain),
        get_ip_by_tengxundns(domain),
        get_ip_by_baidudns(domain),
        get_ip_by_localdns(domain),
    )
    ips = set([ip for isub in ips for ip in isub])
    print(domain, ips)
    check_ips = await asyncio.gather(*[check_web(domain, ip, session, port=port) for ip in ips])
    check_ips = [ip for ip in check_ips if ip[1] < 60]
    if len(check_ips) == 0: return domain, None
    fast_ip = sorted(check_ips, key=lambda x: x[1])[0][0]
    return domain, fast_ip


# 批量检测域名
async def check_domains(addresses):
    # fast_ips = await asyncio.gather(*[get_fast(addr[0], port=addr[1]) for addr in addresses])
    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))
    fast_ips = []
    for addr in addresses:
        fast_ips.append(await get_fast(addr[0], session, port=addr[1], check=addr[2]))
        await asyncio.sleep(1)
    with open('./out/fast_host.txt', 'w', encoding='utf-8') as f:
        for addr in fast_ips:
            if addr[1] is None: continue
            foramt_host = f'{addr[1]:<25}{addr[0]}\n'
            print(foramt_host, end='')
            f.write(foramt_host)

if __name__ == '__main__':
    addresses = [
        # ('api.github.com', 443, check_web),
        # ('codeload.github.com', 443, check_web),
        # ('collector.github.com', 443, check_web),
        # ('pipelines.actions.githubusercontent.com', 443, check_web),
        # ('media.githubusercontent.com', 443, check_web),
        # ('cloud.githubusercontent.com', 443, check_web),
        # ('objects.githubusercontent.com', 443, check_web),
        ('github.com', 443, check_web),
        # ('raw.githubusercontent.com', 443, check_web),
        # ('assets-cdn.github.com', 443, check_web),
        # ('github.githubassets.com', 443, check_web),
        # ('huggingface.co', 443, check_web),
        # ('cdnjs.cloudflare.com', 443, check_web),
        # ('m.stripe.com', 443, check_web),
        # ('fonts.gstatic.com', 443, check_web),
        # ('aeiljuispo.cloudimg.io', 443, check_web),
        ('cdn-lfs.huggingface.co', 443, check_web),
        ('hf.co',22, check_ip),
    ]

    loop = asyncio.get_event_loop()

    loop.run_until_complete(check_domains(addresses))
