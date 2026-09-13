import threading
from typing import Any,Generic, List, Optional, TypeVar, Union,Iterator


# 1. 任意の型を表す型変数「T」を作る
T = TypeVar('T')
class AtomicStack(Generic[T]):
    _cls:Optional['AtomicStack[Any]'] = None
    _lock:threading.RLock = threading.RLock()
    _initialized:bool = False
    def __new__(cls,*args,**kwargs) -> 'AtomicStack[T]':
        if cls._cls is None :
            cls._cls = super().__new__(cls)
        return cls._cls   
    
    def __init__(self,obj:Union[str,List[T]]) -> None:
        with self._lock:
            if self._initialized:
                return
            self.__stack = obj
            self.__head  = len(obj) - 1
            self.__index = len(obj) - 1
            self._initialized = True
    
    def __enter__(self) -> 'AtomicStack[T]':
        self._lock.acquire()
        return self
    
    def __exit__(self
                 ,exec_type:Optional[type]
                 ,exec_val:Optional[BaseException]
                 ,exec_tb:Optional[Any]
                 ) -> None:
        self._lock.release()

    def __len__(self) -> int:
        with self._lock:
            return len(self.__stack)

    def __iter__(self) -> Iterator[Union[str,T]]:
        with self._lock :
            self.__index = self.__len__()
            return self

    def __next__(self) -> Union[str,T]:
        with self._lock:
            if self.__index <=0:
                raise StopIteration()
            self.__index-=1
            return self.__stack[self.__index]
    
    def __index__(self) -> int:
        with self._lock:
            return self.__index
    
    def __str__(self) -> str:
        with self._lock:
            if type(self.__stack) == list :
                return ''.join(map(str,self.__stack))
            return self.__stack
    
    def __bool__(self) -> bool:
        with self._lock:
            return bool(self.__stack)

    def as_list(self) -> List[Union[str,T]]:
        with self._lock:
            if type(self.__stack) == str :
                return self.__stack.split()
            return list(self.__stack)

    def as_chars(self) -> List[Union[str,T]]:
        with self._lock:
            return list(self.__stack)

    def is_head(self) -> bool:
        with self._lock:
            return self.__head != - 1
    
    def push(self,items:T) -> None:
        with self._lock:
            if self.is_none() :
                raise AttributeError('stack is NonType')
            if type(self.__stack) == list:
                self.__stack.append(items)
            elif type(self.__stack) == str :
                self.__stack += str(items)
            self.__head = self.__head + 1
    
    def pop(self) -> Union[str,T]:
        with self._lock:
            if not self.is_head() :
                raise IndexError(f'pointer head of {self.__head}')
            else :
                current_val = self.__stack[-1]
                if type(self.__stack) == list :
                    del self.__stack[-1]
                elif type(self.__stack) == str :
                    self.__stack = self.__stack[:-1]
                self.__head = self.__head - 1            
        return current_val
    
    def peek(self) -> Union[str,T]:
        with self._lock:
            if not self.is_head() :
                raise IndexError(f'pointer head of {self.__head}')
            return self.__stack[-1]
 
    def peek_optional(self) -> Optional[Union[str,T]]:
        try:
            return self.peek()
        except IndexError as ie:
            return None        
    
    def pop_optional(self) -> Optional[Union[str,T]]:
        try:
            return self.pop()
        except IndexError as ie :
            return None
    
    def clear(self) -> None:
        with self._lock :
            if type(self.__stack) == list :
                self.__stack = []
            elif type(self.__stack) == str :
                self.__stack = ''
            self.__head = - 1
            self.__index = - 1
    
    def is_empty(self) -> bool:
        with self._lock:
            return not self.__stack
    
    def is_none(self) -> bool:
        with self._lock:
            return self.__stack is None

 
    

if __name__ == '__main__':
    from pathlib import Path
    # このファイル (astack.py) の親の親にある LICENSE を取得
    license_path = Path(__file__).resolve().parents[2] / 'LICENSE'
    with open(license_path, encoding='utf-8') as f:
        print(f.read())
