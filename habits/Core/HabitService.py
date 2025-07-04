from habits.Core.Habit import Habit
from habits.Core.HabitActivity import HabitActivity
from habits.Core.Repositories import BaseRepository, ModelBasedActivityRepository, ModelBasedHabitRepository
from datetime import date
from typing import Optional, List, Set


def create_activity_repository():
    return ModelBasedActivityRepository()


def create_habit_repository():
    return ModelBasedHabitRepository()


class HabitService:

    # Any domain specific action should be defined here

    def __init__(self, activity_repository: BaseRepository,
                 habit_repository: BaseRepository):
        self._activity_repository = activity_repository
        self._habit_repository = habit_repository

    def create_habit(self, name: str, user_id: int, activity_value_type: str, target_days: Optional[int] = None):
        return self._habit_repository.create(
            name=name,
            user_id=user_id,
            activity_value_type=activity_value_type,
            target_days=target_days
        )

    def get_habit(self, habit_id: int) -> Habit:
        return self._habit_repository.get_by_id(habit_id)

    def remove_habit(self, habit_id: int):
        self._habit_repository.remove(habit_id)

    def edit_habit(self, habit_id: int, name: str, user_id: int, activity_value_type: str,
                   target_days: Optional[int] = None):
        new_obj = Habit(
            habit_id=habit_id,
            name=name,
            user_id=user_id,
            activity_value_type=activity_value_type,
            rep_obj_id=habit_id
        )
        new_obj.target_days = target_days
        self._habit_repository.update(new_obj)

    def get_activity_range(self, habit_id: int, period_start: date, period_end: date):
        """
        Gets habit activities associated with given habit in specified time period.
        """
        activities: list[HabitActivity] = self._activity_repository.get_all()
        filter_ = lambda a: a.happenedInPeriod(period_start, period_end) and a.habit_id == habit_id
        return [a for a in activities if filter_(a)]

    def register_activity(self, habit_id: int, timestamp: date, value: int | float):
        return self._activity_repository.create(habit_id=habit_id, date_=timestamp, value=value)

    def count_unique_days(self, habit_id: int) -> int:
        activities = self._activity_repository.get_all()
        unique_days: Set[date] = set(
            a.activity_date for a in activities if a.habit_id == habit_id
        )
        return len(unique_days)

    def is_habit_completed(self, habit_id: int) -> bool:
        habit = self._habit_repository.get_by_id(habit_id)

        if habit.target_days is None:
            return False

        completed_days = self.count_unique_days(habit_id)
        return completed_days >= habit.target_days