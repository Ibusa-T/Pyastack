"""
2026/09/13 
author Ibusa-T
"""

import threading
from typing import Any,Generic, List, Optional, TypeVar, Union,Iterator


# 1. 任意の型を表す型変数「T」を作る
T = TypeVar('T')
class AtomicStack(Generic[T]):
    __slots__ = ('_lock','_stack','__capacity')
    def __init__(self
    ,obj:Union[str,List[T]]
    ,capacity:Optional[int] = 255) -> None:
        if obj is None:
            raise ValueError('Object args NonType')     
        elif capacity is not None and capacity <= 0 :
            raise ValueError('capacity must be a positive integer')
        elif capacity is not None and capacity < len(obj)  :
            raise OverflowError(f'initial object size {len(obj)} exceeds {capacity}')

        self._lock:threading.RLock = threading.RLock()
        with self._lock:
            self._stack = obj
            self.__capacity = capacity
        
        
    def __enter__(self) -> 'AtomicStack[T]':	
        self._lock.acquire()
        return self
    
    
    def __exit__(self
                 ,exec_type:Optional[type]
                 ,exec_val:Optional[BaseException]
                 ,exec_tb:Optional[Any]
                 ) -> None:
        self._lock.release()


    def __str__(self) -> str:
        with self._lock:
            if isinstance(self._stack,list) :
                return ''.join(map(str,self._stack))
            return self._stack


    def __len__(self) -> int:
        with self._lock:
            return len(self._stack)


    def __getitem__(self, index: Union[int, slice]) -> Union[Union[str, T], list[Union[str, T]]]:
      with self._lock:
        return self._stack[index]


    def __iter__(self) -> Iterator[Union[str, T]]:
      with self._lock:
        return iter(reversed(self.as_list()))


    def __contains__(self,item:Any) -> bool:
        with self._lock:
            return item in self._stack


    def __reversed__(self) -> Iterator[Union[str, T]]:
        with self._lock:
            return iter(self.as_list())


    def __repr__(self) -> str:
      with self._lock:
        return (
            f"{self.__class__.__name__}(size={len(self._stack)},"
            f" capacity={self.capacity})"
        )
    
    
    def __bool__(self) -> bool:
        with self._lock:
            return bool(self._stack)
    

    @property
    def capacity(self):
        with self._lock:
            return self.__capacity
    

    def as_list(self) -> List[Union[str,T]]:
        with self._lock:
            if isinstance(self._stack,str) and ' ' in self._stack:
                return self._stack.split()
            else :
                return list(self._stack)
            return list(self._stack)

    
    def as_chars(self) -> List[Union[str,T]]:
        with self._lock:
            return list(self._stack)


    @property
    def head(self):
        with self._lock:
            return len(self._stack) - 1


    def is_head(self) -> bool:
        with self._lock:
            return self.head != - 1
    
    
    def push(self,item:T) -> None:
        with self._lock:
            if self.__bool__() :
                raise AttributeError('stack is NonType')  
            elif item is None :
                raise ValueError('item is NonType')
            elif self.is_full():
                    raise OverflowError(f'object size {len(self._stack)} exceeds push item {self.capacity}')
            if isinstance(self._stack,list):
                self._stack.append(item)
            elif isinstance(self._stack,str):
                self._stack += str(item)
            else :
                self._stack.append(item)
    
    def pop(self) -> Union[str,T]:
        with self._lock:
            if not self.is_head() :
                raise IndexError(f'pointer head of {self.head}')
            else :
                current_val = self._stack[-1]
                if isinstance(self._stack,list) :
                    del self._stack[-1]
                elif isinstance(self._stack,str) :
                    self._stack = self._stack[:-1]
        return current_val
    
    
    def peek(self) -> Union[str,T]:
        with self._lock:
            if not self.is_head() :
                raise IndexError(f'pointer head of {self.head}')
            return self._stack[-1]
    
    
    """
    Safety
    """
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
    
    
    def push_many(self, *items: T) -> None:
        with self._lock:
            if None in items:
                raise ValueError('NonType in items')
            elif  self.__bool__() :
                raise AttributeError('stack is NonType')
            elif self.is_full():
                raise OverflowError(
                    f"stack size ({len(self._stack)}) reached capacity"
                    f" ({self.capacity})"
                )
            elif (len(self._stack) + len(items)) > self.capacity:
                raise OverflowError(
                    f"Adding {len(items)} items exceeds available capacity "
                    f"(current: {len(self._stack)}, capacity: {self.capacity})"
                )
            if isinstance(self._stack, list):
                self._stack.extend(items)
            elif isinstance(self._stack, str):
                self._stack += "".join(map(str, items))
            else:
                self._stack.extend(items)
   
    
    def clear(self) -> None:
        with self._lock :
            if isinstance(self._stack,list):
                self._stack = []
            elif isinstance(self._stack,str):
                self._stack = ''
        
    
    def is_full(self) -> bool:
        with self._lock:
            if self.capacity is None :
                return False
            return len(self._stack) >= self.capacity
    
    

if __name__ == '__main__':
    stack = AtomicStack('aaa')
    stack.clear()
    stack.push_many(2)
    print(stack)
    """
    from pathlib import Path
    # このファイル (astack.py) の親の親にある LICENSE を取得
    license_path = Path(__file__).resolve().parents[2] / 'LICENSE'
    with open(license_path, encoding='utf-8') as f:
        print(f.read())
    """








































