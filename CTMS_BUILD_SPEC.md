# Clinical Trial Management System (CTMS)
## Complete Build Specification — Vibe Coding Reference

> **Purpose:** QA Assessment Platform with intentional silent bugs, format bypass vulnerabilities, and audit trail gaps. Built in Django (Python). Designed to look like a production-grade clinical system.

---

## Table of Contents

1. [Tech Stack](#tech-stack)
2. [Project Structure](#project-structure)
3. [Database Models](#database-models)
4. [Bug Manifest](#bug-manifest)
5. [Page 1 — Patient Registration](#page-1--patient-registration)
6. [Page 2 — Visit Log](#page-2--visit-log)
7. [Page 3 — Lab Results](#page-3--lab-results)
8. [Page 4 — Adverse Events](#page-4--adverse-events)
9. [Page 5 — Patient Listing](#page-5--patient-listing)
10. [Audit Trail Module](#audit-trail-module)
11. [Export / Report System](#export--report-system)
12. [Authentication System](#authentication-system)
13. [UI & Design System](#ui--design-system)
14. [Seed Data](#seed-data)
15. [Deployment](#deployment)

---

## Tech Stack

```
Backend:        Django 4.2 (Python 3.11+)
Database:       SQLite (dev) / PostgreSQL (prod)
Frontend:       Bootstrap 5 + AdminLTE 3
Icons:          Font Awesome 6
Date Picker:    Flatpickr (looks polished, still accepts garbage underneath)
Dropdowns:      Select2
Modals:         SweetAlert2 (reason modals)
Tables:         DataTables.js
Notifications:  Toastr.js
Export:         Python csv module (built-in)
Auth:           Django built-in auth + session middleware
```

---

## Project Structure

```
ctms_project/
├── manage.py
├── requirements.txt
├── .env
├── README.md
│
├── ctms/                        # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/                    # Auth module
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── templates/
│       └── accounts/
│           └── login.html
│
├── patients/                    # Page 1 — Patient Registration
│   ├── models.py
│   ├── forms.py                 # ← Bug layer lives here
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── patients/
│           ├── form.html
│           ├── detail.html
│           └── confirm_delete.html
│
├── visits/                      # Page 2 — Visit Log
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── visits/
│           ├── form.html
│           └── detail.html
│
├── labs/                        # Page 3 — Lab Results
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── labs/
│           ├── form.html
│           └── detail.html
│
├── adverse_events/              # Page 4 — Adverse Events
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── adverse_events/
│           ├── form.html
│           └── detail.html
│
├── reports/                     # Page 5 — Listing + Export
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── reports/
│           └── listing.html
│
├── audit/                       # Audit Trail Engine
│   ├── models.py
│   ├── middleware.py
│   ├── mixins.py
│   └── templates/
│       └── audit/
│           └── trail.html
│
├── templates/                   # Global templates
│   ├── base.html
│   ├── sidebar.html
│   ├── navbar.html
│   └── dashboard.html
│
└── static/
    ├── css/
    │   └── ctms.css
    └── js/
        └── ctms.js
```

---

## Database Models

### accounts/models.py

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CTMSUser(AbstractUser):
    ROLE_CHOICES = [('coordinator', 'Coordinator'), ('admin', 'Admin')]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='coordinator')
    employee_id = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
```

---

### patients/models.py

```python
from django.db import models

GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ('U', 'Unknown')]
BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'),
]
STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive'), ('withdrawn', 'Withdrawn')]
TRIAL_CHOICES = [
    ('TRIAL-001', 'Phase II Cardiology Study'),
    ('TRIAL-002', 'Oncology Immunotherapy Trial'),
    ('TRIAL-003', 'Diabetes Management Protocol'),
    ('TRIAL-004', 'Neurological Disorder Study'),
]

class Patient(models.Model):
    # Identity
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.CharField(max_length=50)           # BUG: should be DateField
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    medical_record_number = models.CharField(max_length=50)   # BUG: no format validation
    national_id = models.CharField(max_length=50)             # BUG: accepts short values

    # Contact
    email = models.CharField(max_length=200)                  # BUG: CharField not EmailField
    phone = models.CharField(max_length=50)                   # BUG: accepts alphabets
    address = models.TextField(blank=True)

    # Medical
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    weight_kg = models.CharField(max_length=20)               # BUG: should be DecimalField
    height_cm = models.CharField(max_length=20)               # BUG: should be DecimalField
    diagnosis = models.TextField()

    # Trial
    trial_assignment = models.CharField(max_length=50, choices=TRIAL_CHOICES)
    enrollment_date = models.CharField(max_length=50)         # BUG: should be DateField
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    # Emergency Contact — not shown as required in UI, but backend requires them
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=50)

    # Consent — shown as required in UI (*), but backend saves without it
    consent_signed = models.BooleanField(default=False)       # BUG: not enforced

    # Meta
    created_by = models.ForeignKey(
        'accounts.CTMSUser', on_delete=models.SET_NULL, null=True,
        related_name='patients_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.medical_record_number})"

    class Meta:
        ordering = ['-created_at']
```

---

### visits/models.py

```python
from django.db import models

VISIT_TYPE_CHOICES = [
    ('screening', 'Screening'),
    ('baseline', 'Baseline'),
    ('followup', 'Follow-up'),
    ('final', 'Final Visit'),
    ('unscheduled', 'Unscheduled'),
]

class VisitLog(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='visits')
    visit_number = models.CharField(max_length=20)           # BUG: accepts V@#! (no regex)
    visit_date = models.CharField(max_length=50)             # BUG: should be DateField
    visit_type = models.CharField(max_length=20, choices=VISIT_TYPE_CHOICES)
    investigator_name = models.CharField(max_length=100)
    coordinator = models.ForeignKey(
        'accounts.CTMSUser', on_delete=models.SET_NULL, null=True, related_name='visits'
    )

    # Vitals — all CharField, should be numeric
    systolic_bp = models.CharField(max_length=20)            # BUG: accepts "normal"
    diastolic_bp = models.CharField(max_length=20)           # BUG: accepts "low"
    heart_rate = models.CharField(max_length=20)             # BUG: accepts "fast"
    body_temperature = models.CharField(max_length=20)       # BUG: accepts "warm"
    oxygen_saturation = models.CharField(max_length=20)      # BUG: accepts "good"

    visit_notes = models.TextField(blank=True)
    next_visit_date = models.CharField(max_length=50, blank=True)  # BUG: can be before visit_date

    # Protocol Deviation
    protocol_deviation = models.BooleanField(default=False)
    deviation_notes = models.TextField(blank=True)           # BUG: Required in UI if deviation=True, saves without

    created_by = models.ForeignKey(
        'accounts.CTMSUser', on_delete=models.SET_NULL, null=True, related_name='visits_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient} — {self.visit_number} ({self.visit_date})"

    class Meta:
        ordering = ['-created_at']
```

---

### labs/models.py

```python
from django.db import models

SAMPLE_TYPE_CHOICES = [('blood', 'Blood'), ('urine', 'Urine'), ('tissue', 'Tissue'), ('csf', 'CSF')]
ABNORMAL_FLAG_CHOICES = [('normal', 'Normal'), ('abnormal', 'Abnormal'), ('critical', 'Critical')]

class LabResult(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='lab_results')
    visit = models.ForeignKey('visits.VisitLog', on_delete=models.SET_NULL, null=True, blank=True, related_name='lab_results')

    sample_collection_date = models.CharField(max_length=50)  # BUG: accepts "00/00/0000"
    sample_type = models.CharField(max_length=20, choices=SAMPLE_TYPE_CHOICES)
    test_name = models.CharField(max_length=200)

    result_value = models.CharField(max_length=100)           # BUG: accepts "positive" for numeric test
    unit = models.CharField(max_length=50)                    # BUG: free text, should be dropdown
    reference_range_low = models.CharField(max_length=50)     # BUG: accepts alphabets
    reference_range_high = models.CharField(max_length=50)    # BUG: accepts alphabets

    abnormal_flag = models.CharField(max_length=20, choices=ABNORMAL_FLAG_CHOICES, default='normal')
    lab_technician = models.CharField(max_length=100)
    lab_name = models.CharField(max_length=200)
    remarks = models.TextField(blank=True)                    # BUG: if flag=Critical, should require remarks but doesn't

    created_by = models.ForeignKey(
        'accounts.CTMSUser', on_delete=models.SET_NULL, null=True, related_name='labs_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient} — {self.test_name} ({self.sample_collection_date})"

    class Meta:
        ordering = ['-created_at']
```

---

### adverse_events/models.py

```python
from django.db import models

SEVERITY_CHOICES = [
    ('mild', 'Mild'),
    ('moderate', 'Moderate'),
    ('severe', 'Severe'),
    ('life_threatening', 'Life-Threatening'),
]
CAUSALITY_CHOICES = [
    ('related', 'Related'),
    ('unrelated', 'Unrelated'),
    ('possible', 'Possible'),
    ('probable', 'Probable'),
]
ACTION_CHOICES = [
    ('none', 'None'),
    ('dose_reduced', 'Dose Reduced'),
    ('drug_stopped', 'Drug Stopped'),
    ('hospitalized', 'Hospitalized'),
]
OUTCOME_CHOICES = [
    ('recovered', 'Recovered'),
    ('recovering', 'Recovering'),
    ('ongoing', 'Ongoing'),
    ('fatal', 'Fatal'),
    ('unknown', 'Unknown'),
]

class AdverseEvent(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='adverse_events')
    event_title = models.CharField(max_length=200)
    onset_date = models.CharField(max_length=50)             # BUG: accepts garbage
    resolution_date = models.CharField(max_length=50, blank=True)  # BUG: can be before onset_date
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    causality = models.CharField(max_length=20, choices=CAUSALITY_CHOICES)
    event_description = models.TextField(blank=True)         # BUG: Required in UI, saves without

    action_taken = models.CharField(max_length=20, choices=ACTION_CHOICES)
    outcome = models.CharField(max_length=20, choices=OUTCOME_CHOICES)

    is_sae = models.BooleanField(default=False)              # Serious Adverse Event
    sae_report_number = models.CharField(max_length=50, blank=True)  # BUG: Required if SAE=True in UI, saves without

    reported_by = models.CharField(max_length=100)
    report_date = models.CharField(max_length=50)            # BUG: accepts future dates
    regulatory_reported = models.BooleanField(default=False)

    attachment = models.FileField(upload_to='ae_attachments/', blank=True, null=True)
    # BUG: No file type validation — accepts .exe, .js, .bat

    created_by = models.ForeignKey(
        'accounts.CTMSUser', on_delete=models.SET_NULL, null=True, related_name='ae_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient} — {self.event_title}"

    class Meta:
        ordering = ['-created_at']
```

---

### audit/models.py

```python
from django.db import models

ACTION_CHOICES = [
    ('CREATE', 'Create'),
    ('UPDATE', 'Update'),
    ('DELETE', 'Delete'),
    ('LOGIN', 'Login'),
    ('LOGOUT', 'Logout'),
    ('EXPORT', 'Export'),
]

class AuditLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        'accounts.CTMSUser', on_delete=models.SET_NULL,
        null=True, related_name='audit_logs'
    )
    module = models.CharField(max_length=50)           # patients / visits / labs / adverse_events
    record_id = models.IntegerField(null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    reason = models.TextField(blank=True)              # Populated from reason modal on UPDATE/DELETE
    changed_fields = models.JSONField(default=dict)    # {"field": {"old": x, "new": y}}
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)

    # BUG (intentional): Status change on Patient does NOT create an AuditLog entry
    # All other updates do. This gap should be caught by thorough exploratory testing.

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.timestamp}] {self.user} — {self.action} on {self.module}#{self.record_id}"
```

---

## Bug Manifest

> This is the **master reference** for all intentional bugs. Keep this document private — give candidates only the system URL and credentials.

### Category A — UI Shows Required (*), Backend Does NOT Enforce

| Module | Field | Expected Behavior | Bug |
|--------|-------|-------------------|-----|
| Patient | Consent Signed | Must be True to save | `required=False` in form |
| Patient | Diagnosis | Required field | Backend `blank=True` |
| Visit | Deviation Notes | Required when Protocol Deviation = Yes | No cross-field validation |
| Adverse Event | Event Description | Required | `blank=True` in model |
| Adverse Event | SAE Report Number | Required when SAE = True | No conditional validation |

### Category B — UI Shows NO Required Indicator, Backend Rejects

| Module | Field | Bug |
|--------|-------|-----|
| Patient | Emergency Contact Name | Django raises ValidationError but no `*` shown in UI |
| Patient | Emergency Contact Phone | Same — error only appears after submit |

**Implementation:**
```python
# patients/forms.py
def clean_emergency_contact_name(self):
    val = self.cleaned_data.get('emergency_contact_name')
    if not val:
        raise forms.ValidationError("Emergency contact name is required.")
    return val
# No asterisk (*) on this label in the template
```

### Category C — Date Fields Accept Any String (Garbage Input)

| Module | Field | Bug |
|--------|-------|-----|
| Patient | Date of Birth | CharField, accepts "32/13/2099", "abc", "yesterday" |
| Patient | Enrollment Date | CharField, accepts "N/A", "TBD" |
| Visit | Visit Date | CharField, accepts "99/99/9999" |
| Visit | Next Visit Date | CharField, no validation that it's after Visit Date |
| Lab | Sample Collection Date | CharField, accepts "00/00/0000" |
| Adverse Event | Onset Date | CharField, accepts "last week" |
| Adverse Event | Report Date | CharField, accepts future dates |
| Adverse Event | Resolution Date | CharField, can be before Onset Date |

**Implementation for all date fields:**
```python
# Use CharField in model instead of DateField
# Use Flatpickr date picker widget in template (looks like proper date picker)
# But underlying field is text — Flatpickr can be bypassed by typing directly
onset_date = models.CharField(max_length=50)  # No DateField validators
```

### Category D — Numeric Fields as Plain Textboxes

| Module | Field | Should Be | Bug |
|--------|-------|-----------|-----|
| Patient | Weight (kg) | DecimalField, min=1, max=500 | CharField, accepts "heavy", "N/A" |
| Patient | Height (cm) | DecimalField, min=50, max=250 | CharField, accepts "tall" |
| Visit | Systolic BP | IntegerField, range 60–250 | CharField, accepts "normal" |
| Visit | Diastolic BP | IntegerField, range 40–150 | CharField, accepts "low" |
| Visit | Heart Rate | IntegerField, range 30–250 | CharField, accepts "fast" |
| Visit | Body Temperature | DecimalField, range 35–42 | CharField, accepts "warm" |
| Visit | Oxygen Saturation | IntegerField, range 70–100 | CharField, accepts "good" |
| Lab | Result Value | DecimalField | CharField, accepts "positive" |
| Lab | Reference Range Low | DecimalField | CharField, accepts "low" |
| Lab | Reference Range High | DecimalField | CharField, accepts "high" |

**Implementation:**
```python
# All fields defined as CharField in models
# No widget type="number" in templates
# No MinValueValidator / MaxValueValidator
weight_kg = models.CharField(max_length=20)
# Template renders: <input type="text" name="weight_kg" placeholder="e.g. 72.5">
```

### Category E — Format Validation Bypasses (Hint in UI, No Backend Validation)

| Module | Field | Placeholder/Hint Shown | What Backend Actually Accepts |
|--------|-------|------------------------|-------------------------------|
| Patient | Medical Record Number | "Format: MRN-000000" | Any string including "ABC", "1" |
| Patient | National ID | "10-12 digit ID" | Any 1+ character string |
| Patient | Email | Shows email-style input, but type="text" | "xyz@@", "notanemail" |
| Patient | Phone | "10-digit number" | Alphabets, symbols |
| Visit | Visit Number | "Format: V-001" | "V@#!", "VISIT!!!" |

**Implementation:**
```python
# patients/forms.py
medical_record_number = forms.CharField(
    widget=forms.TextInput(attrs={
        'placeholder': 'Format: MRN-000000',
        'class': 'form-control'
    })
    # BUG: No validators=[RegexValidator(r'^MRN-\d{6}$')]
)
```

### Category F — Logic / Cross-field Validation Missing

| Bug | Description |
|-----|-------------|
| Date order | Resolution Date can be before Onset Date — no comparison in `clean()` |
| Next Visit | Can be before Visit Date |
| SAE conditional | SAE Report Number not enforced when `is_sae = True` |
| Deviation conditional | Deviation Notes not enforced when `protocol_deviation = True` |
| Critical without remarks | Lab result with Abnormal Flag = "Critical" saves with empty Remarks |

### Category G — Audit Trail Gaps (Subtle)

| Gap | Description |
|-----|-------------|
| Status change | Changing Patient status (Active→Withdrawn) does NOT create AuditLog entry |
| Export | CSV export action is NOT logged in audit trail |
| Login failure | Failed login attempts are NOT logged |

### Category H — Export Bug

| Bug | Description |
|-----|-------------|
| Filter ignored | Export to CSV exports ALL records regardless of active search/filter |
| Page ignored | Exports all pages, not just current page — no UI indication of this |

---

## Page 1 — Patient Registration

### Form Fields

```
SECTION: Personal Information
─────────────────────────────
Field: First Name
  Type: TextInput
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

Field: Last Name
  Type: TextInput
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

Field: Date of Birth
  Type: TextInput + Flatpickr (cosmetic only)
  Placeholder: "DD/MM/YYYY"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: CharField — accepts "32/13/2099", "abc", blank with JS disabled

Field: Gender
  Type: Select (Male / Female / Other / Unknown)
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

Field: Medical Record Number
  Type: TextInput
  Placeholder: "Format: MRN-000000"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: No regex validation — accepts "ABC", "1", "MRN-@#"

Field: National ID
  Type: TextInput
  Placeholder: "Enter 10–12 digit national ID"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: No length/format validation — accepts any string

SECTION: Contact Information
─────────────────────────────
Field: Email Address
  Type: TextInput (NOT type="email")
  Required UI: Yes (*)
  Required Backend: No (blank=True in form)
  Bug: Accepts "xyz@@", "notanemail", "hello world"

Field: Phone Number
  Type: TextInput
  Placeholder: "10-digit phone number"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: Accepts "abc", "+++", "call me"

Field: Address
  Type: Textarea
  Required UI: No
  Required Backend: No
  Bug: None

SECTION: Emergency Contact (no asterisk shown, no hint that it's required)
─────────────────────────────────────────────────────────────────────────────
Field: Emergency Contact Name
  Type: TextInput
  Required UI: No (no asterisk, no label hint)
  Required Backend: YES — raises ValidationError on save
  Bug: Mismatch — user sees no indication this is required

Field: Emergency Contact Phone
  Type: TextInput
  Required UI: No (no asterisk)
  Required Backend: YES — raises ValidationError on save
  Bug: Same mismatch — also accepts alphabets when provided

SECTION: Medical Information
─────────────────────────────
Field: Blood Group
  Type: Select (A+, A-, B+, B-, AB+, AB-, O+, O-)
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

Field: Weight (kg)
  Type: TextInput (plain text, no type="number")
  Placeholder: "e.g. 72.5"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: CharField — accepts "heavy", "obese", "N/A", "??"

Field: Height (cm)
  Type: TextInput (plain text)
  Placeholder: "e.g. 170"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: CharField — accepts "tall", "short", "5 feet"

Field: Diagnosis / Primary Condition
  Type: Textarea
  Placeholder: "Describe primary diagnosis"
  Required UI: Yes (*)
  Required Backend: No (backend allows blank)
  Bug: UI asterisk misleads — saves without it

SECTION: Trial Information
───────────────────────────
Field: Trial Assignment
  Type: Select (4 trial options)
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

Field: Enrollment Date
  Type: TextInput + Flatpickr (cosmetic)
  Placeholder: "DD/MM/YYYY"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: CharField — accepts "TBD", "next month", "00/00/0000"

Field: Patient Status
  Type: Select (Active / Inactive / Withdrawn)
  Required UI: Yes (*)
  Required Backend: Yes (default: Active)
  Bug: Status change does NOT create AuditLog entry (audit gap)

SECTION: Consent
──────────────────
Field: Consent Form Signed
  Type: Checkbox
  Label: "I confirm the patient has signed the informed consent form *"
  Required UI: Yes (asterisk shown, looks mandatory)
  Required Backend: No — BooleanField(required=False)
  Bug: Can be left unchecked and record saves successfully
```

### Views (patients/views.py)

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Patient
from .forms import PatientForm
from audit.mixins import log_action

@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.created_by = request.user
            patient.save()
            log_action(request, 'patients', patient.id, 'CREATE', {})
            messages.success(request, 'Patient registered successfully.')
            return redirect('patients:detail', pk=patient.pk)
    else:
        form = PatientForm()
    return render(request, 'patients/form.html', {'form': form, 'title': 'Register New Patient'})

@login_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('edit_reason', '')
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            old_data = {f: getattr(patient, f) for f in form.changed_data}
            form.save()
            new_data = {f: getattr(patient, f) for f in form.changed_data}
            changed = {f: {'old': old_data[f], 'new': new_data[f]} for f in form.changed_data}
            # BUG: if only 'status' was changed, log_action is still called here
            # but inside log_action, status-only changes are silently skipped
            log_action(request, 'patients', patient.id, 'UPDATE', changed, reason=reason)
            messages.success(request, 'Patient updated.')
            return redirect('patients:detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/form.html', {'form': form, 'patient': patient, 'title': 'Edit Patient'})

@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('delete_reason', '')
        log_action(request, 'patients', patient.id, 'DELETE', {}, reason=reason)
        patient.delete()
        messages.success(request, 'Patient record deleted.')
        return redirect('reports:listing')
    return render(request, 'patients/confirm_delete.html', {'patient': patient})
```

### Forms (patients/forms.py)

```python
from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['created_by', 'created_at', 'updated_at']
        widgets = {
            'date_of_birth': forms.TextInput(attrs={
                'class': 'form-control flatpickr-date',
                'placeholder': 'DD/MM/YYYY',
                'autocomplete': 'off'
            }),
            'enrollment_date': forms.TextInput(attrs={
                'class': 'form-control flatpickr-date',
                'placeholder': 'DD/MM/YYYY',
            }),
            'weight_kg': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 72.5'
                # BUG: type="text", not type="number"
            }),
            'height_cm': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 170'
            }),
            'medical_record_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Format: MRN-000000'
                # BUG: No RegexValidator
            }),
            'national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 10–12 digit national ID'
                # BUG: No length validator
            }),
            'email': forms.TextInput(attrs={   # BUG: TextInput not EmailInput
                'class': 'form-control',
                'placeholder': 'patient@example.com'
            }),
            'consent_signed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    # BUG: consent_signed not required
    consent_signed = forms.BooleanField(required=False)

    # BUG: These fields have no asterisk in template but raise errors
    def clean_emergency_contact_name(self):
        val = self.cleaned_data.get('emergency_contact_name')
        if not val or val.strip() == '':
            raise forms.ValidationError("Emergency contact name is required.")
        return val

    def clean_emergency_contact_phone(self):
        val = self.cleaned_data.get('emergency_contact_phone')
        if not val or val.strip() == '':
            raise forms.ValidationError("Emergency contact phone is required.")
        return val

    # BUG: No cross-field validation, no date format check, no numeric check
```

---

## Page 2 — Visit Log

### Form Fields

```
SECTION: Visit Information
───────────────────────────
Field: Patient
  Type: Select2 searchable dropdown (linked to Patient records)
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

Field: Visit Number
  Type: TextInput
  Placeholder: "Format: V-001"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: No regex validation — accepts "V@#!", "VISIT!!!", "123abc"

Field: Visit Date
  Type: TextInput + Flatpickr (cosmetic)
  Placeholder: "DD/MM/YYYY"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: CharField — accepts "99/99/9999", "yesterday"

Field: Visit Type
  Type: Select (Screening / Baseline / Follow-up / Final Visit / Unscheduled)
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

Field: Investigator Name
  Type: TextInput
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

Field: Coordinator
  Type: Select (logged-in users with coordinator role)
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

SECTION: Vitals (all fields are plain text, no numeric enforcement)
────────────────────────────────────────────────────────────────────
Field: Systolic BP (mmHg)
  Type: TextInput — plain text
  Placeholder: "e.g. 120"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: Accepts "normal", "high", "120/80", alphabets

Field: Diastolic BP (mmHg)
  Type: TextInput — plain text
  Placeholder: "e.g. 80"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: Accepts "low", "N/A", alphabets

Field: Heart Rate (bpm)
  Type: TextInput — plain text
  Placeholder: "e.g. 72"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: Accepts "fast", "irregular"

Field: Body Temperature (°C)
  Type: TextInput — plain text
  Placeholder: "e.g. 37.2"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: Accepts "warm", "normal", "fever"

Field: Oxygen Saturation (%)
  Type: TextInput — plain text
  Placeholder: "e.g. 98"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: Accepts "good", "low", "100%"

SECTION: Visit Details
────────────────────────
Field: Visit Notes
  Type: Textarea
  Required UI: No
  Required Backend: No
  Bug: None

Field: Next Visit Date
  Type: TextInput + Flatpickr
  Placeholder: "DD/MM/YYYY"
  Required UI: No
  Required Backend: No
  Bug: CharField — can be set before Visit Date with no validation

SECTION: Protocol Deviation
─────────────────────────────
Field: Protocol Deviation Occurred?
  Type: Radio (Yes / No), default No
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

Field: Deviation Notes
  Type: Textarea
  Placeholder: "Describe the deviation in detail"
  Required UI: Yes — shown with (*) when Protocol Deviation = Yes (JS conditional show)
  Required Backend: No — no clean() cross-field validation
  Bug: If JS is bypassed or deviation=Yes, notes field saves empty
```

---

## Page 3 — Lab Results

### Form Fields

```
SECTION: Sample Information
─────────────────────────────
Field: Patient
  Type: Select2 searchable dropdown
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

Field: Visit Reference
  Type: Select (filtered by patient — shows visit number + date)
  Required UI: No
  Required Backend: No
  Bug: None

Field: Sample Collection Date
  Type: TextInput + Flatpickr
  Placeholder: "DD/MM/YYYY"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: CharField — accepts "00/00/0000", "N/A", "collected yesterday"

Field: Sample Type
  Type: Select (Blood / Urine / Tissue / CSF)
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

SECTION: Test Results
──────────────────────
Field: Test Name
  Type: TextInput
  Placeholder: "e.g. Complete Blood Count, HbA1c"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

Field: Result Value
  Type: TextInput — plain text (should be numeric)
  Placeholder: "e.g. 5.4"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: Accepts "positive", "reactive", "low", "within range"

Field: Unit
  Type: TextInput — free text (should be controlled dropdown)
  Placeholder: "e.g. mg/dL, mmol/L, %"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: Accepts "xyz", "units", "unknown", any garbage

Field: Reference Range — Low
  Type: TextInput — plain text
  Placeholder: "e.g. 4.0"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: Accepts "low", "N/A", alphabets

Field: Reference Range — High
  Type: TextInput — plain text
  Placeholder: "e.g. 11.0"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: Accepts "high", "unlimited", alphabets

Field: Abnormal Flag
  Type: Select (Normal / Abnormal / Critical)
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: When "Critical" is selected, Remarks should be required — but no validation enforces this

SECTION: Lab Information
──────────────────────────
Field: Lab Technician Name
  Type: TextInput
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

Field: Lab Name / Facility
  Type: TextInput
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

Field: Remarks / Clinical Notes
  Type: Textarea
  Required UI: No (no asterisk)
  Required Backend: No
  Bug: Silent — when Abnormal Flag = Critical, this should be mandatory, but backend ignores it
```

---

## Page 4 — Adverse Events

### Form Fields

```
SECTION: Event Information
───────────────────────────
Field: Patient
  Type: Select2 searchable dropdown
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

Field: Event Title / Name
  Type: TextInput
  Placeholder: "Brief title of the adverse event"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

Field: Onset Date
  Type: TextInput + Flatpickr
  Placeholder: "DD/MM/YYYY"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: CharField — accepts "last week", "approximate", "2025/99/99"

Field: Resolution Date
  Type: TextInput + Flatpickr
  Placeholder: "DD/MM/YYYY (leave blank if ongoing)"
  Required UI: No
  Required Backend: No
  Bug: CharField — accepts dates before Onset Date, no comparison validation

Field: Severity
  Type: Select (Mild / Moderate / Severe / Life-Threatening)
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

Field: Causality Assessment
  Type: Select (Related / Unrelated / Possible / Probable)
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

Field: Event Description
  Type: Textarea
  Placeholder: "Detailed description of the event"
  Required UI: Yes (*) — label marked as required
  Required Backend: No — blank=True in model, no clean() validation
  Bug: Saves with empty description despite asterisk

SECTION: Management
─────────────────────
Field: Action Taken
  Type: Select (None / Dose Reduced / Drug Stopped / Hospitalized)
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

Field: Outcome
  Type: Select (Recovered / Recovering / Ongoing / Fatal / Unknown)
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

SECTION: SAE (Serious Adverse Event)
──────────────────────────────────────
Field: Is this a Serious Adverse Event (SAE)?
  Type: Checkbox
  Required UI: No (optional)
  Required Backend: No
  Bug: None

Field: SAE Report Number
  Type: TextInput
  Placeholder: "SAE-YYYY-XXXXX"
  Required UI: Yes (*) — shown via JS when SAE checkbox is checked
  Required Backend: No — blank=True, no conditional clean() logic
  Bug: Saves without SAE Report Number even when SAE = True

SECTION: Reporting
────────────────────
Field: Reported By
  Type: TextInput
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: None

Field: Report Date
  Type: TextInput + Flatpickr
  Placeholder: "DD/MM/YYYY"
  Required UI: Yes (*)
  Required Backend: Yes
  Bug: CharField — accepts future dates, "TBD", garbage strings

Field: Regulatory Reported?
  Type: Checkbox (Yes/No toggle)
  Required UI: No
  Required Backend: No
  Bug: None

Field: Attachment / Supporting Document
  Type: FileInput
  Required UI: No
  Required Backend: No
  Bug: No file type validation — accepts .exe, .js, .bat, .sh — dangerous file types accepted silently
```

---

## Page 5 — Patient Listing

### Features & Specs

```
LAYOUT:
- Full-width DataTables table
- Top bar: Search input + Filter dropdowns + Export button
- Pagination: 10 / 25 / 50 records per page (default 25)
- Column headers are sortable (click to sort)

COLUMNS SHOWN:
1. MRN
2. Patient Name (First + Last)
3. Date of Birth
4. Gender
5. Trial Assignment
6. Enrollment Date
7. Status (colored badge)
8. Actions (View / Edit / Delete)

SEARCH:
- Global search across: Name, MRN, Diagnosis
- Filter by: Status (dropdown), Trial (dropdown), Gender (dropdown)

BUG — Export ignores filters:
- User applies filter: "Status = Active, Trial = TRIAL-001"
- Clicks Export CSV
- CSV contains ALL patients regardless of filters
- No message or warning shown to user

BUG — Export not logged:
- Export action does not create an AuditLog entry
- Other actions (Create, Update, Delete) do log

PATIENT DETAIL VIEW:
From listing, clicking "View" → Patient Detail page showing:
- All patient info in read-only cards
- Tabbed sub-sections: Visits | Lab Results | Adverse Events | Audit Trail
- Each tab shows linked records with count badge
- Add New button per tab
- Edit / Delete buttons with reason modal
```

---

## Audit Trail Module

### audit/mixins.py

```python
from .models import AuditLog

def log_action(request, module, record_id, action, changed_fields, reason=''):
    """
    Call this in every view after a successful save/delete.
    
    BUG: In patients/views.py — status-only changes are silently skipped.
    This is implemented by checking if changed_fields only contains 'status'
    and returning early without creating the log entry.
    
    All other field changes are logged normally.
    """
    # INTENTIONAL BUG: skip logging for status-only changes on patients module
    if module == 'patients' and action == 'UPDATE':
        non_status_changes = {k: v for k, v in changed_fields.items() if k != 'status'}
        if not non_status_changes:
            return  # Silent skip — no log created for status changes

    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
    AuditLog.objects.create(
        user=request.user,
        module=module,
        record_id=record_id,
        action=action,
        reason=reason,
        changed_fields=changed_fields,
        ip_address=ip[:45] if ip else None,
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
    )
```

### Audit Trail View

```
URL: /audit/
URL: /audit/patient/<patient_id>/      (per-patient trail)
URL: /audit/module/<module_name>/      (per-module trail)

TABLE COLUMNS:
- Timestamp (DD/MM/YYYY HH:MM:SS)
- User
- Module
- Record ID
- Action (badge: green=CREATE, blue=UPDATE, red=DELETE)
- Reason
- Changed Fields (expandable JSON diff)
- IP Address

FILTERS:
- Date range (from/to)
- User
- Module
- Action type

DISPLAY: Monospaced font for timestamps, action badges colored by type
NOTE: Status changes on Patient will not appear here — this is the intentional gap
```

---

## Export / Report System

### Export Specification Per Module

Every page has an **Export** button. Each export generates a CSV. Certain fields are **excluded** from the export intentionally (sensitive or internal fields).

### Export — Patient List

```
Included Columns:
  MRN, First Name, Last Name, Date of Birth, Gender, Blood Group,
  Email, Phone, Trial Assignment, Enrollment Date, Status, Diagnosis,
  Weight (kg), Height (cm), Created At

Excluded from Export (not in CSV):
  - National ID          (privacy — sensitive govt ID)
  - Address              (privacy)
  - Emergency Contact Name  (internal use only)
  - Emergency Contact Phone (internal use only)
  - Consent Signed       (excluded — legal sensitivity)
  - Created By (user ID) (internal)

BUG: Filter/search state is ignored — exports ALL patients
```

### Export — Visit Log

```
Included Columns:
  Patient MRN, Patient Name, Visit Number, Visit Date, Visit Type,
  Investigator Name, Systolic BP, Diastolic BP, Heart Rate,
  Body Temperature, Oxygen Saturation, Protocol Deviation,
  Next Visit Date, Created At

Excluded from Export:
  - Visit Notes          (free text, excluded for brevity)
  - Deviation Notes      (excluded)
  - Coordinator (user)   (internal)
  - Created By           (internal)

BUG: Exports all visits for all patients regardless of current page filter
```

### Export — Lab Results

```
Included Columns:
  Patient MRN, Patient Name, Sample Collection Date, Sample Type,
  Test Name, Result Value, Unit, Reference Range Low,
  Reference Range High, Abnormal Flag, Lab Name, Created At

Excluded from Export:
  - Remarks              (clinical notes excluded)
  - Lab Technician       (excluded)
  - Visit Reference      (internal FK)
  - Created By           (internal)

BUG: Exports all lab results, not filtered by current patient view
```

### Export — Adverse Events

```
Included Columns:
  Patient MRN, Patient Name, Event Title, Onset Date, Resolution Date,
  Severity, Causality, Action Taken, Outcome, Is SAE,
  SAE Report Number, Report Date, Regulatory Reported, Created At

Excluded from Export:
  - Event Description    (excluded — lengthy clinical narrative)
  - Attachment path      (excluded — file path exposure risk)
  - Reported By          (excluded)
  - Created By           (internal)

BUG: Exports all adverse events, ignores filters
BUG: Export action is NOT logged in audit trail
```

### Export — Audit Trail

```
Included Columns:
  Timestamp, User (username), Module, Record ID, Action, Reason,
  IP Address, Created At

Excluded from Export:
  - Changed Fields JSON  (excluded — too verbose for CSV)
  - User Agent           (excluded)

Note: This export IS accessible but the irony is that the export itself
      is not logged — so exporting the audit trail doesn't appear in the audit trail.
```

### Export Implementation (reports/views.py)

```python
import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from patients.models import Patient

PATIENT_EXPORT_FIELDS = [
    'medical_record_number', 'first_name', 'last_name', 'date_of_birth',
    'gender', 'blood_group', 'email', 'phone', 'trial_assignment',
    'enrollment_date', 'status', 'diagnosis', 'weight_kg', 'height_cm',
    'created_at'
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

    # BUG: Fetches ALL patients — ignores any GET params (search/filter)
    patients = Patient.objects.all()

    for p in patients:
        writer.writerow([getattr(p, f) for f in PATIENT_EXPORT_FIELDS])

    # BUG: No log_action() call here — export is not audited

    return response
```

---

## Authentication System

### Login Page

```
URL: /login/
Fields:
  - Username (text)
  - Password (password)
  - "Remember Me" checkbox (does nothing — cosmetic bug)

On Success: Redirect to /dashboard/
On Failure: Show "Invalid username or password." (generic, no lockout)

BUG: Failed login attempts are NOT logged in AuditLog
BUG: "Remember Me" checkbox has no effect on session length
BUG: No account lockout after N failed attempts

Session Timeout: 30 minutes of inactivity (Django SESSION_COOKIE_AGE = 1800)
After timeout: Redirect to login with message "Your session has expired."
```

### settings.py (auth-related)

```python
AUTH_USER_MODEL = 'accounts.CTMSUser'

SESSION_COOKIE_AGE = 1800          # 30 minutes
SESSION_SAVE_EVERY_REQUEST = True  # Resets timer on activity
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'
```

### Seed Users

```python
# Run via: python manage.py seed_users

Users to create:
  1. admin@ctms.com       / Admin@123       (superuser, Admin role)
  2. coordinator1@ctms.com / Coord@123      (Coordinator role)
  3. coordinator2@ctms.com / Coord@123      (Coordinator role)
```

---

## UI & Design System

### Base Theme

```
Theme: AdminLTE 3 (https://adminlte.io/)
Color Scheme: Blue/clinical (#007bff primary, white, light grey)
Font: Inter or Roboto (via Google Fonts)
Icons: Font Awesome 6 Free
```

### Sidebar Navigation

```
CTMS Logo + "v2.1.0" tag

Navigation Items:
  🏠 Dashboard
  ─────────────
  👥 Patients
     └── Register New Patient
     └── All Patients
  📋 Visit Logs
     └── Add Visit
     └── All Visits
  🧪 Lab Results
     └── Add Lab Result
     └── All Lab Results
  ⚠️  Adverse Events
     └── Report Event
     └── All Events
  ─────────────
  📊 Reports & Export
  🔍 Audit Trail
  ─────────────
  👤 [Username] — Coordinator
  🚪 Logout
```

### Dashboard (Landing Page After Login)

```
Top Row — 4 Stat Cards:
  [Total Patients: XX]  [Active Trials: 4]  [Open AEs: XX]  [Visits This Month: XX]

Middle Row:
  Recent Patients table (last 5 registered)
  Recent Adverse Events (last 5, severity colored)

Bottom Row:
  Quick Actions: [+ Register Patient] [+ Log Visit] [+ Report AE] [View Audit Trail]

Footer: "CTMS v2.1.0 | Confidential — For Internal Use Only | © 2025 ClinTrials Corp"
```

### Reason Modal (Edit & Delete)

```html
<!-- Triggered before form submission on all Edit and Delete actions -->
<!-- Uses SweetAlert2 -->

Edit Reason Modal:
  Title: "Reason for Edit"
  Body: "Please provide a reason for modifying this record."
  Input: Textarea (required — JS enforces locally)
  Buttons: [Cancel] [Confirm Edit]

Delete Reason Modal:
  Title: "Confirm Deletion"
  Body: "This action cannot be undone. Please state the reason for deletion."
  Input: Textarea (required — JS enforces locally)
  Buttons: [Cancel] [Confirm Delete] (red)

Implementation Note:
  The reason field IS required in the modal JS.
  However — if a candidate submits the form directly via Playwright without
  triggering the modal, the backend still saves without a reason.
  The backend should also validate that reason is non-empty on POST for edit/delete.
  BUG: Backend does NOT enforce reason — it's only enforced by frontend JS modal.
```

### Status Badges

```css
.badge-active    { background: #28a745; color: white; }
.badge-inactive  { background: #6c757d; color: white; }
.badge-withdrawn { background: #dc3545; color: white; }
.badge-critical  { background: #dc3545; color: white; }
.badge-abnormal  { background: #ffc107; color: black; }
.badge-normal    { background: #28a745; color: white; }
```

---

## Seed Data

### management/commands/seed_data.py

```python
"""
Creates realistic demo data for assessment use.
Run: python manage.py seed_data
"""

Patients to create (10 records):
  - Mix of Active, Inactive, Withdrawn statuses
  - Spread across all 4 trials
  - Some with intentionally bad data already saved (shows the bugs work):
      * Patient 3: weight_kg = "obese" (shows CharField bug)
      * Patient 5: date_of_birth = "01/00/1990" (shows date bug)
      * Patient 7: consent_signed = False (shows consent bug)
      * Patient 9: email = "xyz@@domain" (shows email bug)

Visits to create (3 per patient = 30 total):
  - Mix of visit types
  - Some with protocol_deviation = True but deviation_notes = "" (shows the bug)
  - Some with systolic_bp = "normal" (shows numeric bug)

Lab Results (2 per patient = 20 total):
  - Some with abnormal_flag = "critical" and remarks = "" (shows the gap)
  - Some with result_value = "positive" (shows numeric bug)

Adverse Events (5 total across patients):
  - 2 marked as SAE but sae_report_number = "" (shows conditional bug)
  - 1 with resolution_date before onset_date (shows logic bug)
  - 1 with event_description = "" despite being shown as required

Audit Logs (auto-generated from seeding actions):
  - NOTE: Status changes are intentionally NOT in audit log
  - All other seeded creates will appear in audit trail
```

---

## Deployment

### requirements.txt

```
Django==4.2.13
python-decouple==3.8
whitenoise==6.6.0
gunicorn==21.2.0
Pillow==10.3.0
django-environ==0.11.2
```

### Option A — Local (Simplest for Assessment)

```bash
# Setup
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure
cp .env.example .env          # Edit SECRET_KEY and DEBUG=True

# Initialize
python manage.py migrate
python manage.py seed_users
python manage.py seed_data

# Run
python manage.py runserver

# Share with candidate:
# URL: http://localhost:8000
# Login: coordinator1@ctms.com / Coord@123
```

### Option B — Railway / Render (Free Cloud Deployment)

```bash
# Procfile
web: gunicorn ctms.wsgi --log-file -

# Environment variables to set on platform:
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app
DATABASE_URL=sqlite:///db.sqlite3
```

### Option C — Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py migrate && python manage.py seed_users && python manage.py seed_data
CMD ["gunicorn", "ctms.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```bash
docker build -t ctms .
docker run -p 8000:8000 ctms
```

---

## Assessment Handout (Give to Candidate)

```
=============================================================
  CTMS — Clinical Trial Management System
  QA Assessment — Session Brief
=============================================================

System URL:    http://[your-url]/
Username:      coordinator1@ctms.com
Password:      Coord@123

CONTEXT:
You are a QA engineer joining a clinical trials team.
This system has been built by a development team and is
about to go into production. Your job is to test it thoroughly
before sign-off.

SESSION 1 — Manual Exploration (2.5 hours):
  1. Explore the full system — all 5 pages
  2. Document all functionality you discover
  3. Identify and document all bugs, inconsistencies, and
     gaps you find
  4. Use the provided Test Case Template (Excel/Google Sheet)

SESSION 2 — Automation (2.5 hours):
  1. Using your documentation from Session 1
  2. Write Playwright (Python) test scripts for:
     - At least 3 complete CRUD flows
     - Form validation scenarios (both positive and negative)
     - At least 1 audit trail verification
  3. Scripts should be runnable with: pytest tests/

DELIVERABLES:
  - Completed test case document
  - Playwright test files
  - Brief summary of critical bugs found

=============================================================
```

---

## Summary — Bug Count by Category

| Category | Count | Description |
|----------|-------|-------------|
| A — UI Required, Backend Not Enforced | 5 | Consent, Diagnosis, Deviation Notes, AE Description, SAE Number |
| B — Not Required in UI, Backend Rejects | 2 | Emergency Contact Name & Phone |
| C — Date Fields Accept Garbage | 8 | DOB, Enrollment, Visit Date, Next Visit, Sample Date, Onset, Resolution, Report Date |
| D — Numeric Fields as Textboxes | 10 | Weight, Height, BP x2, HR, Temp, O2Sat, Result Value, Ref Range x2 |
| E — Format Validation Bypass | 5 | MRN, National ID, Email, Phone, Visit Number |
| F — Logic/Cross-field Bugs | 4 | Date order, SAE conditional, Deviation conditional, Critical remarks |
| G — Audit Trail Gaps | 3 | Status change not logged, Export not logged, Login failure not logged |
| H — Export Bugs | 2 | Filters ignored, Remember Me does nothing |
| **Total** | **39** | |

> A strong semi-senior candidate (2–5 yrs) should find 25–32 of these.
> Finding all 39 in 2.5 hours would be exceptional.
> Automation coverage of 15+ scenarios in 2.5 hours is the target.
