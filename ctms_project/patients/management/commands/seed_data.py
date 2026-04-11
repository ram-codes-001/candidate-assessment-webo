from django.core.management.base import BaseCommand, CommandError
from accounts.models import CTMSUser
from patients.models import Patient
from visits.models import VisitLog
from labs.models import LabResult
from adverse_events.models import AdverseEvent


PATIENT_DATA = [
    # index 0
    {
        'first_name': 'Eleanor', 'last_name': 'Hartwell',
        'date_of_birth': '14/03/1968', 'gender': 'F',
        'medical_record_number': 'MRN-10001', 'national_id': 'NID-881234',
        'email': 'eleanor.hartwell@email.com', 'phone': '+1-555-0101',
        'address': '42 Maple Drive, Boston, MA 02101',
        'blood_group': 'A+', 'weight_kg': '72', 'height_cm': '165',
        'diagnosis': 'Hypertensive heart disease with stage 2 hypertension',
        'trial_assignment': 'TRIAL-001', 'enrollment_date': '05/01/2024',
        'status': 'active', 'emergency_contact_name': 'Robert Hartwell',
        'emergency_contact_phone': '+1-555-0102', 'consent_signed': True,
    },
    # index 1
    {
        'first_name': 'Marcus', 'last_name': 'Delgado',
        'date_of_birth': '22/07/1975', 'gender': 'M',
        'medical_record_number': 'MRN-10002', 'national_id': 'NID-752209',
        'email': 'marcus.delgado@email.com', 'phone': '+1-555-0201',
        'address': '17 Oak Street, Chicago, IL 60601',
        'blood_group': 'O+', 'weight_kg': '88', 'height_cm': '180',
        'diagnosis': 'Non-small cell lung carcinoma, stage IIIA',
        'trial_assignment': 'TRIAL-002', 'enrollment_date': '12/02/2024',
        'status': 'active', 'emergency_contact_name': 'Lucia Delgado',
        'emergency_contact_phone': '+1-555-0202', 'consent_signed': True,
    },
    # index 2 — BUG Cat-D: weight_kg="obese"
    {
        'first_name': 'Priya', 'last_name': 'Nair',
        'date_of_birth': '09/11/1982', 'gender': 'F',
        'medical_record_number': 'MRN-10003', 'national_id': 'NID-823301',
        'email': 'priya.nair@email.com', 'phone': '+1-555-0301',
        'address': '88 Birch Lane, Houston, TX 77001',
        'blood_group': 'B+', 'weight_kg': 'obese', 'height_cm': '158',  # BUG Cat-D
        'diagnosis': 'Type 2 diabetes mellitus with peripheral neuropathy',
        'trial_assignment': 'TRIAL-003', 'enrollment_date': '20/02/2024',
        'status': 'active', 'emergency_contact_name': 'Arjun Nair',
        'emergency_contact_phone': '+1-555-0302', 'consent_signed': True,
    },
    # index 3
    {
        'first_name': 'Thomas', 'last_name': 'Okafor',
        'date_of_birth': '30/05/1960', 'gender': 'M',
        'medical_record_number': 'MRN-10004', 'national_id': 'NID-601445',
        'email': 'thomas.okafor@email.com', 'phone': '+1-555-0401',
        'address': '5 Cedar Court, Phoenix, AZ 85001',
        'blood_group': 'AB+', 'weight_kg': '95', 'height_cm': '175',
        'diagnosis': 'Parkinson\'s disease, Hoehn and Yahr stage II',
        'trial_assignment': 'TRIAL-004', 'enrollment_date': '01/03/2024',
        'status': 'active', 'emergency_contact_name': 'Ngozi Okafor',
        'emergency_contact_phone': '+1-555-0402', 'consent_signed': True,
    },
    # index 4 — BUG Cat-C: date_of_birth="01/00/1990"
    {
        'first_name': 'Isabelle', 'last_name': 'Fontaine',
        'date_of_birth': '01/00/1990', 'gender': 'F',  # BUG Cat-C
        'medical_record_number': 'MRN-10005', 'national_id': 'NID-900012',
        'email': 'isabelle.fontaine@email.com', 'phone': '+1-555-0501',
        'address': '23 Elm Avenue, Philadelphia, PA 19101',
        'blood_group': 'A-', 'weight_kg': '61', 'height_cm': '162',
        'diagnosis': 'Coronary artery disease with stable angina',
        'trial_assignment': 'TRIAL-001', 'enrollment_date': '10/03/2024',
        'status': 'active', 'emergency_contact_name': 'Pierre Fontaine',
        'emergency_contact_phone': '+1-555-0502', 'consent_signed': True,
    },
    # index 5
    {
        'first_name': 'David', 'last_name': 'Kowalski',
        'date_of_birth': '18/09/1971', 'gender': 'M',
        'medical_record_number': 'MRN-10006', 'national_id': 'NID-710934',
        'email': 'david.kowalski@email.com', 'phone': '+1-555-0601',
        'address': '99 Pine Road, San Antonio, TX 78201',
        'blood_group': 'O-', 'weight_kg': '82', 'height_cm': '178',
        'diagnosis': 'Diffuse large B-cell lymphoma, relapsed',
        'trial_assignment': 'TRIAL-002', 'enrollment_date': '15/03/2024',
        'status': 'inactive', 'emergency_contact_name': 'Anna Kowalski',
        'emergency_contact_phone': '+1-555-0602', 'consent_signed': True,
    },
    # index 6 — BUG Cat-A: consent_signed=False
    {
        'first_name': 'Amara', 'last_name': 'Mensah',
        'date_of_birth': '03/12/1988', 'gender': 'F',
        'medical_record_number': 'MRN-10007', 'national_id': 'NID-881267',
        'email': 'amara.mensah@email.com', 'phone': '+1-555-0701',
        'address': '14 Walnut Street, San Diego, CA 92101',
        'blood_group': 'B-', 'weight_kg': '67', 'height_cm': '170',
        'diagnosis': 'Insulin-dependent diabetes mellitus with retinopathy',
        'trial_assignment': 'TRIAL-003', 'enrollment_date': '22/03/2024',
        'status': 'active', 'emergency_contact_name': 'Kwame Mensah',
        'emergency_contact_phone': '+1-555-0702', 'consent_signed': False,  # BUG Cat-A
    },
    # index 7
    {
        'first_name': 'Richard', 'last_name': 'Ashworth',
        'date_of_birth': '25/04/1955', 'gender': 'M',
        'medical_record_number': 'MRN-10008', 'national_id': 'NID-550489',
        'email': 'richard.ashworth@email.com', 'phone': '+1-555-0801',
        'address': '7 Spruce Boulevard, Dallas, TX 75201',
        'blood_group': 'AB-', 'weight_kg': '79', 'height_cm': '172',
        'diagnosis': 'Alzheimer\'s disease, mild cognitive impairment stage',
        'trial_assignment': 'TRIAL-004', 'enrollment_date': '01/04/2024',
        'status': 'active', 'emergency_contact_name': 'Margaret Ashworth',
        'emergency_contact_phone': '+1-555-0802', 'consent_signed': True,
    },
    # index 8 — BUG Cat-E: email="xyz@@domain"
    {
        'first_name': 'Yuki', 'last_name': 'Tanaka',
        'date_of_birth': '11/06/1993', 'gender': 'F',
        'medical_record_number': 'MRN-10009', 'national_id': 'NID-930611',
        'email': 'xyz@@domain',  # BUG Cat-E
        'phone': '+1-555-0901',
        'address': '31 Aspen Way, San Jose, CA 95101',
        'blood_group': 'A+', 'weight_kg': '55', 'height_cm': '160',
        'diagnosis': 'Atrial fibrillation with rapid ventricular response',
        'trial_assignment': 'TRIAL-001', 'enrollment_date': '08/04/2024',
        'status': 'withdrawn', 'emergency_contact_name': 'Hiroshi Tanaka',
        'emergency_contact_phone': '+1-555-0902', 'consent_signed': True,
    },
    # index 9
    {
        'first_name': 'Carlos', 'last_name': 'Reyes',
        'date_of_birth': '07/02/1979', 'gender': 'M',
        'medical_record_number': 'MRN-10010', 'national_id': 'NID-790207',
        'email': 'carlos.reyes@email.com', 'phone': '+1-555-1001',
        'address': '56 Hickory Lane, Jacksonville, FL 32201',
        'blood_group': 'O+', 'weight_kg': '91', 'height_cm': '183',
        'diagnosis': 'Multiple sclerosis, relapsing-remitting form',
        'trial_assignment': 'TRIAL-004', 'enrollment_date': '15/04/2024',
        'status': 'active', 'emergency_contact_name': 'Maria Reyes',
        'emergency_contact_phone': '+1-555-1002', 'consent_signed': True,
    },
]


