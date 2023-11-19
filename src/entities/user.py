import uuid
from dataclasses import dataclass


@dataclass
class User:
    id: uuid
    first_name: str
    second_name: str
    third_name: str
    phone: str
    group_num: str


