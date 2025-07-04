from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="server_status"),
    path('create/', views.create_habit, name='create_habit'),
    path('remove/', views.remove_habit, name='remove_habit'),
    path('edit/', views.edit_habit, name='edit_habit'),
    path('done/', views.mark_as_done, name='mark_as_done'),
    path('stats/', views.get_habit_stats, name='get_habit_stats'),
    path('all/', views.get_all_habits),
]
