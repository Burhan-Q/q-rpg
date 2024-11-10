"""Core components for characters."""

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

