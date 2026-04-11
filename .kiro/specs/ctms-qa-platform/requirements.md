# Requirements Document

## Introduction

The CTMS QA Assessment Platform is a Django 4.2 web application that simulates a production-grade Clinical Trial Management System. It manages patients, visit logs, lab results, and adverse events across four fictional clinical trials. The system includes a full audit trail engine, CSV export, role-based authentication, and an AdminLTE 3 UI. The platform contains 39 intentional bugs across validation, audit, and data-type layers — precisely placed to enable structured evaluation of QA candidates' exploratory testing and automation skills. Requirements in this document describe the system as it is designed to behave, including all intentional gaps.

## Glossary

- **Authentication_System**: The accounts Django app handling login, logout, and session management
- **Patient_Module**: The patients Django app handling patient CRUD operations
- **Visit_Module**: The visits Django app handling visit log CRUD operations
- **Lab_Module**: The labs Django app handling lab result CRUD operations
- **AE_Module**: The adverse_events Django app handling adverse event CRUD operations
- **Audit_System**: The audit Django app containing `log_action()` and the AuditLog model
- **Export_System**: The reports Django app handling patient listing and CSV export
- **Dashboard**: The main landing page after login showing stat cards and recent records
- **PatientForm**: The Django ModelForm for creating and editing Patient records
- **VisitForm**: The Django ModelForm for creating and editing VisitLog records
- **LabForm**: The Django ModelForm for creating and editing LabResult records
- **AdverseEventForm**: The Django ModelForm for creating and editing AdverseEvent records
- **AuditLog**: The database model recording system actions with timestamp, user, module, action, and changed fields
- **CTMSUser**: The custom user model extending AbstractUser with role and employee_id fields
- **SAE**: Serious Adverse Event — an adverse event flagged as serious via the `is_sae` boolean field
- **Cat-A Bug**: UI shows required asterisk (*) but backend does not enforce the field
- **Cat-B Bug**: UI shows no required indicator but backend raises ValidationError
- **Cat-C Bug**: Date field stored as CharField, accepts any string
- **Cat-D Bug**: Numeric field stored as CharField, accepts any string
- **Cat-E Bug**: Format hint shown in UI placeholder, no backend RegexValidator or EmailValidator
- **Cat-F Bug**: Cross-field conditional validation missing from form `clean()` method
- **Cat-G Bug**: Audit trail gap — specific action not logged
- **Cat-H Bug**: Export or UI behavior ignores user-provided parameters

---

## Requirements

### Requirement 1: Authentication

**User Story:** As a CTMS user, I want to log in and out of the system, so that I can access clinical trial data securely.

#### Acceptance Criteria

1. WHEN a user submits valid credentials, THE Authentication_System SHALL authenticate the user, create a session, and redirect to `/dashboard/`
2. WHEN a user submits valid credentials, THE Authentication_System SHALL create an AuditLog entry with action=LOGIN
3. WHEN a user submits invalid credentials, THE Authentication_System SHALL display an error message "Invalid username or password."
4. WHEN a user submits invalid credentials, THE Authentication_System SHALL NOT create an AuditLog entry (Cat-G bug: failed login not logged)
5. WHEN a user logs out via `/logout/`, THE Authentication_System SHALL terminate the session and create an AuditLog entry with action=LOGOUT
6. WHEN a session has been inactive for 30 minutes, THE Authentication_System SHALL expire the session and redirect the user to `/login/`
7. THE Authentication_System SHALL reset the session inactivity timer on every authenticated request
8. THE "Remember Me" checkbox on the login form SHALL have no effect on SESSION_COOKIE_AGE (Cat-H bug: cosmetic only)
9. THE Authentication_System SHALL NOT implement account lockout after repeated failed login attempts

---

### Requirement 2: Patient Registration — CRUD

**User Story:** As a coordinator, I want to create, view, edit, and delete patient records, so that I can manage clinical trial participants.

