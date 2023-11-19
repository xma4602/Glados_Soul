import uuid
from dataclasses import dataclass


@dataclass
class UserVk:
    user_id: uuid
    vk_id: str
