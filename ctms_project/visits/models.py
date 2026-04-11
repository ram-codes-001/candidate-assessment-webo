from django.db import models

VISIT_TYPE_CHOICES = [
    ('screening', 'Screening'), ('baseline', 'Baseline'),
    ('followup', 'Follow-up'), ('final', 'Final Visit'), ('unscheduled', 'Unscheduled'),
]

class VisitLog(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='visits')
    visit_number = models.CharField(max_length=20)           # BUG Cat-E: accepts "V@#!"
    visit_date = models.CharField(max_length=50)             # BUG Cat-C: should be DateField
    visit_type = models.CharField(max_length=20, choices=VISIT_TYPE_CHOICES)
    investigator_name = models.CharField(max_length=100)
    coordinator = models.ForeignKey(
        'accounts.CTMSUser', on_delete=models.SET_NULL, null=True, related_name='visits'
    )
    # Vitals — BUG Cat-D: all CharField, should be numeric types
    systolic_bp = models.CharField(max_length=20)
    diastolic_bp = models.CharField(max_length=20)
    heart_rate = models.CharField(max_length=20)
    body_temperature = models.CharField(max_length=20)
    oxygen_saturation = models.CharField(max_length=20)
    visit_notes = models.TextField(blank=True)
    next_visit_date = models.CharField(max_length=50, blank=True)  # BUG Cat-C/F
    protocol_deviation = models.BooleanField(default=False)
    deviation_notes = models.TextField(blank=True)           # BUG Cat-A/F
    created_by = models.ForeignKey(
        'accounts.CTMSUser', on_delete=models.SET_NULL, null=True, related_name='visits_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient} — {self.visit_number} ({self.visit_date})"

    class Meta:
        ordering = ['-created_at']