#### Acceptance Criteria

1. WHEN a user submits a valid patient registration form, THE Patient_Module SHALL create a Patient record, set `created_by` to the current user, and redirect to the patient detail page
2. WHEN a patient record is created, THE Audit_System SHALL create an AuditLog entry with action=CREATE and module='patients'
3. WHEN a user requests the patient detail page, THE Patient_Module SHALL display all patient fields and tabbed sub-sections for Visits, Lab Results, Adverse Events, and Audit Trail
4. WHEN a user submits a valid patient edit form, THE Patient_Module SHALL update the Patient record and redirect to the patient detail page
5. WHEN a patient record is edited and the changed fields include fields other than status, THE Audit_System SHALL create an AuditLog entry with action=UPDATE, the changed field values, and the edit reason
6. WHEN a user confirms patient deletion, THE Patient_Module SHALL delete the Patient record and redirect to the patient listing
7. WHEN a patient record is deleted, THE Audit_System SHALL create an AuditLog entry with action=DELETE and the deletion reason
8. THE Patient_Module SHALL require authentication via `@login_required` on all CRUD views

---

### Requirement 3: Patient Registration — Field Validation Gaps

**User Story:** As a QA assessor, I want the patient form to contain precisely-placed validation gaps, so that candidates can discover and document them.

#### Acceptance Criteria

1. THE PatientForm SHALL accept any string value for `date_of_birth` without date format validation (Cat-C bug)
2. THE PatientForm SHALL accept any string value for `enrollment_date` without date format validation (Cat-C bug)
3. THE PatientForm SHALL accept any string value for `weight_kg` without numeric validation (Cat-D bug)
4. THE PatientForm SHALL accept any string value for `height_cm` without numeric validation (Cat-D bug)
5. THE PatientForm SHALL accept any string value for `email` without email format validation, using TextInput instead of EmailInput (Cat-E bug)
6. THE PatientForm SHALL accept any string value for `medical_record_number` without enforcing the "MRN-000000" format (Cat-E bug)
7. THE PatientForm SHALL accept any string value for `national_id` without length or format validation (Cat-E bug)
8. THE PatientForm SHALL accept any string value for `phone` without numeric or format validation (Cat-E bug)
9. WHEN `consent_signed` is False, THE PatientForm SHALL pass validation and save the record (Cat-A bug)
10. WHEN `diagnosis` is empty, THE PatientForm SHALL pass validation and save the record (Cat-A bug)
11. WHEN `emergency_contact_name` is empty, THE PatientForm SHALL raise a ValidationError (Cat-B bug)
12. WHEN `emergency_contact_phone` is empty, THE PatientForm SHALL raise a ValidationError (Cat-B bug)
13. THE patient registration template SHALL NOT display a required asterisk (*) next to the Emergency Contact Name or Emergency Contact Phone labels (Cat-B bug)
14. THE PatientForm SHALL NOT perform any cross-field validation (Cat-F bug)

---

### Requirement 4: Patient Status Change Audit Gap

**User Story:** As a QA assessor, I want patient status-only changes to be silently unlogged, so that candidates can discover the audit trail gap.

#### Acceptance Criteria

1. WHEN a patient record is edited and only the `status` field changes, THE Audit_System SHALL NOT create an AuditLog entry (Cat-G bug)
2. WHEN a patient record is edited and fields other than `status` also change, THE Audit_System SHALL create an AuditLog entry that includes all changed fields
3. THE `log_action()` function SHALL implement the status-skip by returning early when `module='patients'`, `action='UPDATE'`, and `changed_fields` contains only the `'status'` key

---

### Requirement 5: Visit Log — CRUD and Validation Gaps

**User Story:** As a coordinator, I want to create, view, edit, and delete visit log records, so that I can track patient visits and vitals.

#### Acceptance Criteria

