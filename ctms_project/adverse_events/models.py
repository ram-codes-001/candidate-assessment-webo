from django.db import models

SEVERITY_CHOICES = [
    ('mild', 'Mild'), ('moderate', 'Moderate'),
    ('severe', 'Severe'), ('life_threatening', 'Life-Threatening'),
]
CAUSALITY_CHOICES = [
    ('related', 'Related'), ('unrelated', 'Unrelated'),
    ('possible', 'Possible'), ('probable', 'Probable'),
]
ACTION_CHOICES = [
    ('none', 'None'), ('dose_reduced', 'Dose Reduced'),
    ('drug_stopped', 'Drug Stopped'), ('hospitalized', 'Hospitalized'),
]
OUTCOME_CHOICES = [
    ('recovered', 'Recovered'), ('recovering', 'Recovering'),
    ('ongoing', 'Ongoing'), ('fatal', 'Fatal'), ('unknown', 'Unknown'),
]


class AdverseEvent(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='adverse_events')
    event_title = models.CharField(max_length=200)
    onset_date = models.CharField(max_length=50)             # BUG Cat-C
    resolution_date = models.CharField(max_length=50, blank=True)  # BUG Cat-C/F
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    causality = models.CharField(max_length=20, choices=CAUSALITY_CHOICES)
    event_description = models.TextField(blank=True)         # BUG Cat-A
    action_taken = models.CharField(max_length=20, choices=ACTION_CHOICES)
    outcome = models.CharField(max_length=20, choices=OUTCOME_CHOICES)
    is_sae = models.BooleanField(default=False)
    sae_report_number = models.CharField(max_length=50, blank=True)  # BUG Cat-A/F
    reported_by = models.CharField(max_length=100)
    report_date = models.CharField(max_length=50)            # BUG Cat-C
    regulatory_reported = models.BooleanField(default=False)
    attachment = models.FileField(upload_to='ae_attachments/', blank=True, null=True)
    # BUG: No file type validation — accepts .exe, .js, .bat, .sh
    created_by = models.ForeignKey(
        'accounts.CTMSUser', on_delete=models.SET_NULL, null=True, related_name='ae_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient} — {self.event_title}"

    class Meta:
        ordering = ['-created_at']
