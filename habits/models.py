from django.db import models

# Create your models here.


class User(models.Model):
    # id field is generated automatically
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    email = models.EmailField()
    recovery_code = models.CharField(max_length=20)


class Habit(models.Model):

    SUPPORTED_ACTIVITY_TYPES = {
        "int": "Integer",
        "float": "floating"
    }

    name = models.CharField(max_length=32)
    description = models.TextField(default="Placeholder. Edit habit to set custom description")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_value_type = models.CharField(max_length=8, choices=SUPPORTED_ACTIVITY_TYPES)


class FloatMeasurableActivity(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    value = models.FloatField()
    date = models.DateField()


class CountableActivity(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    value = models.IntegerField()
    date = models.DateField()

