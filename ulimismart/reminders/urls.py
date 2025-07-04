from django.urls import path
from . import views

app_name = 'reminders'

urlpatterns = [
    path('', views.reminder_list, name='list'),
    path('create/', views.reminder_create, name='create'),
    path('<int:pk>/', views.reminder_detail, name='detail'),
    path('<int:pk>/update/', views.reminder_update, name='update'),
    path('<int:pk>/delete/', views.reminder_delete, name='delete'),
    path('<int:pk>/complete/', views.reminder_complete, name='complete'),
    path('upcoming/', views.upcoming_reminders, name='upcoming'),
]