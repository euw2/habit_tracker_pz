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
        "float": "Float"
    }

    name = models.CharField(max_length=32)
    description = models.TextField(default="Placeholder. Edit habit to set custom description")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_value_type = models.CharField(max_length=8, choices=SUPPORTED_ACTIVITY_TYPES)
    target_days = models.IntegerField(null=True, blank=True)


class Activity(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    VALUE_TYPE_CHOICES = [
        ("int", "Integer"),
        ("float", "Float")
    ]
    value_type = models.CharField(max_length=10, choices=VALUE_TYPE_CHOICES)
    int_value = models.IntegerField(null=True, blank=True)
    float_value = models.FloatField(null=True, blank=True)
    date = models.DateField()

    @property
    def value(self):
        match self.value_type:
            case "int":
                return self.int_value
            case "float":
                return self.float_value
        raise ValueError("Unsupported value type")

    @value.setter
    def value(self, v):
        self.int_value = None
        self.float_value = None

        match self.value_type:
            case "int":
                self.int_value = int(v)
            case "float":
                self.float_value = float(v)
            case _:
                raise ValueError("Unsupported value type")