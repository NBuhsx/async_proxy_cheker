import os
import time
import random
import asyncio
import colorama

from user_agent.base import generate_user_agent
from aiohttp import ClientSession
from aiohttp_socks import ProxyConnector, ProxyType

from typing import Iterable

from utils import Proxy
from parse import ParseProxyPattern, parse_search, judges_by_proxy, ResponseSerch
from read_write import read_rows





async def check(proxy:Proxy) -> Proxy|None:
    async with ClientSession(connector=ProxyConnector(
                proxy_type=proxy.proxy_type,
                host=proxy.host,
                port=proxy.port,
                username=proxy.username,
                password=proxy.password)) as session:
        start_time = time.perf_counter()
        async with session.get(
            url=random.choice(judges_by_proxy), 
            headers= {
                'User-Agent': generate_user_agent()},
            timeout=15) as response:
            if response.ok:
                proxy.status = True
                html_obj = (await response.text())
                proxy.timeout = time.perf_counter() - start_time

                if ip := parse_search(ResponseSerch.host, html_obj):
                    proxy.anonymous = True if proxy.host == ip else False
                proxy.print_log_result()
            return proxy


async def choice_proxy_type(proxy:Proxy):
    if proxy.proxy_type:
        try: 
            return await check(proxy=proxy)
        except Exception:
            proxy.status = False
            proxy.print_log_result()
            return proxy
    else:
        for proxy_type in ProxyType:
            try:
                proxy.proxy_type = proxy_type
                return await check(proxy=proxy)
            except Exception as error:
                continue
        proxy.status = False
        proxy.print_log_result()
        return proxy



async def soft(proxy_iters:Iterable):
    tasks = []
    for proxy in proxy_iters:
        task = asyncio.create_task(
            choice_proxy_type(proxy=Proxy(
                    proxy_type=parse_search(ParseProxyPattern.proxy_type, proxy),
                    host=parse_search(ParseProxyPattern.host, proxy),
                    port=parse_search(ParseProxyPattern.port, proxy),
                    username=parse_search(ParseProxyPattern.username, proxy),
                    password=parse_search(ParseProxyPattern.password, proxy))))
        tasks.append(task)
    result = await asyncio.gather(*tasks)

   
   
def main():
    start = time.time()
    asyncio.run(soft(proxy_iters=read_rows(
            pathfile=os.path.dirname(os.path.abspath(__file__)) + '/check.txt')))
    print(f'{colorama.Fore.CYAN + "Время работы" + colorama.Fore.YELLOW + ":"}\
 {colorama.Fore.MAGENTA + str(time.time() - start)}' + colorama.Fore.RESET)


if __name__ == '__main__':
    main()