1. WHEN a user submits a valid visit form, THE Visit_Module SHALL create a VisitLog record linked to the selected patient and redirect to the visit detail page
2. WHEN a visit record is created or updated, THE Audit_System SHALL create an AuditLog entry with the appropriate action and module='visits'
3. WHEN a visit record is deleted, THE Audit_System SHALL create an AuditLog entry with action=DELETE
4. THE VisitForm SHALL accept any string value for `visit_date` without date format validation (Cat-C bug)
5. THE VisitForm SHALL accept any string value for `next_visit_date` without validating that it is chronologically after `visit_date` (Cat-C/F bug)
6. THE VisitForm SHALL accept any string value for `visit_number` without enforcing the "V-001" format (Cat-E bug)
7. THE VisitForm SHALL accept any string value for `systolic_bp` without numeric or range validation (Cat-D bug)
8. THE VisitForm SHALL accept any string value for `diastolic_bp` without numeric or range validation (Cat-D bug)
9. THE VisitForm SHALL accept any string value for `heart_rate` without numeric or range validation (Cat-D bug)
10. THE VisitForm SHALL accept any string value for `body_temperature` without numeric or range validation (Cat-D bug)
11. THE VisitForm SHALL accept any string value for `oxygen_saturation` without numeric or range validation (Cat-D bug)
12. WHEN `protocol_deviation` is True and `deviation_notes` is empty, THE VisitForm SHALL pass validation and save the record (Cat-A/F bug)
13. THE VisitForm SHALL NOT perform any cross-field validation (Cat-F bug)

---

### Requirement 6: Lab Results — CRUD and Validation Gaps

**User Story:** As a coordinator, I want to create, view, edit, and delete lab result records, so that I can track patient laboratory data.

#### Acceptance Criteria

1. WHEN a user submits a valid lab result form, THE Lab_Module SHALL create a LabResult record linked to the selected patient and redirect to the lab result detail page
2. WHEN a lab result record is created or updated, THE Audit_System SHALL create an AuditLog entry with the appropriate action and module='labs'
3. WHEN a lab result record is deleted, THE Audit_System SHALL create an AuditLog entry with action=DELETE
4. THE LabForm SHALL accept any string value for `sample_collection_date` without date format validation (Cat-C bug)
5. THE LabForm SHALL accept any string value for `result_value` without numeric validation (Cat-D bug)
6. THE LabForm SHALL accept any string value for `reference_range_low` without numeric validation (Cat-D bug)
7. THE LabForm SHALL accept any string value for `reference_range_high` without numeric validation (Cat-D bug)
8. THE `unit` field SHALL be a free-text input with no controlled dropdown or validation (Cat-D bug)
9. WHEN `abnormal_flag` is 'critical' and `remarks` is empty, THE LabForm SHALL pass validation and save the record (Cat-F bug)
10. THE LabForm SHALL NOT perform any cross-field validation (Cat-F bug)

---

### Requirement 7: Adverse Events — CRUD and Validation Gaps

**User Story:** As a coordinator, I want to create, view, edit, and delete adverse event records, so that I can track and report patient safety events.

#### Acceptance Criteria

1. WHEN a user submits a valid adverse event form, THE AE_Module SHALL create an AdverseEvent record linked to the selected patient and redirect to the adverse event detail page
2. WHEN an adverse event record is created or updated, THE Audit_System SHALL create an AuditLog entry with the appropriate action and module='adverse_events'
3. WHEN an adverse event record is deleted, THE Audit_System SHALL create an AuditLog entry with action=DELETE
4. THE AdverseEventForm SHALL accept any string value for `onset_date` without date format validation (Cat-C bug)
5. THE AdverseEventForm SHALL accept any string value for `resolution_date` without date format validation (Cat-C bug)
6. THE AdverseEventForm SHALL accept any string value for `report_date` without date format validation, including future dates (Cat-C bug)
7. WHEN `resolution_date` is chronologically before `onset_date`, THE AdverseEventForm SHALL pass validation and save the record (Cat-F bug)
8. WHEN `event_description` is empty, THE AdverseEventForm SHALL pass validation and save the record (Cat-A bug)
9. WHEN `is_sae` is True and `sae_report_number` is empty, THE AdverseEventForm SHALL pass validation and save the record (Cat-A/F bug)
10. THE AdverseEventForm SHALL NOT perform any cross-field validation (Cat-F bug)
11. THE `attachment` field SHALL accept file uploads of any file type including .exe, .js, .bat, and .sh with no file type validation (unsafe upload bug)

