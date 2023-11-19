import uuid
from dataclasses import dataclass


@dataclass
class Nickname:
    creator_id: uuid
    called_id: uuid
    nickname: str

