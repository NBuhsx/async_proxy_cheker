from typing import Any, Generator, Iterable
from config import DIR_WORK

from input_output import read_rows, write_file, my_input2



def unique_rows(rows:Iterable) -> Generator[str|Any, None, None]:
    # Уникальные строки
    return (i for i in set(rows))



class proxy_type_raw:
    __slots__ = ()
    def socks5(self, proxy:str) -> str: return 'socks5://' + proxy + '\n'
    def socks4(self, proxy:str) -> str: return 'socks4://' + proxy + '\n'
    def http(self, proxy:str) -> str: return 'http://' + proxy + '\n'


"""
Форматирование
...
...
"""

if __name__ == '__name__':

    unique_rows(rows=read_rows(
        pathfile=DIR_WORK + '/check.txt'
    ))


# Быстрое форматирование через input
    write_file(
        pathfile= DIR_WORK + '/check.txt',
        write=my_input2(
            end='',
            execute_with_element=proxy_type_raw().http),
        mode='a')