---

### Requirement 8: Audit Trail

**User Story:** As an administrator, I want to view a comprehensive audit trail of all system actions, so that I can monitor data changes and user activity.

#### Acceptance Criteria

1. THE Audit_System SHALL record AuditLog entries for CREATE, UPDATE, and DELETE actions on the patients, visits, labs, and adverse_events modules
2. THE Audit_System SHALL record AuditLog entries for LOGIN and LOGOUT actions on the accounts module
3. WHEN a patient status-only update occurs, THE Audit_System SHALL NOT record an AuditLog entry (Cat-G bug — see Requirement 4)
4. WHEN a CSV export is performed, THE Audit_System SHALL NOT record an AuditLog entry (Cat-G bug)
5. WHEN a failed login attempt occurs, THE Audit_System SHALL NOT record an AuditLog entry (Cat-G bug)
6. THE AuditLog model SHALL store timestamp, user (FK), module, record_id, action, reason, changed_fields (JSONField), ip_address, and user_agent
7. THE `changed_fields` JSONField SHALL store the format `{"field": {"old": value, "new": value}}` for UPDATE actions
8. THE audit trail view at `/audit/` SHALL support filtering by date range, user, module, and action
9. THE audit trail view at `/audit/patient/<patient_id>/` SHALL display only AuditLog entries for the specified patient
10. THE audit trail view at `/audit/module/<module_name>/` SHALL display only AuditLog entries for the specified module

---

### Requirement 9: Patient Listing and CSV Export

**User Story:** As a coordinator, I want to view a filterable patient list and export data to CSV, so that I can review and share clinical trial data.

#### Acceptance Criteria

1. THE Export_System SHALL display a patient listing page at `/reports/` with a DataTables table showing MRN, Patient Name, DOB, Gender, Trial, Enrollment Date, Status, and Actions columns
2. THE patient listing page SHALL support filtering by search text, status, trial, and gender via GET parameters
3. WHEN a user clicks Export CSV on the patient listing page, THE Export_System SHALL return a CSV file containing all Patient records regardless of any active filters (Cat-H bug)
4. THE export_patients_csv view SHALL use `Patient.objects.all()` and SHALL NOT read any GET parameters (Cat-H bug)
5. THE Export_System SHALL provide CSV export endpoints for visits, labs, adverse events, and audit trail, each exporting all records without filter support (Cat-H bug)
6. THE patient CSV export SHALL exclude the fields: national_id, address, emergency_contact_name, emergency_contact_phone, consent_signed, created_by
7. THE visit CSV export SHALL exclude the fields: visit_notes, deviation_notes, coordinator, created_by
8. THE lab CSV export SHALL exclude the fields: remarks, lab_technician, visit (FK), created_by
9. THE adverse event CSV export SHALL exclude the fields: event_description, attachment, reported_by, created_by
10. THE audit trail CSV export SHALL exclude the fields: changed_fields JSON, user_agent

---

### Requirement 10: Dashboard

**User Story:** As a coordinator, I want a dashboard overview of the system, so that I can quickly see key metrics and navigate to common actions.

#### Acceptance Criteria

1. THE Dashboard SHALL display four stat cards: Total Patients, Active Trials (always 4), Open AEs, and Visits This Month
2. THE Dashboard SHALL display a Recent Patients table showing the last 5 registered patients with columns: MRN, Name, Trial, Status
3. THE Dashboard SHALL display a Recent Adverse Events table showing the last 5 adverse events with columns: Patient, Event, Severity (colored badge)
4. THE Dashboard SHALL display Quick Action buttons: Register Patient, Log Visit, Report AE, and View Audit Trail
5. THE Dashboard SHALL require authentication via `@login_required`

