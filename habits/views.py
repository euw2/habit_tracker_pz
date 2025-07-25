from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import date, datetime
from collections import defaultdict

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
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    try:
        print("RAW body:", request.body)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        print("Parsed JSON:", data)

        name = data.get('name')
        user_id = data.get('user_id')
        activity_value_type = data.get('activity_value_type')
        target_days = data.get('target_days')

        missing = []
        if not name:
            missing.append("name")
        if user_id is None:
            missing.append("user_id")
        if not activity_value_type:
            missing.append("activity_value_type")

        if missing:
            return JsonResponse({'error': f"Missing fields: {', '.join(missing)}"}, status=400)

        try:
            user_id = int(user_id)
        except ValueError:
            return JsonResponse({'error': 'user_id must be an integer'}, status=400)

        if target_days is not None:
            try:
                target_days = int(target_days)
            except ValueError:
                return JsonResponse({'error': 'target_days must be an integer or null'}, status=400)

        habit = habit_service.create_habit(
            name=name,
            user_id=user_id,
            activity_value_type=activity_value_type,
            target_days=target_days
        )

        return JsonResponse({
            'habit_id': habit.habit_id,
            'name': habit.name,
            'user_id': habit.user_id,
            'activity_value_type': habit.activity_value_type
        }, status=201)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def remove_habit(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    habit_id = data.get('habit_id')

    if habit_id is None:
        return JsonResponse({'error': 'Missing habit_id'}, status=400)

    try:
        habit_id = int(habit_id)
    except ValueError:
        return JsonResponse({'error': 'habit_id must be an integer'}, status=400)

    try:
        habit_service.get_habit(habit_id)
        habit_service.remove_habit(habit_id)
        return JsonResponse({'status': 'deleted'}, status=200)

    except NoSuchElementException:
        return JsonResponse({'error': f'Habit with id {habit_id} not found'}, status=404)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def edit_habit(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    required_fields = ["habit_id", "name", "user_id", "activity_value_type"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return JsonResponse({"error": f"Missing fields: {', '.join(missing)}"}, status=400)

    try:
        habit_id = int(data["habit_id"])
        user_id = int(data["user_id"])
        name = data["name"]
        activity_value_type = data["activity_value_type"]
        target_days = data.get("target_days")  # 🔹 Nowe pole (opcjonalne)

        if target_days is not None:
            try:
                target_days = int(target_days)
            except ValueError:
                return JsonResponse({"error": "target_days must be an integer or null"}, status=400)

        habit_service.get_habit(habit_id)
        habit_service.edit_habit(habit_id, name, user_id, activity_value_type, target_days)

        return JsonResponse({"status": "success", "message": "Habit edited successfully"}, status=200)

    except NoSuchElementException:
        return JsonResponse({"error": f"Habit with id {data['habit_id']} not found"}, status=404)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def mark_as_done(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    habit_id = data.get('habit_id')
    timestamp_str = data.get('timestamp')
    value = data.get('value')

    if habit_id is None or value is None:
        return JsonResponse({'error': 'habit_id and value are required'}, status=400)

    try:
        habit_id = int(habit_id)
        habit = habit_service.get_habit(habit_id)

        if habit.activity_value_type == "int":
            value = int(value)
        elif habit.activity_value_type == "float":
            value = float(value)
        else:
            return JsonResponse({'error': 'Unsupported activity_value_type'}, status=400)

        timestamp = (
            datetime.strptime(timestamp_str, "%Y-%m-%d").date()
            if timestamp_str else date.today()
        )

        existing = habit_service.get_activity_range(habit_id, timestamp, timestamp)
        if existing:
            return JsonResponse({'error': 'Activity already recorded for this date'}, status=400)

        activity = habit_service.register_activity(habit_id, timestamp, value)

        completed = habit_service.is_habit_completed(habit_id)

        return JsonResponse({
            'habit_id': activity.habit_id,
            'date': str(activity.activity_date),
            'completed': completed
        }, status=201)

    except NoSuchElementException:
        return JsonResponse({'error': f'Habit with id {habit_id} not found'}, status=404)

    except (ValueError, TypeError) as e:
        return JsonResponse({'error': f'Invalid data: {str(e)}'}, status=400)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)



@csrf_exempt
def get_all_habits(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET allowed'}, status=405)

    try:
        habits = habit_service._habit_repository.get_all()

        if not habits:
            return JsonResponse({'habits': []}, status=200)

        habit_list = []
        for habit in habits:
            try:
                habit_list.append({
                    'habit_id': habit.habit_id,
                    'name': habit.name,
                    'user_id': habit.user_id,
                    'activity_value_type': habit.activity_value_type
                })
            except Exception as e:
                print("ERROR PARSING HABIT:", habit, e)

        return JsonResponse({'habits': habit_list}, status=200)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def get_habit_stats(request):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET method allowed"}, status=405)

    try:
        habit_id = int(request.GET.get("habit_id"))
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")

        from_date = datetime.strptime(from_date, "%Y-%m-%d").date() if from_date else None
        to_date = datetime.strptime(to_date, "%Y-%m-%d").date() if to_date else None

        all_activities = habit_service._activity_repository.get_all()
        filtered = [
            a for a in all_activities
            if a.habit_id == habit_id and
               (from_date is None or a.activity_date >= from_date) and
               (to_date is None or a.activity_date <= to_date)
        ]

        weekly_freq = defaultdict(int)
        for a in filtered:
            iso_year, iso_week, _ = a.activity_date.isocalendar()
            weekly_freq[f"{iso_year}-W{iso_week:02}"] += 1

        return JsonResponse({
            "habit_id": habit_id,
            "activity_count": len(filtered),
            "weekly_frequency": weekly_freq,
            "activity_dates": [str(a.activity_date) for a in filtered]
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)

# endpoint for testing server status
def index(request):
    return JsonResponse({"status": "success", "server_status": "running"})
