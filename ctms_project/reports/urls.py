from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.patient_listing, name='listing'),
    path('export/patients/', views.export_patients_csv, name='export_patients'),
    path('export/visits/', views.export_visits_csv, name='export_visits'),
    path('export/labs/', views.export_labs_csv, name='export_labs'),
    path('export/adverse-events/', views.export_ae_csv, name='export_ae'),
    path('export/audit/', views.export_audit_csv, name='export_audit'),
]
