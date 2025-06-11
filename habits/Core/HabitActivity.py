from dataclasses import dataclass
from datetime import date


@dataclass
class HabitActivity:
    id: int
    habit_id: int
    activity_date: date
    value: any

    def happenedInPeriod(self, period_start: date, period_end: date):
        return period_start <= self.activity_date < period_end
