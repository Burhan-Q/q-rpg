import time
import threading
from enum import Enum


def total_check(properties:dict[str, int]) -> bool:
    return sum(properties.values()) == 200


def balance_check(properties:dict[str, int]) -> bool:
    return all([0 <= val <= 100 for val in properties.values()])


def exp_to_level_up(level: int) -> int:
    return (level * 10) ** 2


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


class StatusEffects(Enum):
    POISONED = ("Poisoned", "health", 15, 3)
    BURNED = ("Burned", "health", 9, 6)
    FROZEN = ("Frozen", "agility", 8, 10)
    PARALYZED = ("Paralyzed", "agility", 5, 20)
    CONFUSED = ("Confused", "intelligence", 25, 4)
    WEAKENED = ("Weakened", "strength", 8, 20)


class Item:
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


class CharacterAttributes:
    def __init__(
            self,
            name: str,
            job_class: str,
            health: int = 100,
            defense: int = 25,
            strength: int = 25,
            agility: int = 25,
            intelligence: int = 25,
    ) -> None:
        character_sheet = dict(
            health=health,
            defense=defense,
            strength=strength,
            agility=agility,
            intelligence=intelligence
        )
        assert total_check(character_sheet), "Total must equal 200"
        assert balance_check(character_sheet), "Values must be between 0 and 100"
        self._name = name
        self._job_class = job_class
        self._health = health
        self._defense = defense
        self._strength = strength
        self._agility = agility
        self._intelligence = intelligence
        self.__max_health = health
        self.__max_defense = defense
        self.__max_strength = strength
        self.__max_agility = agility
        self.__max_intelligence = intelligence

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def job_class(self) -> str:
        return self._job_class

    @property
    def health(self) -> int:
        return self._health
        
    @health.setter
    def health(self, value: int) -> None:
        self._health = value
        self._health = max(0, self._health)
    
    @property
    def max_health(self) -> int:
        return self.__max_health
    
    @max_health.setter
    def max_health(self, value: int) -> None:
        self.__max_health = value

    @property
    def defense(self) -> int:
        return self._defense

    @defense.setter
    def defense(self, value: int) -> None:
        self._defense = value

    @property
    def max_defense(self) -> int:
        return self.__max_defense

    @max_defense.setter
    def max_defense(self, value: int) -> None:
        self.__max_defense = value        
    
    @property
    def strength(self) -> int:
        return self._strength

    @strength.setter
    def strength(self, value: int) -> None:
        self._strength = value
    
    @property
    def max_strength(self) -> int:
        return self.__max_strength
    
    @max_strength.setter
    def max_strength(self, value: int) -> None:
        self.__max_strength = value
    
    @property
    def agility(self) -> int:
        return self._agility

    @agility.setter
    def agility(self, value: int) -> None:
        self._agility = value

    @property
    def max_agility(self) -> int:
        return self.__max_agility
    
    @max_agility.setter
    def max_agility(self, value: int) -> None:
        self.__max_agility = value

    @property
    def intelligence(self) -> int:
        return self._intelligence
    
    @intelligence.setter
    def intelligence(self, value: int) -> None:
        self._intelligence = value

    @property
    def max_intelligence(self) -> int:
        return self.__max_intelligence
    
    @max_intelligence.setter
    def max_intelligence(self, value: int) -> None:
        self.__max_intelligence = value

    def asdict(self) -> dict:
        return {
            "name": self.name,
            "job_class": self.job_class,
            "health": self.health,
            "defense": self.defense,
            "strength": self.strength,
            "agility": self.agility,
            "intelligence": self.intelligence
        }
    
    def __repr__(self) -> str:
        return f"""{self.name}
        +++ Class:{self.job_class} 
        +++ Health:{self.health} 
        +++ Defense:{self.defense} 
        +++ Strength:{self.strength} 
        +++ Agility:{self.agility} 
        +++ Intelligence:{self.intelligence}
        """


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


class Character(CharacterAttributes):
    def __init__(
            self,
            attributes: CharacterAttributes
        ) -> None:
        super().__init__(**attributes.asdict())
        self._exp = 0
        self._level = 1
        self._exp_to_next_level = exp_to_level_up(self._level)
        self.status = Status.HEALTHY
    
    @property
    def exp(self) -> int:
        return self._exp
    
    @exp.setter
    def exp(self, value: int) -> None:
        self._exp = value
        if self._exp >= self._exp_to_next_level:
            self.level_up()

    @property
    def level(self) -> int:
        return self._level
    
    @level.setter
    def level(self, value: int) -> None:
        self._level = value
    
    def attribute_check(self, attribute: str, value: int) -> bool:
        return getattr(self, attribute) >= value

    def attack(self, target: "Character") -> None:
        if self.status != Status.DEAD:
            target.defend(self.strength)

    def defend(self, damage: int) -> None:
        damage -= self.defense
        if damage > 0:
            self.health -= damage
        if self.health <= 0:
            self.status = Status.DEAD

    def use_item(self, item: Item) -> None:
        setattr(
            self,
            item.effect.lower(),
            getattr(self, item.effect.lower()) + item.value
        )

    def level_up(self) -> None:
        for attribute in {"max_strength", "max_agility", "max_intelligence", "max_defense"}:
            setattr(self, attribute, getattr(self, attribute) + 1)
        self.exp = 0
        self._level += 1
        self.max_health += 10
        self._exp_to_next_level = exp_to_level_up(self._level)
    
    def apply_buff(self, buff:Buff) -> None:
        buff.apply(self)
    
    def apply_debuff(self, debuff:Debuff) -> None:
        debuff.apply(self)

    def effect(self, effect:StatusEffect) -> None:
        self._e = effect  # TODO make this a property
        threading.Thread(target=effect.apply, kwargs={"target": self}, daemon=True).start()
        if self._e.expired and self.status != Status.DEAD:
            self.status = Status.HEALTHY
    
    def __repr__(self) -> str:
        return f"{self.name} +++ Class:{self.job_class} +++ Level:{self.level} +++ XP:{self.exp} +++ Status:{self.status.value}"
    
    def __str__(self) -> str:
        return f"{self.name} the {self.job_class} is {self.status.value}."

    def __add__(self, val) -> None:
        self.exp += val
    
    def __sub__(self, val) -> None:
        self.health -= val

