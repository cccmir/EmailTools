from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class ItemType(Enum):
    Email = 1
    APPOINTMET = 2


@dataclass
class Configuration:
    sender: str = ""
    password: str = ""
    to: str = ""
    cc: str = ""
    bcc: str = ""
    optional: str = ""
    required: str = ""
    count: int = 1
    itemType: ItemType = 1

    def __init__(self, d:dict):
        self.__dict__ = d
        if not isinstance(self.itemType, int):
            raise ValueError('itemType must be intenger with value 1 or 2')
        self.__dict__ ['itemType'] = ItemType(self.__dict__ ['itemType'] )



