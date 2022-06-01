from more_itertools import islice_extended
from pathlib import Path
from dataclasses import dataclass


from typing import Callable, Generator, Any, Iterable, Optional, Literal
from aiohttp_socks import ProxyType

#Читает прокси
def read_rows(
        pathfile:str|Path, 
        templete:Optional[Callable[[str], Any]]=None, 
        mode:Literal['r', 'rb']='r', 
        islice:slice=slice(0,None,1), 
        encoding:str='utf-8') -> Generator[str | Any, None, None]:
    """Возращает генератор по строчно"""
    with open(file=pathfile, mode=mode, encoding=encoding) as file:
        for row in islice_extended(file)[islice]:
            try:
                yield templete(row) if templete else row
            except GeneratorExit:
                break
            except:
                continue


@dataclass
class Proxy:
    proxy_type: Optional[str|ProxyType] = None
    host: Optional[str] = None
    port: Optional[str] = None
    username:Optional[str] = None
    password: Optional[str] = None
    status: bool = False
    timeout:Optional[float] = None
    anonymous: Optional[bool] = None
    
    def __post_init__(self):
        match self.proxy_type:
            # case ProxyType():
            #     pass
            case 'socks5':
                self.proxy_type = ProxyType.SOCKS5
            case 'socks4':
                self.proxy_type = ProxyType.SOCKS4
            case 'http':
                self.proxy_type = ProxyType.HTTP
            case _:
                self.proxy_type = None

    # __str__(self)
    def proxy_string(self):
        match self:
            case Proxy(proxy_type, host, port, username, passwrod) \
                if isinstance(proxy_type, ProxyType) and username and passwrod and host and port:
                    return f"{proxy_type.name.lower()}://{username}:{passwrod}@{host}:{port}"

            case Proxy(proxy_type, host, port, username=None, password=None) \
                if isinstance(proxy_type, ProxyType) and host and port:
                    return f"{proxy_type.name.lower()}://{host}:{port}"
    
    def print_log_result(self):
        match self:
            case Proxy(timeout, status=True) if timeout:
                print(self.proxy_string(), timeout)

