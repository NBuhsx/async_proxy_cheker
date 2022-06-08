from dataclasses import dataclass, InitVar
from aiohttp_socks import ProxyType
from typing import Optional
from colorama import Fore





@dataclass(slots=False)
class Proxy:
    proxy_type : InitVar[Optional[ProxyType|str]] = None
    host: Optional[str] = None
    port: Optional[str] = None
    username:Optional[str] = None
    password: Optional[str] = None
    status: bool = False
    timeout:Optional[float] = None
    anonymous: Optional[bool] = None
    
    def __post_init__(self, pr):
        match pr:
            case ProxyType():
                self.proxy_type = pr
            case 'socks5':
                self.proxy_type = ProxyType.SOCKS5
            case 'socks4':
                self.proxy_type = ProxyType.SOCKS4
            case 'http':
                self.proxy_type = ProxyType.HTTP
            case _:
                self.proxy_type = None


    # __str__(self)
    def proxy_string(self) -> str:
        match self:
            case Proxy(proxy_type, host, port, username=None, password=None):
                if isinstance(proxy_type, ProxyType) and host and port:
                    return f"{proxy_type.name.lower()}://{host}:{port}"

            case Proxy(proxy_type, host, port, username, password=None):
                if isinstance(proxy_type, ProxyType) and username and host and port:
                    return f"{proxy_type.name.lower()}://{host}:{port}"

            case Proxy(proxy_type, host, port, username, passwrod) \
                if isinstance(proxy_type, ProxyType) and username and passwrod and host and port:
                    return f"{proxy_type.name.lower()}://{username}:{passwrod}@{host}:{port}"   
        return f"{self.host}:{self.port}"
      
    

    def print_log_result(self):
        match self:
            case Proxy(status=True):
                print(f"{Fore.GREEN + self.proxy_string()}   {Fore.BLUE + 'status='}{Fore.GREEN + str(self.status)}\
    {Fore.BLUE + 'timeout='}{Fore.MAGENTA + str(self.timeout) if self.timeout else Fore.MAGENTA + str(None)}\
    {Fore.BLUE + 'anonymous='}{Fore.MAGENTA + str(self.anonymous) if self.anonymous else Fore.MAGENTA + 'False'}" + Fore.RESET)
               
            case Proxy(status=False):
                print(f"{Fore.RED + self.proxy_string() + Fore.RESET}   {Fore.BLUE + 'status'}={Fore.RED + str(self.status)}" + Fore.RESET)