import os
import time
import random
import asyncio

from user_agent.base import generate_user_agent
from aiohttp import ClientSession
from aiohttp_socks import ProxyConnector, ProxyType

from typing import Iterable

from utils import read_rows, Proxy
from parse import Searhc, parse_proxy_url, judges_by_proxy




async def check(session:ClientSession):
    async with session.get(
        url=random.choice(judges_by_proxy), 
        headers= {
            'User-Agent': generate_user_agent()},
        timeout=15) as response:
        return response
            



async def choice_proxy_type(proxy:Proxy):
    if proxy.proxy_type:
        try: 
            async with ClientSession(connector=ProxyConnector(
                proxy_type=proxy.proxy_type,
                host=proxy.host,
                port=proxy.port,
                username=proxy.username,
                password=proxy.password)) as session:

                await check(session=session)
        except Exception:
            return proxy.set_status(status='BAD')
    else:
        for proxy_type in ProxyType:
            try:
                async with ClientSession(connector=ProxyConnector(
                    proxy_type=proxy_type,
                    host=proxy.host,
                    port=proxy.port,
                    username=proxy.username,
                    password=proxy.password)) as session:

                    response = await check(session=session)
                    print(response)
            except Exception as error:
                continue
        return proxy.set_status(status='BAD')



async def soft(proxy_iters:Iterable):
    tasks = []
    for proxy in proxy_iters:
        task = asyncio.create_task(
            choice_proxy_type(proxy=Proxy(
                    proxy_type=parse_proxy_url(Searhc.proxy_type, proxy),
                    host=parse_proxy_url(Searhc.host, proxy),
                    port=parse_proxy_url(Searhc.port, proxy),
                    username=parse_proxy_url(Searhc.username, proxy),
                    password=parse_proxy_url(Searhc.password, proxy))))
        tasks.append(task)
    await asyncio.gather(*tasks)
   
   
   
def main():
    start = time.time()
    asyncio.run(soft(proxy_iters=read_rows(
            pathfile=os.path.dirname(os.path.abspath(__file__)) + '/check.txt')
    ))
    print(f'Время работы: {time.time() - start}')


if __name__ == '__main__':
    main()