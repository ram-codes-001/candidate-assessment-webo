from django.urls import path
from . import views

app_name = 'adverse_events'

urlpatterns = [
    path('', views.ae_list, name='list'),
    path('new/', views.ae_create, name='create'),
    path('<int:pk>/', views.ae_detail, name='detail'),
    path('<int:pk>/edit/', views.ae_edit, name='edit'),
    path('<int:pk>/delete/', views.ae_delete, name='delete'),
]
