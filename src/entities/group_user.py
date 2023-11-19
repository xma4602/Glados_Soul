import uuid
from dataclasses import dataclass


@dataclass
class GroupUser:
    group_id: uuid
    user_id: uuid
