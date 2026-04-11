from django.urls import path
from . import views

app_name = 'visits'

urlpatterns = [
    path('', views.visit_list, name='list'),
    path('new/', views.visit_create, name='create'),
    path('<int:pk>/', views.visit_detail, name='detail'),
    path('<int:pk>/edit/', views.visit_edit, name='edit'),
    path('<int:pk>/delete/', views.visit_delete, name='delete'),
]
