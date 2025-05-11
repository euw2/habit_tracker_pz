from dataclasses import dataclass


@dataclass
class Habit:
    habit_id: int
    name: str
    user_id: int
    activity_value_type: str  # 'int' or 'float'