# 30 VisitLog records — 3 per patient
# Bugs: some protocol_deviation=True + deviation_notes="" (Cat-A/F), some systolic_bp="normal" (Cat-D)
VISIT_DATA = [
    # Patient 0 visits
    {'visit_number': 'V-001', 'visit_date': '10/01/2024', 'visit_type': 'screening',
     'investigator_name': 'Dr. Helen Carter', 'systolic_bp': '128', 'diastolic_bp': '82',
     'heart_rate': '74', 'body_temperature': '36.8', 'oxygen_saturation': '98',
     'visit_notes': 'Initial screening. Patient tolerated procedure well.',
     'next_visit_date': '10/02/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    {'visit_number': 'V-002', 'visit_date': '10/02/2024', 'visit_type': 'baseline',
     'investigator_name': 'Dr. Helen Carter', 'systolic_bp': '132', 'diastolic_bp': '85',
     'heart_rate': '76', 'body_temperature': '36.7', 'oxygen_saturation': '97',
     'visit_notes': 'Baseline vitals recorded. ECG normal.',
     'next_visit_date': '10/03/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    {'visit_number': 'V-003', 'visit_date': '10/03/2024', 'visit_type': 'followup',
     'investigator_name': 'Dr. Helen Carter', 'systolic_bp': '125', 'diastolic_bp': '80',
     'heart_rate': '72', 'body_temperature': '36.6', 'oxygen_saturation': '99',
     'visit_notes': 'Follow-up. BP improving on current regimen.',
     'next_visit_date': '10/04/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    # Patient 1 visits
    {'visit_number': 'V-001', 'visit_date': '15/02/2024', 'visit_type': 'screening',
     'investigator_name': 'Dr. Raj Patel', 'systolic_bp': '118', 'diastolic_bp': '76',
     'heart_rate': '80', 'body_temperature': '37.1', 'oxygen_saturation': '96',
     'visit_notes': 'Oncology screening. CT scan ordered.',
     'next_visit_date': '15/03/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    {'visit_number': 'V-002', 'visit_date': '15/03/2024', 'visit_type': 'baseline',
     'investigator_name': 'Dr. Raj Patel', 'systolic_bp': 'normal', 'diastolic_bp': '78',  # BUG Cat-D
     'heart_rate': '82', 'body_temperature': '37.0', 'oxygen_saturation': '95',
     'visit_notes': 'Baseline. Chemotherapy cycle 1 initiated.',
     'next_visit_date': '15/04/2024', 'protocol_deviation': True, 'deviation_notes': ''},  # BUG Cat-A/F
    {'visit_number': 'V-003', 'visit_date': '15/04/2024', 'visit_type': 'followup',
     'investigator_name': 'Dr. Raj Patel', 'systolic_bp': '120', 'diastolic_bp': '77',
     'heart_rate': '79', 'body_temperature': '36.9', 'oxygen_saturation': '96',
     'visit_notes': 'Post-chemo follow-up. Nausea reported.',
     'next_visit_date': '15/05/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    # Patient 2 visits
    {'visit_number': 'V-001', 'visit_date': '25/02/2024', 'visit_type': 'screening',
     'investigator_name': 'Dr. Susan Lee', 'systolic_bp': '135', 'diastolic_bp': '88',
     'heart_rate': '88', 'body_temperature': '36.5', 'oxygen_saturation': '97',
     'visit_notes': 'Diabetes screening. HbA1c elevated.',
     'next_visit_date': '25/03/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    {'visit_number': 'V-002', 'visit_date': '25/03/2024', 'visit_type': 'baseline',
     'investigator_name': 'Dr. Susan Lee', 'systolic_bp': '138', 'diastolic_bp': '90',
     'heart_rate': '90', 'body_temperature': '36.6', 'oxygen_saturation': '97',
     'visit_notes': 'Baseline. Insulin dosage adjusted.',
     'next_visit_date': '25/04/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    {'visit_number': 'V-003', 'visit_date': '25/04/2024', 'visit_type': 'followup',
     'investigator_name': 'Dr. Susan Lee', 'systolic_bp': '130', 'diastolic_bp': '85',
     'heart_rate': '85', 'body_temperature': '36.7', 'oxygen_saturation': '98',
     'visit_notes': 'Follow-up. Glucose levels stabilising.',
     'next_visit_date': '25/05/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    # Patient 3 visits
    {'visit_number': 'V-001', 'visit_date': '05/03/2024', 'visit_type': 'screening',
     'investigator_name': 'Dr. Michael Obi', 'systolic_bp': '122', 'diastolic_bp': '79',
     'heart_rate': '68', 'body_temperature': '36.4', 'oxygen_saturation': '98',
     'visit_notes': 'Neurology screening. UPDRS score recorded.',
     'next_visit_date': '05/04/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    {'visit_number': 'V-002', 'visit_date': '05/04/2024', 'visit_type': 'baseline',
     'investigator_name': 'Dr. Michael Obi', 'systolic_bp': '124', 'diastolic_bp': '80',
     'heart_rate': '70', 'body_temperature': '36.5', 'oxygen_saturation': '98',
     'visit_notes': 'Baseline. Levodopa therapy commenced.',
     'next_visit_date': '05/05/2024', 'protocol_deviation': True, 'deviation_notes': ''},  # BUG Cat-A/F
    {'visit_number': 'V-003', 'visit_date': '05/05/2024', 'visit_type': 'followup',
     'investigator_name': 'Dr. Michael Obi', 'systolic_bp': '120', 'diastolic_bp': '78',
     'heart_rate': '69', 'body_temperature': '36.6', 'oxygen_saturation': '99',
     'visit_notes': 'Follow-up. Tremor frequency reduced.',
     'next_visit_date': '05/06/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    # Patient 4 visits
    {'visit_number': 'V-001', 'visit_date': '12/03/2024', 'visit_type': 'screening',
     'investigator_name': 'Dr. Helen Carter', 'systolic_bp': '145', 'diastolic_bp': '92',
     'heart_rate': '84', 'body_temperature': '36.9', 'oxygen_saturation': '97',
     'visit_notes': 'Cardiology screening. Stress test scheduled.',
     'next_visit_date': '12/04/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    {'visit_number': 'V-002', 'visit_date': '12/04/2024', 'visit_type': 'baseline',
     'investigator_name': 'Dr. Helen Carter', 'systolic_bp': '142', 'diastolic_bp': '90',
     'heart_rate': '82', 'body_temperature': '36.8', 'oxygen_saturation': '97',
     'visit_notes': 'Baseline. Nitrate therapy initiated.',
     'next_visit_date': '12/05/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    {'visit_number': 'V-003', 'visit_date': '12/05/2024', 'visit_type': 'followup',
     'investigator_name': 'Dr. Helen Carter', 'systolic_bp': 'normal', 'diastolic_bp': '88',  # BUG Cat-D
     'heart_rate': '80', 'body_temperature': '36.7', 'oxygen_saturation': '98',
     'visit_notes': 'Follow-up. Angina episodes reduced.',
     'next_visit_date': '12/06/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    # Patient 5 visits
    {'visit_number': 'V-001', 'visit_date': '18/03/2024', 'visit_type': 'screening',
     'investigator_name': 'Dr. Raj Patel', 'systolic_bp': '115', 'diastolic_bp': '74',
     'heart_rate': '77', 'body_temperature': '37.2', 'oxygen_saturation': '95',
     'visit_notes': 'Lymphoma screening. PET scan ordered.',
     'next_visit_date': '18/04/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    {'visit_number': 'V-002', 'visit_date': '18/04/2024', 'visit_type': 'baseline',
     'investigator_name': 'Dr. Raj Patel', 'systolic_bp': '117', 'diastolic_bp': '75',
     'heart_rate': '78', 'body_temperature': '37.1', 'oxygen_saturation': '95',
     'visit_notes': 'Baseline. R-CHOP cycle 1 started.',
     'next_visit_date': '18/05/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    {'visit_number': 'V-003', 'visit_date': '18/05/2024', 'visit_type': 'followup',
     'investigator_name': 'Dr. Raj Patel', 'systolic_bp': '116', 'diastolic_bp': '74',
     'heart_rate': '76', 'body_temperature': '37.0', 'oxygen_saturation': '96',
     'visit_notes': 'Follow-up. Partial response noted on imaging.',
     'next_visit_date': '18/06/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    # Patient 6 visits
    {'visit_number': 'V-001', 'visit_date': '25/03/2024', 'visit_type': 'screening',
     'investigator_name': 'Dr. Susan Lee', 'systolic_bp': '140', 'diastolic_bp': '89',
     'heart_rate': '92', 'body_temperature': '36.8', 'oxygen_saturation': '97',
     'visit_notes': 'Diabetes screening. Retinal exam performed.',
     'next_visit_date': '25/04/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    {'visit_number': 'V-002', 'visit_date': '25/04/2024', 'visit_type': 'baseline',
     'investigator_name': 'Dr. Susan Lee', 'systolic_bp': '138', 'diastolic_bp': '87',
     'heart_rate': '90', 'body_temperature': '36.7', 'oxygen_saturation': '97',
     'visit_notes': 'Baseline. Insulin pump initiated.',
     'next_visit_date': '25/05/2024', 'protocol_deviation': True, 'deviation_notes': ''},  # BUG Cat-A/F
    {'visit_number': 'V-003', 'visit_date': '25/05/2024', 'visit_type': 'followup',
     'investigator_name': 'Dr. Susan Lee', 'systolic_bp': '133', 'diastolic_bp': '84',
     'heart_rate': '87', 'body_temperature': '36.6', 'oxygen_saturation': '98',
     'visit_notes': 'Follow-up. HbA1c improved to 7.2%.',
     'next_visit_date': '25/06/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    # Patient 7 visits
    {'visit_number': 'V-001', 'visit_date': '05/04/2024', 'visit_type': 'screening',
     'investigator_name': 'Dr. Michael Obi', 'systolic_bp': '119', 'diastolic_bp': '77',
     'heart_rate': '65', 'body_temperature': '36.3', 'oxygen_saturation': '99',
     'visit_notes': 'Alzheimer screening. MMSE score 22/30.',
     'next_visit_date': '05/05/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    {'visit_number': 'V-002', 'visit_date': '05/05/2024', 'visit_type': 'baseline',
     'investigator_name': 'Dr. Michael Obi', 'systolic_bp': '121', 'diastolic_bp': '78',
     'heart_rate': '66', 'body_temperature': '36.4', 'oxygen_saturation': '99',
     'visit_notes': 'Baseline. Donepezil 5mg commenced.',
     'next_visit_date': '05/06/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    {'visit_number': 'V-003', 'visit_date': '05/06/2024', 'visit_type': 'followup',
     'investigator_name': 'Dr. Michael Obi', 'systolic_bp': '118', 'diastolic_bp': '76',
     'heart_rate': '67', 'body_temperature': '36.5', 'oxygen_saturation': '99',
     'visit_notes': 'Follow-up. Caregiver reports improved recall.',
     'next_visit_date': '05/07/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    # Patient 8 visits
    {'visit_number': 'V-001', 'visit_date': '10/04/2024', 'visit_type': 'screening',
     'investigator_name': 'Dr. Helen Carter', 'systolic_bp': '155', 'diastolic_bp': '95',
     'heart_rate': '110', 'body_temperature': '36.9', 'oxygen_saturation': '96',
     'visit_notes': 'Cardiology screening. Holter monitor applied.',
     'next_visit_date': '10/05/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    {'visit_number': 'V-002', 'visit_date': '10/05/2024', 'visit_type': 'baseline',
     'investigator_name': 'Dr. Helen Carter', 'systolic_bp': '150', 'diastolic_bp': '93',
     'heart_rate': '105', 'body_temperature': '36.8', 'oxygen_saturation': '96',
     'visit_notes': 'Baseline. Rate control with metoprolol initiated.',
     'next_visit_date': '10/06/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    {'visit_number': 'V-003', 'visit_date': '10/06/2024', 'visit_type': 'followup',
     'investigator_name': 'Dr. Helen Carter', 'systolic_bp': '145', 'diastolic_bp': '90',
     'heart_rate': '98', 'body_temperature': '36.7', 'oxygen_saturation': '97',
     'visit_notes': 'Follow-up. Heart rate better controlled.',
     'next_visit_date': '', 'protocol_deviation': False, 'deviation_notes': ''},
    # Patient 9 visits
    {'visit_number': 'V-001', 'visit_date': '18/04/2024', 'visit_type': 'screening',
     'investigator_name': 'Dr. Michael Obi', 'systolic_bp': '126', 'diastolic_bp': '81',
     'heart_rate': '73', 'body_temperature': '36.6', 'oxygen_saturation': '98',
     'visit_notes': 'MS screening. MRI brain with gadolinium ordered.',
     'next_visit_date': '18/05/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    {'visit_number': 'V-002', 'visit_date': '18/05/2024', 'visit_type': 'baseline',
     'investigator_name': 'Dr. Michael Obi', 'systolic_bp': '128', 'diastolic_bp': '82',
     'heart_rate': '74', 'body_temperature': '36.5', 'oxygen_saturation': '98',
     'visit_notes': 'Baseline. Interferon beta-1a initiated.',
     'next_visit_date': '18/06/2024', 'protocol_deviation': False, 'deviation_notes': ''},
    {'visit_number': 'V-003', 'visit_date': '18/06/2024', 'visit_type': 'followup',
     'investigator_name': 'Dr. Michael Obi', 'systolic_bp': '125', 'diastolic_bp': '80',
     'heart_rate': '72', 'body_temperature': '36.4', 'oxygen_saturation': '99',
     'visit_notes': 'Follow-up. Relapse frequency reduced.',
     'next_visit_date': '18/07/2024', 'protocol_deviation': False, 'deviation_notes': ''},
]


# 20 LabResult records — 2 per patient
# Bugs: some abnormal_flag="critical" + remarks="" (Cat-F), some result_value="positive" (Cat-D)
LAB_DATA = [
    # Patient 0
    {'sample_collection_date': '10/01/2024', 'sample_type': 'blood', 'test_name': 'Complete Blood Count',
     'result_value': '4.8', 'unit': '10^9/L', 'reference_range_low': '4.0', 'reference_range_high': '11.0',
     'abnormal_flag': 'normal', 'lab_technician': 'T. Williams', 'lab_name': 'Boston General Lab', 'remarks': ''},
    {'sample_collection_date': '10/02/2024', 'sample_type': 'blood', 'test_name': 'Lipid Panel',
     'result_value': '6.8', 'unit': 'mmol/L', 'reference_range_low': '0', 'reference_range_high': '5.2',
     'abnormal_flag': 'critical', 'lab_technician': 'T. Williams', 'lab_name': 'Boston General Lab', 'remarks': ''},  # BUG Cat-F
    # Patient 1
    {'sample_collection_date': '15/02/2024', 'sample_type': 'blood', 'test_name': 'Tumour Marker CA-125',
     'result_value': 'positive', 'unit': 'U/mL', 'reference_range_low': '0', 'reference_range_high': '35',  # BUG Cat-D
     'abnormal_flag': 'abnormal', 'lab_technician': 'K. Johnson', 'lab_name': 'Chicago Oncology Lab', 'remarks': 'Elevated marker noted'},
    {'sample_collection_date': '15/03/2024', 'sample_type': 'blood', 'test_name': 'Liver Function Test',
     'result_value': '52', 'unit': 'U/L', 'reference_range_low': '7', 'reference_range_high': '40',
     'abnormal_flag': 'critical', 'lab_technician': 'K. Johnson', 'lab_name': 'Chicago Oncology Lab', 'remarks': ''},  # BUG Cat-F
    # Patient 2
    {'sample_collection_date': '25/02/2024', 'sample_type': 'blood', 'test_name': 'HbA1c',
     'result_value': '9.2', 'unit': '%', 'reference_range_low': '4.0', 'reference_range_high': '5.6',
     'abnormal_flag': 'abnormal', 'lab_technician': 'R. Singh', 'lab_name': 'Houston Diabetes Centre', 'remarks': 'Poor glycaemic control'},
    {'sample_collection_date': '25/03/2024', 'sample_type': 'blood', 'test_name': 'Fasting Glucose',
     'result_value': '11.4', 'unit': 'mmol/L', 'reference_range_low': '3.9', 'reference_range_high': '5.5',
     'abnormal_flag': 'abnormal', 'lab_technician': 'R. Singh', 'lab_name': 'Houston Diabetes Centre', 'remarks': 'Insulin adjustment required'},
    # Patient 3
    {'sample_collection_date': '05/03/2024', 'sample_type': 'blood', 'test_name': 'Dopamine Metabolites',
     'result_value': '0.31', 'unit': 'nmol/L', 'reference_range_low': '0.40', 'reference_range_high': '1.20',
     'abnormal_flag': 'abnormal', 'lab_technician': 'L. Brown', 'lab_name': 'Phoenix Neurology Lab', 'remarks': 'Reduced dopaminergic activity'},
    {'sample_collection_date': '05/04/2024', 'sample_type': 'blood', 'test_name': 'Serum Ferritin',
     'result_value': '12', 'unit': 'ng/mL', 'reference_range_low': '30', 'reference_range_high': '400',
     'abnormal_flag': 'critical', 'lab_technician': 'L. Brown', 'lab_name': 'Phoenix Neurology Lab', 'remarks': ''},  # BUG Cat-F
    # Patient 4
    {'sample_collection_date': '12/03/2024', 'sample_type': 'blood', 'test_name': 'Troponin I',
     'result_value': '0.08', 'unit': 'ng/mL', 'reference_range_low': '0', 'reference_range_high': '0.04',
     'abnormal_flag': 'abnormal', 'lab_technician': 'T. Williams', 'lab_name': 'Philadelphia Cardiac Lab', 'remarks': 'Mild elevation'},
    {'sample_collection_date': '12/04/2024', 'sample_type': 'blood', 'test_name': 'BNP',
     'result_value': 'positive', 'unit': 'pg/mL', 'reference_range_low': '0', 'reference_range_high': '100',  # BUG Cat-D
     'abnormal_flag': 'abnormal', 'lab_technician': 'T. Williams', 'lab_name': 'Philadelphia Cardiac Lab', 'remarks': 'Cardiac stress indicated'},
    # Patient 5
    {'sample_collection_date': '18/03/2024', 'sample_type': 'tissue', 'test_name': 'Lymph Node Biopsy',
     'result_value': 'positive', 'unit': 'N/A', 'reference_range_low': 'N/A', 'reference_range_high': 'N/A',  # BUG Cat-D
     'abnormal_flag': 'critical', 'lab_technician': 'K. Johnson', 'lab_name': 'San Antonio Pathology Lab', 'remarks': ''},  # BUG Cat-F
    {'sample_collection_date': '18/04/2024', 'sample_type': 'blood', 'test_name': 'LDH',
     'result_value': '620', 'unit': 'U/L', 'reference_range_low': '140', 'reference_range_high': '280',
     'abnormal_flag': 'abnormal', 'lab_technician': 'K. Johnson', 'lab_name': 'San Antonio Pathology Lab', 'remarks': 'Elevated in lymphoma'},
    # Patient 6
    {'sample_collection_date': '25/03/2024', 'sample_type': 'blood', 'test_name': 'HbA1c',
     'result_value': '8.7', 'unit': '%', 'reference_range_low': '4.0', 'reference_range_high': '5.6',
     'abnormal_flag': 'abnormal', 'lab_technician': 'R. Singh', 'lab_name': 'San Diego Diabetes Lab', 'remarks': 'Suboptimal control'},
    {'sample_collection_date': '25/04/2024', 'sample_type': 'urine', 'test_name': 'Microalbuminuria',
     'result_value': '185', 'unit': 'mg/24h', 'reference_range_low': '0', 'reference_range_high': '30',
     'abnormal_flag': 'critical', 'lab_technician': 'R. Singh', 'lab_name': 'San Diego Diabetes Lab', 'remarks': ''},  # BUG Cat-F
    # Patient 7
    {'sample_collection_date': '05/04/2024', 'sample_type': 'blood', 'test_name': 'Amyloid Beta 42',
     'result_value': '412', 'unit': 'pg/mL', 'reference_range_low': '500', 'reference_range_high': '1500',
     'abnormal_flag': 'abnormal', 'lab_technician': 'L. Brown', 'lab_name': 'Dallas Neurology Lab', 'remarks': 'Reduced — consistent with AD'},
    {'sample_collection_date': '05/05/2024', 'sample_type': 'csf', 'test_name': 'CSF Tau Protein',
     'result_value': '620', 'unit': 'pg/mL', 'reference_range_low': '0', 'reference_range_high': '300',
     'abnormal_flag': 'critical', 'lab_technician': 'L. Brown', 'lab_name': 'Dallas Neurology Lab', 'remarks': ''},  # BUG Cat-F
    # Patient 8
    {'sample_collection_date': '10/04/2024', 'sample_type': 'blood', 'test_name': 'INR / PT',
     'result_value': '2.8', 'unit': 'ratio', 'reference_range_low': '0.8', 'reference_range_high': '1.2',
     'abnormal_flag': 'abnormal', 'lab_technician': 'T. Williams', 'lab_name': 'San Jose Cardiac Lab', 'remarks': 'Anticoagulation therapy'},
    {'sample_collection_date': '10/05/2024', 'sample_type': 'blood', 'test_name': 'TSH',
     'result_value': '0.08', 'unit': 'mIU/L', 'reference_range_low': '0.4', 'reference_range_high': '4.0',
     'abnormal_flag': 'critical', 'lab_technician': 'T. Williams', 'lab_name': 'San Jose Cardiac Lab', 'remarks': ''},  # BUG Cat-F
    # Patient 9
    {'sample_collection_date': '18/04/2024', 'sample_type': 'csf', 'test_name': 'Oligoclonal Bands',
     'result_value': 'positive', 'unit': 'N/A', 'reference_range_low': 'N/A', 'reference_range_high': 'N/A',  # BUG Cat-D
     'abnormal_flag': 'abnormal', 'lab_technician': 'L. Brown', 'lab_name': 'Jacksonville Neurology Lab', 'remarks': 'Consistent with MS'},
    {'sample_collection_date': '18/05/2024', 'sample_type': 'blood', 'test_name': 'Vitamin D',
     'result_value': '18', 'unit': 'ng/mL', 'reference_range_low': '30', 'reference_range_high': '100',
     'abnormal_flag': 'abnormal', 'lab_technician': 'L. Brown', 'lab_name': 'Jacksonville Neurology Lab', 'remarks': 'Supplementation recommended'},
]


# 5 AdverseEvent records
# Bugs:
#   AE 0: is_sae=True + sae_report_number="" (Cat-A/F)
#   AE 1: is_sae=True + sae_report_number="" (Cat-A/F)
#   AE 2: resolution_date="01/01/2020" before onset_date="15/06/2020" (Cat-F)
#   AE 3: event_description="" (Cat-A)
AE_DATA = [
    {
        'patient_mrn': 'MRN-10002',
        'event_title': 'Grade 3 Neutropenia',
        'onset_date': '20/03/2024', 'resolution_date': '05/04/2024',
        'severity': 'severe', 'causality': 'related',
        'event_description': 'Patient developed severe neutropenia following cycle 1 chemotherapy. ANC dropped to 0.4 x10^9/L. G-CSF administered.',
        'action_taken': 'dose_reduced', 'outcome': 'recovering',
        'is_sae': True, 'sae_report_number': '',  # BUG Cat-A/F
        'reported_by': 'Dr. Raj Patel', 'report_date': '21/03/2024',
        'regulatory_reported': False,
    },
    {
        'patient_mrn': 'MRN-10005',
        'event_title': 'Acute Myocardial Infarction',
        'onset_date': '02/04/2024', 'resolution_date': '15/04/2024',
        'severity': 'life_threatening', 'causality': 'possible',
        'event_description': 'Patient experienced STEMI requiring emergency PCI. Possible relation to study drug vasodilatory effect.',
        'action_taken': 'hospitalized', 'outcome': 'recovering',
        'is_sae': True, 'sae_report_number': '',  # BUG Cat-A/F
        'reported_by': 'Dr. Helen Carter', 'report_date': '02/04/2024',
        'regulatory_reported': False,
    },
    {
        'patient_mrn': 'MRN-10003',
        'event_title': 'Hypoglycaemic Episode',
        'onset_date': '15/06/2020', 'resolution_date': '01/01/2020',  # BUG Cat-F: resolution before onset
        'severity': 'moderate', 'causality': 'related',
        'event_description': 'Patient reported dizziness and diaphoresis. Blood glucose 2.1 mmol/L. Resolved with oral glucose.',
        'action_taken': 'dose_reduced', 'outcome': 'recovered',
        'is_sae': False, 'sae_report_number': '',
        'reported_by': 'Dr. Susan Lee', 'report_date': '16/06/2020',
        'regulatory_reported': False,
    },
    {
        'patient_mrn': 'MRN-10007',
        'event_title': 'Injection Site Reaction',
        'onset_date': '30/04/2024', 'resolution_date': '07/05/2024',
        'severity': 'mild', 'causality': 'related',
        'event_description': '',  # BUG Cat-A
        'action_taken': 'none', 'outcome': 'recovered',
        'is_sae': False, 'sae_report_number': '',
        'reported_by': 'Dr. Susan Lee', 'report_date': '30/04/2024',
        'regulatory_reported': False,
    },
    {
        'patient_mrn': 'MRN-10010',
        'event_title': 'Flu-like Syndrome',
        'onset_date': '25/05/2024', 'resolution_date': '01/06/2024',
        'severity': 'mild', 'causality': 'probable',
        'event_description': 'Patient reported fever (38.2°C), myalgia, and fatigue within 24 hours of interferon injection. Managed with paracetamol.',
        'action_taken': 'none', 'outcome': 'recovered',
        'is_sae': False, 'sae_report_number': '',
        'reported_by': 'Dr. Michael Obi', 'report_date': '25/05/2024',
        'regulatory_reported': False,
    },
]


class Command(BaseCommand):
    help = 'Seed clinical trial data: patients, visits, lab results, adverse events'

    def handle(self, *args, **options):
        try:
            coordinator = CTMSUser.objects.get(email='coordinator1@ctms.com')
        except CTMSUser.DoesNotExist:
            raise CommandError(
                'coordinator1@ctms.com not found. Run seed_users first: '
                'python manage.py seed_users'
            )

        # ── Patients ──────────────────────────────────────────────────────────
        self.stdout.write('Seeding patients...')
        patients = []
        for data in PATIENT_DATA:
            patient, created = Patient.objects.get_or_create(
                medical_record_number=data['medical_record_number'],
                defaults={**data, 'created_by': coordinator},
            )
            patients.append(patient)
            status = 'Created' if created else 'Exists '
            self.stdout.write(f'  [{status}] Patient {patient.medical_record_number} — {patient.first_name} {patient.last_name}')

        # ── Visits ────────────────────────────────────────────────────────────
        self.stdout.write('Seeding visit logs...')
        for i, vdata in enumerate(VISIT_DATA):
            patient = patients[i // 3]
            _, created = VisitLog.objects.get_or_create(
                patient=patient,
                visit_number=vdata['visit_number'],
                visit_date=vdata['visit_date'],
                defaults={
                    'visit_type': vdata['visit_type'],
                    'investigator_name': vdata['investigator_name'],
                    'coordinator': coordinator,
                    'systolic_bp': vdata['systolic_bp'],
                    'diastolic_bp': vdata['diastolic_bp'],
                    'heart_rate': vdata['heart_rate'],
                    'body_temperature': vdata['body_temperature'],
                    'oxygen_saturation': vdata['oxygen_saturation'],
                    'visit_notes': vdata['visit_notes'],
                    'next_visit_date': vdata['next_visit_date'],
                    'protocol_deviation': vdata['protocol_deviation'],
                    'deviation_notes': vdata['deviation_notes'],
                    'created_by': coordinator,
                },
            )
            status = 'Created' if created else 'Exists '
            self.stdout.write(f'  [{status}] Visit {vdata["visit_number"]} for {patient.medical_record_number} on {vdata["visit_date"]}')

        # ── Lab Results ───────────────────────────────────────────────────────
        self.stdout.write('Seeding lab results...')
        for i, ldata in enumerate(LAB_DATA):
            patient = patients[i // 2]
            _, created = LabResult.objects.get_or_create(
                patient=patient,
                test_name=ldata['test_name'],
                sample_collection_date=ldata['sample_collection_date'],
                defaults={
                    'sample_type': ldata['sample_type'],
                    'result_value': ldata['result_value'],
                    'unit': ldata['unit'],
                    'reference_range_low': ldata['reference_range_low'],
                    'reference_range_high': ldata['reference_range_high'],
                    'abnormal_flag': ldata['abnormal_flag'],
                    'lab_technician': ldata['lab_technician'],
                    'lab_name': ldata['lab_name'],
                    'remarks': ldata['remarks'],
                    'created_by': coordinator,
                },
            )
            status = 'Created' if created else 'Exists '
            self.stdout.write(f'  [{status}] Lab "{ldata["test_name"]}" for {patient.medical_record_number}')

        # ── Adverse Events ────────────────────────────────────────────────────
        self.stdout.write('Seeding adverse events...')
        for aedata in AE_DATA:
            mrn = aedata.pop('patient_mrn')
            try:
                patient = Patient.objects.get(medical_record_number=mrn)
            except Patient.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  [Skip] Patient {mrn} not found'))
                continue

            _, created = AdverseEvent.objects.get_or_create(
                patient=patient,
                event_title=aedata['event_title'],
                onset_date=aedata['onset_date'],
                defaults={**aedata, 'created_by': coordinator},
            )
            status = 'Created' if created else 'Exists '
            self.stdout.write(f'  [{status}] AE "{aedata["event_title"]}" for {mrn}')

        self.stdout.write(self.style.SUCCESS(
            '\nseed_data complete: 10 patients, 30 visits, 20 lab results, 5 adverse events.'
        ))
