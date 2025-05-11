
from abc import ABC, abstractmethod
from typing import List


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

    def __init__(self, object_factory, id_seq=0):
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
    