""" Example script for python 'type hints' """
from typing import List
from typing import Set, Tuple
from typing import Dict
from typing import Optional


class Person:
    """ Person Class """
    def __init__(self, name: str):
        self.name = name


def get_full_name(first_name: str, last_name: str):
    """ Return full name given first and last name"""
    full_name = first_name.title() + " " + last_name.title()
    return full_name


def get_name_with_age(name: str, age: int):
    """Another example with age"""
    name_with_age = name + " is this old" + str(age)
    return name_with_age


def get_items(item_a: str, item_b: int,
              item_c: float, item_d: bool, item_e: bytes):
    """Simple types"""
    return item_a, item_b, item_c, item_d, item_e


def process_items_list(items: List[str]):
    """List with type parameter str"""
    for item in items:
        print(item)


def process_items_tuple_set(items_t: Tuple[int, int, str],
                            items_s: Set[bytes]):
    """Tuple and Set types"""
    return items_t, items_s


def process_items_dict(prices: Dict[str, float]):
    """Dict type example"""
    for item_name, item_price in prices.items():
        print(item_name)
        print(item_price)


def say_hi(name: Optional[str] = None):
    """Example for Optional type"""
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")


def get_person_name(one_person: Person):
    """Class as type return person name"""
    return one_person.name


print(get_full_name("zack", "hemsey"))
