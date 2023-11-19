import uuid
from dataclasses import dataclass


@dataclass
class Group:
    group_id: uuid
    name: str
