import re

from dataclasses import dataclass



judges_by_proxy = (
    'https://www.proxy-listen.de/azenv.php',
    'http://mojeip.net.pl/asdfa/azenv.php',
    'http://www.wfuchs.de/azenv.php',
    'http://azenv.net',
    'http://proxyjudge.us/',

)


@dataclass(slots=True)
class Searhc:
    proxy_type = re.compile(r'(\w+)://')
    host = re.compile(r'(\d+.\d+.\d+.\d+)')
    port = re.compile(r'\d+.\d+.\d+.\d+:(\d+)')
    username = re.compile(r'://(\w+):')
    password = re.compile(r':(\w+)@')


def parse_proxy_url(search_compile:re.Pattern, proxy_url:str):
    if search := search_compile.search(proxy_url):
        return search.group(1)



class RequestSerch:
    host = re.compile(r'REMOTE_ADDR = (\d+.\d+.\d+.\d+)')
    timeout = re.compile(r'REQUEST_TIME = (\d+)')