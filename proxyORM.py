from dataclasses import dataclass, InitVar
from aiohttp_socks import ProxyType
from typing import Optional
from colorama import Fore



@dataclass(slots=False)
class Proxy:
    proxy_type_ : InitVar[Optional[ProxyType|str]] = None
    host: Optional[str] = None
    port: Optional[str] = None
    username:Optional[str] = None
    password: Optional[str] = None
    status: bool = False
    timeout:Optional[float] = None
    anonymous: Optional[bool] = None
    


    def __post_init__(self, proxy_type_:Optional[ProxyType|str]) -> None:
        match proxy_type_:
            case ProxyType():
                self.proxy_type = proxy_type_
            case 'socks5':
                self.proxy_type = ProxyType.SOCKS5
            case 'socks4':
                self.proxy_type = ProxyType.SOCKS4
            case 'http':
                self.proxy_type = ProxyType.HTTP
            case _:
                self.proxy_type = None

    
    def proxy_string(self) -> str:
        string = ''
        if self.proxy_type:
            string += self.proxy_type.name.lower() + '://'
        if self.username and self.password:
            string += self.username + ':' + self.password + '@'
        if self.host and self.port:
            string +=  self.host + ':' + self.port
        return string


    def print_log_result(self) -> None:
        match self:
            case Proxy(status=True):
                print(f"{Fore.GREEN + self.proxy_string()}   {Fore.BLUE + 'status='}{Fore.GREEN + str(self.status)}\
    {Fore.BLUE + 'timeout='}{Fore.MAGENTA + str(self.timeout) if self.timeout else Fore.MAGENTA + str(None)}\
    {Fore.BLUE + 'anonymous='}{Fore.MAGENTA + str(self.anonymous) if self.anonymous else Fore.MAGENTA + 'False'}" + Fore.RESET)
               
            case Proxy(status=False):
                print(f"{Fore.RED + self.proxy_string() + Fore.RESET}   {Fore.BLUE + 'status'}={Fore.RED + str(self.status)}" + Fore.RESET)