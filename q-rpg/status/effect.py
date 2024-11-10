from enum import Enum

class Status(Enum):
    HEALTHY = "Healthy"
    POISONED = "Poisoned"
    BURNED = "Burned"
    FROZEN = "Frozen"
    PARALYZED = "Paralyzed"
    CONFUSED = "Confused"
    WEAKENED = "Weakened"
    DEAD = "Dead"
    BUFFED = "Buffed"
    DEBUFFED = "Debuffed"


class StatusArgs(Enum):
    POISONED = ("Poisoned", "health", 15, 3)
    BURNED = ("Burned", "health", 9, 6)
    FROZEN = ("Frozen", "agility", 8, 10)
    PARALYZED = ("Paralyzed", "agility", 5, 20)
    CONFUSED = ("Confused", "intelligence", 25, 4)
    WEAKENED = ("Weakened", "strength", 8, 20)


class StatusEffect:
    def __init__(self, name: str, effects: str, duration: int, value_over_time:int) -> None:
        self._name = name
        self._effects = effects
        self._duration = duration
        self._value_over_time = value_over_time
        self._lasts_until = 0
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def duration(self) -> int:
        return self._duration
    
    @duration.setter
    def duration(self, value: int) -> None:
        self._duration = value
    
    @property
    def effect(self) -> str:
        return self._effects
    
    @property
    def value_over_time(self) -> int:
        return self._value_over_time
    
    @property
    def status(self):
        return getattr(Status, self.name.upper())

    @property
    def expired(self) -> bool:
        return time.time() > self._lasts_until

    def apply(self, target: "Character") -> None:
        self._lasts_until = time.time() + self.duration
        while not self.expired and self._duration > 0:
            target.status = self.status
            target.health -= self.value_over_time
            self.duration -= 1
            time.sleep(1)
            if self.expired or target.status == Status.DEAD:
                break
        if self.expired and target.status != Status.DEAD:
            target.status = Status.HEALTHY

    def __repr__(self) -> str:
        return f"{self.name} +++ Duration:{self.duration} +++ Effect:{self.effect}"
    
    def __add__(self, val:int) -> None:
        self._lasts_until += val
        self._duration += val
    
    def __sub__(self, val:int) -> None:
        self._lasts_until -= val
        self._duration -= val


class Buff(StatusEffect):
    def __init__(self, attribute:str, duration: int, value: int) -> None:
        super().__init__("BUFFED", attribute.lower(), duration, value)
    
    def apply(self, target: "Character") -> None:
        if not self.expired():
            target.status = Status.BUFFED
            setattr(
                target,
                self.effect,
                getattr(target, self.effect) + self.value_over_time
            )
            self._duration -= 1
        elif self.expired() and target.status != Status.DEAD:
            target.status = Status.HEALTHY


class Debuff(StatusEffect):
    def __init__(self, attribute:str, duration: int, value: int) -> None:
        super().__init__("DEBUFFED", attribute.lower(), duration, value)
    
    def apply(self, target: "Character") -> None:
        if not self.expired():
            target.status = Status.DEBUFFED
            setattr(
                target,
                self.effect,
                getattr(target, self.effect) - self.value_over_time
            )
            self._duration -= 1
        elif self.expired() and target.status != Status.DEAD:
            target.status = Status.HEALTHY
