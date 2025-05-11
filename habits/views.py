from django.shortcuts import render
from django.http import JsonResponse

from habits.Core.HabitService import create_habit_repository, create_activity_repository, HabitService

"""
    habit service     
"""
activity_repository = create_activity_repository()
habit_repository = create_habit_repository()
habit_service = HabitService(activity_repository, habit_repository)

# Create your views here.


def create_habit(request):
    # TODO: implement
    ...


def remove_habit(request):
    # TODO: implement
    ...


def edit_habit(request):
    # TODO: implement
    ...


def mark_as_done(request):
    # TODO: implement
    ...


# endpoint for testing server status
def index(request):
    return JsonResponse({"status": "success", "server_status": "running"})
