from more_itertools import islice_extended
from pathlib import Path
from enum import Enum
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
    port: Optional[int] = None
    username:Optional[str] = None
    password: Optional[str] = None
    
    def __post_init__(self):
        match self.proxy_type:
            case 'socks5':
                self.proxy_type = ProxyType.SOCKS5
            case 'socks4':
                self.proxy_type = ProxyType.SOCKS4
            case 'http':
                self.proxy_type = ProxyType.HTTP
            case _:
                self.proxy_type = None
    
    def set_status(self, status):
       setattr(self, 'status', status)