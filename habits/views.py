from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import date, datetime

from habits.Core.HabitService import create_habit_repository, create_activity_repository, HabitService
from habits.Core.Repositories import NoSuchElementException
"""
    habit service     
"""
activity_repository = create_activity_repository()
habit_repository = create_habit_repository()
habit_service = HabitService(activity_repository, habit_repository)

# Create your views here.

@csrf_exempt
def create_habit(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            user_id = data.get('user_id')
            activity_value_type = data.get('activity_value_type')

            if not all([name, user_id, activity_value_type]):
                return JsonResponse({'error': 'Missing fields'}, status=400)

            habit = habit_service.create_habit(name, int(user_id), activity_value_type)

            return JsonResponse({
                'habit_id': habit.habit_id,
                'name': habit.name,
                'user_id': habit.user_id,
                'activity_value_type': habit.activity_value_type
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

@csrf_exempt
def remove_habit(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            habit_id = data.get('habit_id')

            if habit_id is None:
                return JsonResponse({'error': 'habit_id is required'}, status=400)

            habit_service.get_habit(int(habit_id))

            habit_service.remove_habit(int(habit_id))
            return JsonResponse({'status': 'deleted'}, status=200)

        except NoSuchElementException:
            return JsonResponse({'error': 'Habit not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Only POST allowed'}, status=405)

@csrf_exempt
def edit_habit(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)

        habit_id = data.get("habit_id")
        name = data.get("name")
        user_id = data.get("user_id")
        activity_value_type = data.get("activity_value_type")

        if None in (habit_id, name, user_id, activity_value_type):
            return JsonResponse({"status": "error", "message": "Missing required fields"}, status=400)

        habit_service.get_habit(int(habit_id))

        habit_service.edit_habit(int(habit_id), name, int(user_id), activity_value_type)

        return JsonResponse({"status": "success", "message": "Habit edited successfully"})

    except NoSuchElementException:
        return JsonResponse({"status": "error", "message": "Habit not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

@csrf_exempt
def mark_as_done(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            habit_id = data.get('habit_id')
            timestamp_str = data.get('timestamp')

            if not habit_id:
                return JsonResponse({'error': 'habit_id is required'}, status=400)

            habit_service.get_habit(int(habit_id))

            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d").date() if timestamp_str else date.today()

            activity = habit_service.register_activity(int(habit_id), timestamp)

            return JsonResponse({
                'habit_id': activity.habit_id,
                'date': str(activity.activity_date)
            }, status=201)

        except NoSuchElementException:
            return JsonResponse({'error': 'Habit not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Only POST allowed'}, status=405)




@csrf_exempt
def get_all_habits(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET allowed'}, status=405)

    try:
        habits = habit_service._habit_repository.get_all()
        habit_list = [{
            'habit_id': habit.habit_id,
            'name': habit.name,
            'user_id': habit.user_id,
            'activity_value_type': habit.activity_value_type
        } for habit in habits]

        return JsonResponse({'habits': habit_list}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# endpoint for testing server status
def index(request):
    return JsonResponse({"status": "success", "server_status": "running"})
