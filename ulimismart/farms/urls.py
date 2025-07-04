from django.urls import path
from . import views

app_name = 'farms'

urlpatterns = [
    path('', views.farm_list, name='list'),
    path('create/', views.farm_create, name='create'),
    path('<int:pk>/', views.farm_detail, name='detail'),
    path('<int:pk>/update/', views.farm_update, name='update'),
    path('<int:pk>/delete/', views.farm_delete, name='delete'),
    path('<int:pk>/crops/', views.crop_list, name='crop_list'),
    path('<int:pk>/crops/create/', views.crop_create, name='crop_create'),
    path('crops/<int:pk>/update/', views.crop_update, name='crop_update'),
    path('crops/<int:pk>/delete/', views.crop_delete, name='crop_delete'),
]