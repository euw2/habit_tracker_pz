from abc import ABC, abstractmethod
from django.core.exceptions import ObjectDoesNotExist

from ..models import Habit, User, Activity
import Habit as CoreHabit
import HabitActivity as CoreActivity


class RepositoryException(BaseException):
    ...


class NoSuchElementException(BaseException):
    ...


class BaseRepository(ABC):

    @abstractmethod
    def create(self, *args, **kwargs):
        """
        Construct, save and return object.

        RepositoryException is raised if creation or saving operation fails.

        :param args:
        :param kwargs:
        :return: Constructed object
        """

    @abstractmethod
    def remove(self, object_id) -> bool:
        """
        Remove object associated with given id.

        If remove operation fails for some other reason RepositoryException is raised.

        :param object_id:
        :return: True object was removed, false otherwise
        """

    @abstractmethod
    def get_all(self):
        """
        Returns all objects stored in the repository.

        If operation fails the RepositoryException is raised.

        :return:
        """

    @abstractmethod
    def get_by_id(self, object_id):
        """
        Return object associated with given id.

        If object is not found, None is returned
        If operation fails the RepositoryException is raised.

        :param object_id:
        :return:
        """

    @abstractmethod
    def update(self, object_: any):
        """
        Updates specified object in the repository.

        If operation fails the RepositoryException is raised.
        :param object_:
        :return:
        """


class MemoryRepository(BaseRepository):
    """
        Quick, in memory implementation.
    """

    def __init__(self, object_factory, id_seq=1):
        """

        :param object_factory:
            A callback that accepts a bunch of arguments and constructs
            object to be stored in database. Callback should accept
            the following keyword argument: 'rep_obj_id' to capture generated
            object id.
        :param id_seq:
        """
        self._seq = id_seq
        self._object_factory = object_factory
        self._objects = {}

    def _generate_id(self) -> int:
        result = self._seq
        self._seq = self._seq + 1
        return result

    def create(self, *args, **kwargs):
        object_id = self._generate_id()
        kwargs = {**kwargs, "rep_obj_id": object_id}  # add generated id to object factory call arguments
        self._objects[object_id] = self._object_factory(*args, **kwargs)
        obj = self._objects[object_id]
        setattr(obj, "rep_obj_id", object_id)
        return obj

    def remove(self, object_id):
        self._objects.pop(object_id)

    def get_all(self):
        return self._objects.values()

    def get_by_id(self, object_id):
        return self._objects.get(object_id)

    def update(self, object_: any):
        rep_obj_id = getattr(object_, "rep_obj_id", None)

        if rep_obj_id is not None:
            self._objects[rep_obj_id] = object_
        else:
            raise RepositoryException


class ModelBasedHabitRepository(BaseRepository):

    @staticmethod
    def _domain_object_from_model(model: Habit) -> CoreHabit.Habit:
        return CoreHabit.Habit(model.pk, model.name, model.user.primary_key, model.activity_value_type, None)

    @staticmethod
    def _fetch_user(user_id: int):
        try:
            user = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            raise RepositoryException
        return user

    @staticmethod
    def _model_from_domain_object(habit: CoreHabit.Habit) -> CoreHabit.Habit:
        return Habit(
            name=habit.name,
            description="",
            activity_value_type=habit.activity_value_type,
            user=ModelBasedHabitRepository._fetch_user(habit.user_id)
        )

    def create(self, *args, **kwargs):
        user_id = kwargs["user_id"]
        user = self._fetch_user(user_id)

        name = kwargs.get("name", "New Habit")
        value_type = kwargs.get("activity_value_type", "int")
        result = Habit(name=name, user=user, activity_value_type=value_type)
        result.full_clean()
        result.save()
        return self._domain_object_from_model(result)

    def remove(self, object_id) -> bool:
        return Habit.objects.filter(pk=object_id).delete()[0] > 0

    def get_all(self):
        return [self._domain_object_from_model(model) for model in Habit.objects.all()]

    def get_by_id(self, object_id):
        result = Habit.objects.get(pk=object_id)
        return self._domain_object_from_model(result)

    def update(self, object_: CoreHabit.Habit):
        mod: Habit = Habit.objects.get(pk=object_.habit_id)
        mod.name = object_.name

        """
            W tym momencie, kiedy użytkownik chce zmienić typ aktywności, możemy zrobić 
            jedną z tym rzeczy:
            1) Wywalić błąd
            2) Usunąć poprzednie aktywności
            3) Przekonwertować aktywności do nowego typu.
        """
        if mod.activity_value_type != object_.activity_value_type:
            raise ValueError("Can't change activity value type")

        mod.user = self._fetch_user(object_.user_id)
        mod.full_clean()
        mod.save()


class ModelBasedActivityRepository(BaseRepository):

    @staticmethod
    def _domain_object_from_model(model: Activity) -> CoreActivity.HabitActivity:
        return CoreActivity.HabitActivity(model.pk, model.habit.primary_key, model.date)

    @staticmethod
    def _fetch_habit(habit_id: int):
        try:
            habit = Habit.objects.get(pk=habit_id)
        except ObjectDoesNotExist:
            raise RepositoryException
        return habit

    @staticmethod
    def _model_from_domain_object(activity: CoreActivity.HabitActivity) -> Activity:
        habit = ModelBasedActivityRepository._fetch_habit(activity.habit_id)
        result = Activity(
            value_type=habit.activity_value_type,
            date=activity.activity_date
        )
        result.value = activity.value
        return result

    def create(self, *args, **kwargs):
        habit_id = kwargs["habit_id"]
        date = kwargs.get("date_")
        value = kwargs.get("value")
        result = CoreActivity.HabitActivity(0, habit_id, date, value)
        model = self._model_from_domain_object(result)
        model.full_clean()
        model.save()
        return result

    def remove(self, object_id) -> bool:
        return Activity.objects.filter(pk=object_id).delete()[0] > 0

    def get_all(self):
        return [self._domain_object_from_model(model) for model in Activity.objects.all()]

    def get_by_id(self, object_id):
        result = Activity.objects.get(pk=object_id)
        return self._domain_object_from_model(result)

    def update(self, object_: CoreActivity.HabitActivity):
        model: Activity = Activity.objects.get(pk=object_.id)
        model.date = object_.activity_date
        model.value = object_.value
        model.habit = self._fetch_habit(object_.habit_id)
