from django.urls import path
from . import views

app_name = 'audit'
urlpatterns = [
    path('', views.audit_trail, name='trail'),
    path('patient/<int:patient_id>/', views.patient_audit_trail, name='patient_trail'),
    path('module/<str:module_name>/', views.module_audit_trail, name='module_trail'),
]
