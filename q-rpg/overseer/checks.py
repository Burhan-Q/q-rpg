"""Checks for characters or actions."""

def total_check(properties:dict[str, int]) -> bool:
    return sum(properties.values()) == 200


def balance_check(properties:dict[str, int]) -> bool:
    return all([0 <= val <= 100 for val in properties.values()])
  
