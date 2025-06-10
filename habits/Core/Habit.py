from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Habit:
    habit_id: int
    name: str
    user_id: int
    activity_value_type: str  # 'int' or 'float' atm
    rep_obj_id: Optional[int] = field(default=None, compare=False)
