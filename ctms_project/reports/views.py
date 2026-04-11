import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from patients.models import Patient, TRIAL_CHOICES, STATUS_CHOICES, GENDER_CHOICES
from visits.models import VisitLog
from labs.models import LabResult
from adverse_events.models import AdverseEvent
from audit.models import AuditLog

# Patient listing — supports server-side filtering via GET params
@login_required
def patient_listing(request):
    patients = Patient.objects.all()
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    trial = request.GET.get('trial', '')
    gender = request.GET.get('gender', '')
    if search:
        from django.db.models import Q
        patients = patients.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(medical_record_number__icontains=search) |
            Q(diagnosis__icontains=search)
        )
    if status:
        patients = patients.filter(status=status)
    if trial:
        patients = patients.filter(trial_assignment=trial)
    if gender:
        patients = patients.filter(gender=gender)
    context = {
        'patients': patients,
        'trial_choices': TRIAL_CHOICES,
        'status_choices': STATUS_CHOICES,
        'gender_choices': GENDER_CHOICES,
        'filters': {'search': search, 'status': status, 'trial': trial, 'gender': gender},
    }
    return render(request, 'reports/listing.html', context)

# Patient CSV export — BUG Cat-H: ignores all GET params, exports ALL patients
# BUG Cat-G: no log_action() call — export not audited
PATIENT_EXPORT_FIELDS = [
    'medical_record_number', 'first_name', 'last_name', 'date_of_birth',
    'gender', 'blood_group', 'email', 'phone', 'trial_assignment',
    'enrollment_date', 'status', 'diagnosis', 'weight_kg', 'height_cm', 'created_at'
]
PATIENT_EXPORT_HEADERS = [
    'MRN', 'First Name', 'Last Name', 'Date of Birth', 'Gender',
    'Blood Group', 'Email', 'Phone', 'Trial', 'Enrollment Date',
    'Status', 'Diagnosis', 'Weight (kg)', 'Height (cm)', 'Created At'
]

@login_required
def export_patients_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="patients_export.csv"'
    writer = csv.writer(response)
    writer.writerow(PATIENT_EXPORT_HEADERS)
    # BUG Cat-H: Fetches ALL patients — ignores any GET params (search/filter)
    patients = Patient.objects.all()
    for p in patients:
        writer.writerow([getattr(p, f) for f in PATIENT_EXPORT_FIELDS])
    # BUG Cat-G: No log_action() call here — export is not audited
    return response

@login_required
def export_visits_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="visits_export.csv"'
    writer = csv.writer(response)
    writer.writerow(['Patient MRN', 'Patient Name', 'Visit Number', 'Visit Date', 'Visit Type',
                     'Investigator Name', 'Systolic BP', 'Diastolic BP', 'Heart Rate',
                     'Body Temperature', 'Oxygen Saturation', 'Protocol Deviation',
                     'Next Visit Date', 'Created At'])
    # BUG Cat-H: exports ALL visits regardless of filter
    for v in VisitLog.objects.select_related('patient').all():
        writer.writerow([
            v.patient.medical_record_number,
            f"{v.patient.first_name} {v.patient.last_name}",
            v.visit_number, v.visit_date, v.visit_type, v.investigator_name,
            v.systolic_bp, v.diastolic_bp, v.heart_rate, v.body_temperature,
            v.oxygen_saturation, v.protocol_deviation, v.next_visit_date, v.created_at
        ])
    return response

@login_required
def export_labs_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="labs_export.csv"'
    writer = csv.writer(response)
    writer.writerow(['Patient MRN', 'Patient Name', 'Sample Collection Date', 'Sample Type',
                     'Test Name', 'Result Value', 'Unit', 'Reference Range Low',
                     'Reference Range High', 'Abnormal Flag', 'Lab Name', 'Created At'])
    # BUG Cat-H: exports ALL lab results regardless of filter
    for l in LabResult.objects.select_related('patient').all():
        writer.writerow([
            l.patient.medical_record_number,
            f"{l.patient.first_name} {l.patient.last_name}",
            l.sample_collection_date, l.sample_type, l.test_name, l.result_value,
            l.unit, l.reference_range_low, l.reference_range_high,
            l.abnormal_flag, l.lab_name, l.created_at
        ])
    return response

@login_required
def export_ae_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="adverse_events_export.csv"'
    writer = csv.writer(response)
    writer.writerow(['Patient MRN', 'Patient Name', 'Event Title', 'Onset Date', 'Resolution Date',
                     'Severity', 'Causality', 'Action Taken', 'Outcome', 'Is SAE',
                     'SAE Report Number', 'Report Date', 'Regulatory Reported', 'Created At'])
    # BUG Cat-H: exports ALL adverse events regardless of filter
    for ae in AdverseEvent.objects.select_related('patient').all():
        writer.writerow([
            ae.patient.medical_record_number,
            f"{ae.patient.first_name} {ae.patient.last_name}",
            ae.event_title, ae.onset_date, ae.resolution_date, ae.severity,
            ae.causality, ae.action_taken, ae.outcome, ae.is_sae,
            ae.sae_report_number, ae.report_date, ae.regulatory_reported, ae.created_at
        ])
    return response

@login_required
def export_audit_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="audit_export.csv"'
    writer = csv.writer(response)
    writer.writerow(['Timestamp', 'User', 'Module', 'Record ID', 'Action', 'Reason', 'IP Address', 'Created At'])
    # Note: This export itself is not logged — irony preserved
    for log in AuditLog.objects.select_related('user').all():
        writer.writerow([
            log.timestamp, log.user.username if log.user else '',
            log.module, log.record_id, log.action, log.reason,
            log.ip_address, log.timestamp
        ])
    return response