---

### Requirement 11: Seed Data Management Commands

**User Story:** As a system administrator, I want management commands to populate the system with demo data, so that QA candidates have realistic records to test against.

#### Acceptance Criteria

1. THE `seed_users` management command SHALL create three CTMSUser accounts: admin@ctms.com (Admin role, superuser), coordinator1@ctms.com (Coordinator role), and coordinator2@ctms.com (Coordinator role)
2. THE `seed_data` management command SHALL create 10 Patient records, 30 VisitLog records, 20 LabResult records, and 5 AdverseEvent records
3. THE seed Patient records SHALL include intentionally malformed field values that demonstrate the intentional bugs, including: a patient with `weight_kg="obese"` (Cat-D), a patient with `date_of_birth="01/00/1990"` (Cat-C), a patient with `consent_signed=False` (Cat-A), and a patient with `email="xyz@@domain"` (Cat-E)
4. THE seed VisitLog records SHALL include records with `protocol_deviation=True` and `deviation_notes=""` (Cat-A/F) and records with `systolic_bp="normal"` (Cat-D)
5. THE seed LabResult records SHALL include records with `abnormal_flag="critical"` and `remarks=""` (Cat-F) and records with `result_value="positive"` (Cat-D)
6. THE seed AdverseEvent records SHALL include records with `is_sae=True` and `sae_report_number=""` (Cat-A/F), a record with `resolution_date` before `onset_date` (Cat-F), and a record with `event_description=""` (Cat-A)

---

### Requirement 12: Deployment

**User Story:** As a system administrator, I want multiple deployment options, so that the platform can be run locally, on cloud platforms, or in containers.

#### Acceptance Criteria

1. THE system SHALL support local development deployment using `python manage.py runserver` after running `migrate`, `seed_users`, and `seed_data`
2. THE system SHALL include a `Procfile` with `web: gunicorn ctms.wsgi --log-file -` for Railway and Render deployment
3. THE system SHALL include a `Dockerfile` based on python:3.11-slim that runs migrations and seed commands at build time and starts gunicorn on port 8000
4. THE system SHALL load `SECRET_KEY` from environment variables via python-decouple
5. THE system SHALL use SQLite for development and support PostgreSQL via `DATABASE_URL` for production
6. THE system SHALL serve static files via whitenoise

---

### Requirement 13: UI and Template Structure

**User Story:** As a QA candidate, I want the system to look like a production clinical application, so that I can perform realistic exploratory testing.

#### Acceptance Criteria

1. THE system SHALL use AdminLTE 3 with Bootstrap 5 as the base UI framework
2. THE base template SHALL include Flatpickr for date fields, Select2 for dropdowns, SweetAlert2 for reason modals, DataTables for listing pages, and Toastr for notifications
3. THE Flatpickr date picker widget SHALL be cosmetic only — the underlying field SHALL be a plain text input that accepts any string when typed directly (Cat-C bug)
4. WHEN a user clicks Edit or Delete on a record, THE system SHALL display a SweetAlert2 reason modal requiring a reason to be entered
5. THE reason modal validation SHALL be enforced by JavaScript only — THE backend SHALL NOT validate that the edit_reason or delete_reason fields are non-empty (Cat-H bug)
6. THE sidebar SHALL include navigation links for Dashboard, Patients, Visit Logs, Lab Results, Adverse Events, Reports & Export, and Audit Trail
7. THE patient detail page SHALL display patient information with tabbed sub-sections for Visits, Lab Results, Adverse Events, and Audit Trail
8. THE system footer SHALL display "CTMS v2.1.0 | Confidential — For Internal Use Only | © 2025 ClinTrials Corp"
