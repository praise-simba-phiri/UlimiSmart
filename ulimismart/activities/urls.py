from django.urls import path
from . import views

app_name = 'activities'

urlpatterns = [
    path('', views.activity_list, name='list'),
    path('create/', views.activity_create, name='create'),
    path('<int:pk>/', views.activity_detail, name='detail'),
    path('<int:pk>/update/', views.activity_update, name='update'),
    path('<int:pk>/delete/', views.activity_delete, name='delete'),
    path('farm/<int:farm_id>/', views.farm_activities, name='farm_activities'),
]