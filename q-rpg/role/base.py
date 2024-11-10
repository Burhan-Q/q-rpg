"""Core components for characters."""

import threading

from overseer import total_check, balance_check, exp_to_level_up
from status import Status, StatusEffect, Buff, Debuff


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
        return f"""
        {self.name}
        +++ Class:{self.job_class} 
        +++ Health:{self.health} 
        +++ Defense:{self.defense} 
        +++ Strength:{self.strength} 
        +++ Agility:{self.agility} 
        +++ Intelligence:{self.intelligence}
        """


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

    # def use_item(self, item: Item) -> None:
    #     setattr(
    #         self,
    #         item.effect.lower(),
    #         getattr(self, item.effect.lower()) + item.value
    #     )

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
