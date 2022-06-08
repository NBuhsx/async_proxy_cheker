from more_itertools import islice_extended
from pathlib import Path
from typing import Callable, Generator, Any, Iterable, Optional, Literal


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