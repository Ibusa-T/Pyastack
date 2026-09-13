"""
2026/09/13 
author Ibusa-T
"""

import threading
from typing import Any,Generic, List, Optional, TypeVar, Union,Iterator


# 1. 任意の型を表す型変数「T」を作る
T = TypeVar('T')
class AtomicStack(Generic[T]):


    def __init__(self
    ,obj:Union[str,List[T]]
    ,capacity:Optional[int] = 255) -> None:
        if capacity is not None and capacity <= 0 :
            raise ValueError('capacity must be a positive integer')
        elif capacity is not None and capacity < len(obj)  :
            raise OverflowError(f'initial object size {len(obj)} exceeds {capacity}')

        self._lock:threading.RLock = threading.RLock()
        with self._lock:
            self._stack = obj
            self.__head  = len(obj) - 1
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

    
    def __len__(self) -> int:
        with self._lock:
            return len(self._stack)

    def __iter__(self) -> Iterator[Union[str, T]]:
      with self._lock:
        return iter(reversed(self.as_list()))
 
    def __str__(self) -> str:
        with self._lock:
            if isinstance(self._stack,list) :
                return ''.join(map(str,self._stack))
            return self._stack
    
    
    def __bool__(self) -> bool:
        with self._lock:
            return bool(self._stack)

    
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

    
    def is_head(self) -> bool:
        with self._lock:
            return self.__head != - 1
    
    def push(self,item:T) -> None:
        with self._lock:
            if self._stack is None :
                raise AttributeError('stack is NonType')
            elif self.is_full():
                    raise OverflowError(f'object size {len(self._stack)} exceeds push item {self.__capacity}')
            if isinstance(self._stack,list):
                self._stack.append(item)
            elif isinstance(self._stack,str):
                self._stack += str(item)
            
            self.__head = self.__head + 1
    
    
    def pop(self) -> Union[str,T]:
        with self._lock:
            if not self.is_head() :
                raise IndexError(f'pointer head of {self.__head}')
            else :
                current_val = self._stack[-1]
                if isinstance(self._stack,list) :
                    del self._stack[-1]
                elif isinstance(self._stack,str) :
                    self._stack = self._stack[:-1]
                self.__head = self.__head - 1            
        return current_val
    
    def peek(self) -> Union[str,T]:
        with self._lock:
            if not self.is_head() :
                raise IndexError(f'pointer head of {self.__head}')
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
    
    """
    プッシュ前にcapacity以上 -> NG
    プッシュ後の合計がcapacityより大きい->NG
    分岐を分けた理由はどちらも理由としては考慮していない問題が別々のため
    メッセージを別にしてわかりやすくした
    """
    def push_many(self,*items:T):
        with self._lock :
            if not items :
                return
            elif self.is_full():
                    raise OverflowError(f'object size {len(self._stack)} exceeds push item {self.__capacity}')
            elif (len(items) + self.__len__()) > self.__capacity :
                raise OverflowError(f'The size being added ({len(self._stack)}) exceeds the capacity of the item to be pushed ({self.__capacity}).')
            
            if isinstance(self._stack,list):
                self._stack.extend(items)
            elif isinstance(self._stack,str) :
                self._stack += "".join(map(str, items))
            self.__head += len(items)
    
    
    def clear(self) -> None:
        with self._lock :
            if isinstance(self._stack,list):
                self._stack = []
            elif isinstance(self._stack,str):
                self._stack = ''
            self.__head = - 1
    
    def is_empty(self) -> bool:
        with self._lock:
            return not self._stack
    
    def is_full(self) -> bool:
        with self._lock:
            if self.__capacity is None :
                return False
            return len(self._stack) >= self.__capacity


if __name__ == '__main__':
    capacity_test_int_stack = AtomicStack([1,2,3],10)
    capacity_test_int_stack.push_many(1,2)
    capacity_test_int_stack.push_many(7,3,4)
    capacity_test_int_stack.push_many(7,3,4)

    """
    from pathlib import Path
    # このファイル (astack.py) の親の親にある LICENSE を取得
    license_path = Path(__file__).resolve().parents[2] / 'LICENSE'
    with open(license_path, encoding='utf-8') as f:
        print(f.read())
    """








































