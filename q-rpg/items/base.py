"""Core object for items"""


class BaseItem:
    def __init__(self, name:str, cost:int, value:int, effect:str) -> None:
        self._name = name
        self._cost = cost
        self._value = value
        self._effect = effect
        self._quantity = 1
    
    @property
    def count(self) -> int:
        return self._quantity
    
    @count.setter
    def count(self, amount: int) -> None:
            self._quantity = amount
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def cost(self) -> int:
        return self._cost
    
    @property
    def value(self) -> int:
        return self._value
    
    @property
    def effect(self) -> str:
        return self._effect
    
    def __subtract__(self, amount) -> None:
        self._quantity -= amount
    
    def __add__(self, amount) -> None:
        self._quantity += amount
    
    def __len__(self) -> int:
        return self._quantity
    
    def __repr__(self) -> str:
        return f"{self.name} {self.type}: {self._quantity}"

    def use(self):
        raise NotImplementedError
