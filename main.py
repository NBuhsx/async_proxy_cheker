import os
import time
import random
import asyncio
import colorama
from colorama.ansi import Fore

from user_agent.base import generate_user_agent
from aiohttp import ClientSession
from aiohttp_socks import ProxyConnector, ProxyType

from typing import Iterable

from proxyORM import Proxy
from parse import ParseProxyPattern, parse_search, judges_by_proxy, ResponseSerch
from input_output import read_rows, write_file
from config import REQUEST_COUNT, DIR_WORK


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
            timeout=20) as response:
            if response.ok:
                proxy.status = True
                html_obj = (await response.text())
                proxy.timeout = time.perf_counter() - start_time

                if ip := parse_search(ResponseSerch.host, html_obj):
                    proxy.anonymous = True if proxy.host == ip else False
                proxy.print_log_result()
                return proxy
            else:
                return response.raise_for_status()
            


async def choice_proxy_type(proxy:Proxy):
    global REQUEST_COUNT
    if proxy.proxy_type:
        REQUEST_COUNT += 1
        try:
            return await check(proxy=proxy)
        except Exception:
            proxy.status = False
            proxy.print_log_result()
            return proxy
    else:
        for proxy_type in ProxyType:
            REQUEST_COUNT += 1
            try:
                proxy.proxy_type = proxy_type
                return await check(proxy=proxy)
            except Exception:
                continue
        proxy.status = False
        proxy.print_log_result()
        return proxy



async def soft(proxy_iters:Iterable) -> None:
    tasks = []
    for proxy in proxy_iters:
        task = asyncio.create_task(
            choice_proxy_type(proxy=Proxy(
                    proxy_type_=parse_search(ParseProxyPattern.proxy_type, proxy),
                    host=parse_search(ParseProxyPattern.host, proxy),
                    port=parse_search(ParseProxyPattern.port, proxy),
                    username=parse_search(ParseProxyPattern.username, proxy),
                    password=parse_search(ParseProxyPattern.password, proxy))))
        tasks.append(task)
    results = await asyncio.gather(*tasks)

    write_file(
        pathfile=DIR_WORK + '/good.txt',
        write=(
            proxy.proxy_string() + '\n' for proxy in results if proxy.status))

   
   
def main() -> None:
    start = time.time()
    asyncio.run(soft(proxy_iters=read_rows(
            pathfile=DIR_WORK + '/check.txt')))

    print(f'{colorama.Fore.CYAN + "Время работы" + colorama.Fore.YELLOW + ":"}\
 {colorama.Fore.MAGENTA + str(time.time() - start)}' + colorama.Fore.RESET)
    print(Fore.BLUE + f"Количество сделанных запроса: {Fore.MAGENTA + str(REQUEST_COUNT)}")


if __name__ == '__main__':
    main()