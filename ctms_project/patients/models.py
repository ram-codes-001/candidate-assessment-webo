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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.CharField(max_length=50)           # BUG Cat-C
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    medical_record_number = models.CharField(max_length=50)   # BUG Cat-E
    national_id = models.CharField(max_length=50)             # BUG Cat-E
    email = models.CharField(max_length=200)                  # BUG Cat-E
    phone = models.CharField(max_length=50)                   # BUG Cat-E
    address = models.TextField(blank=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    weight_kg = models.CharField(max_length=20)               # BUG Cat-D
    height_cm = models.CharField(max_length=20)               # BUG Cat-D
    diagnosis = models.TextField()                            # BUG Cat-A: blank=True in form only
    trial_assignment = models.CharField(max_length=50, choices=TRIAL_CHOICES)
    enrollment_date = models.CharField(max_length=50)         # BUG Cat-C
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    emergency_contact_name = models.CharField(max_length=100) # BUG Cat-B
    emergency_contact_phone = models.CharField(max_length=50) # BUG Cat-B
    consent_signed = models.BooleanField(default=False)       # BUG Cat-A
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
