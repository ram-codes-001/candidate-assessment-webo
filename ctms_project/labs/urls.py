from django.urls import path
from . import views

app_name = 'labs'

urlpatterns = [
    path('', views.lab_list, name='list'),
    path('new/', views.lab_create, name='create'),
    path('<int:pk>/', views.lab_detail, name='detail'),
    path('<int:pk>/edit/', views.lab_edit, name='edit'),
    path('<int:pk>/delete/', views.lab_delete, name='delete'),
]
