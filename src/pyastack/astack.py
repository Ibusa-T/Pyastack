"""
2026/09/13 
author Ibusa-T
"""

import threading
from typing import Any,Generic, List, Optional, TypeVar, Union,Iterator

"""AtomicStack"""

# 1. 任意の型を表す型変数「T」を作る
T = TypeVar('T')
class AtomicStack(Generic[T]):
    """基底クラス
  

     Attributes
     _lock(threading.RLock):  排他制御を管理します
     _stack(Union[str,List[T]]):データ構造を扱います
     __capacity(Optional[int]):メモリの上限管理、指定しない場合 規定値の255を適用します
    """
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
    
    """コンテキストマネージャ
    AtomicStackクラスのインスタンスのロックを取得します

    """
        
    def __enter__(self) -> 'AtomicStack[T]':	
        self._lock.acquire()
        return self
    
    
    def __exit__(self
                 ,exec_type:Optional[type]
                 ,exec_val:Optional[BaseException]
                 ,exec_tb:Optional[Any]
                 ) -> None:
        self._lock.release()

    
    """
     
     Returns self._stack(str)

     メンバ変数self._stackがリストの場合
     結合された文字列として返します
    """
    def __str__(self) -> str:
        with self._lock:
            if isinstance(self._stack,list) :
                return ''.join(map(str,self._stack))
            return self._stack
    
    
    """ 
     Returns len(self._stack)

    メンバ変数self._stackの要素数を返します 
    """
    def __len__(self) -> int:
        with self._lock:
            return len(self._stack)

    """
     
     Returns self._stack[index](int)

     sample code
     atomic_stack = AtomicStack([1,2,3],10)
     print(atomic_stack[0])
     print(atomic_stack[0:1])

    """
    def __getitem__(self, index: Union[int, slice]) -> Union[Union[str, T], list[Union[str, T]]]:
      with self._lock:
        return self._stack[index]
    
    
    """
     末尾からアクセスしたイテレータを返します
     Returns iter(reversed(self.as_list()))  (Iterator[Union[str, T]])
    """
    def __iter__(self) -> Iterator[Union[str, T]]:
      with self._lock:
        return iter(reversed(self.as_list()))
    
    """
    """
    def __contains__(self,item:Any) -> bool:
        with self._lock:
            return item in self._stack
    
    """
    インスタンス初期化時の並び順で返します
    Returns iter(self.as_list())  (Iterator[Union[str, T]])
    """
    def __reversed__(self) -> Iterator[Union[str, T]]:
        with self._lock:
            return iter(self.as_list())
    
    
    """カスタムログ"""
    def __repr__(self) -> str:
      with self._lock:
        return (
            f"{self.__class__.__name__}(size={len(self._stack)},"
            f" capacity={self.capacity})"
        )
    
    
    def __bool__(self) -> bool:
        with self._lock:
            return bool(self._stack)
    
    """
    別インスタンスでも、同一の型かつ中身が等しいかをスレッドセーフに判定
    
    Args other(object)
    Returns  self._stack == other._stack
    """
    def __eq__(self, other: object) -> bool:
      if not isinstance(other, AtomicStack):
        # 相手が比較不可能な型なら例外ではなく NotImplemented を返すのが Python の作法
        return NotImplemented
      
      with self._lock:
            with other._lock:
                return self._stack == other._stack
    
    """メモリ上限"""
    @property
    def capacity(self):
        with self._lock:
            return self.__capacity


    """
     
     Returns list(self._stack)

     メンバ変数self._stackが文字列の場合
     リストとして返します
    """
    def as_list(self) -> List[Union[str,T]]:
        with self._lock:
            if isinstance(self._stack,str) and [' ',','] in self._stack:
                return self._stack.split()
            else :
                return list(self._stack)
            return list(self._stack)


    """
     
     Returns list(self._stack)

     メンバ変数self._stackが文字列の場合
     リスト一文字ずつに分解して返します
    """    
    def as_chars(self) -> List[Union[str,T]]:
        with self._lock:
            return list(self._stack)

    """スタックポインタを返します"""
    @property
    def head(self):
        with self._lock:
            return len(self._stack) - 1

    """スタックポインタの終了を判定"""
    def is_head(self) -> bool:
        with self._lock:
            return self.head != - 1
    
    
    """
    新たな要素を一つ追加します    
    
    Args item (T): 追加する要素
    Returns  None
    """
    def push(self,item:T) -> None:
        with self._lock:
            if item is None :
                raise ValueError('item is NonType')
            elif self.is_full():
                    raise OverflowError(f'object size {len(self._stack)} exceeds push item {self.capacity}')
            if isinstance(self._stack,list):
                self._stack.append(item)
            elif isinstance(self._stack,str):
                self._stack += str(item)
            else :
                self._stack.append(item)
    
    """
    要素を削除します
    文字列の場合末尾部分文字列から削除します
    
    Returns  current_val(Union[str,T])
    """
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

    """
    要素を返します
    文字列の場合末尾部分文字列から返します

    Returns  self._stack[-1]
    """
    
    def peek(self) -> Union[str,T]:
        with self._lock:
            if not self.is_head() :
                raise IndexError(f'pointer head of {self.head}')
            return self._stack[-1]
    
    
    """ peekメソッドを安全に実行します
    """

    def peek_optional(self) -> Optional[Union[str,T]]:
        try:
            return self.peek()
        except IndexError as ie:
            return None        
    
    """ popメソッドを安全に実行します
    """
    def pop_optional(self) -> Optional[Union[str,T]]:
        try:
            return self.pop()
        except IndexError as ie :
            return None
    
    
    """ pushメソッドを安全に実行します
    要素の追加は、内部CPythonでメモリは再確保され後実行されます
    """
    def push_many(self, *items: T) -> None:
        with self._lock:
            if None in items:
                raise ValueError('NonType in items')
            elif  not self.__bool__() :
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
   
    
    """ スタックを初期化します""" 
    def clear(self) -> None:
        with self._lock :
            if isinstance(self._stack,list):
                self._stack.clear()
            elif isinstance(self._stack,str):
                self._stack = ''
        
    
    """ スタックのキャパシティ上限を超ると偽を返します"""
    def is_full(self) -> bool:
        with self._lock:
            if self.capacity is None or len(self._stack) < self.capacity:
                return False
            return True
    
    


if __name__ == '__main__':
    import threading
    stack = AtomicStack([], capacity=1000)


    def worker():
        for i in range(100):
            stack.push(i)
        
    threads = [threading.Thread(target=worker) for _ in range(10)]
        
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(len(stack)) # Exactly 1000 without competition

    

    
    """
    from pathlib import Path
    # このファイル (astack.py) の親の親にある LICENSE を取得
    license_path = Path(__file__).resolve().parents[2] / 'LICENSE'
    with open(license_path, encoding='utf-8') as f:
        print(f.read())
    """








































