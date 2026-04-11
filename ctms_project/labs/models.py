from django.db import models

SAMPLE_TYPE_CHOICES = [('blood', 'Blood'), ('urine', 'Urine'), ('tissue', 'Tissue'), ('csf', 'CSF')]
ABNORMAL_FLAG_CHOICES = [('normal', 'Normal'), ('abnormal', 'Abnormal'), ('critical', 'Critical')]


class LabResult(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='lab_results')
    visit = models.ForeignKey('visits.VisitLog', on_delete=models.SET_NULL, null=True, blank=True, related_name='lab_results')
    sample_collection_date = models.CharField(max_length=50)  # BUG Cat-C
    sample_type = models.CharField(max_length=20, choices=SAMPLE_TYPE_CHOICES)
    test_name = models.CharField(max_length=200)
    result_value = models.CharField(max_length=100)           # BUG Cat-D
    unit = models.CharField(max_length=50)                    # BUG Cat-D: free text
    reference_range_low = models.CharField(max_length=50)     # BUG Cat-D
    reference_range_high = models.CharField(max_length=50)    # BUG Cat-D
    abnormal_flag = models.CharField(max_length=20, choices=ABNORMAL_FLAG_CHOICES, default='normal')
    lab_technician = models.CharField(max_length=100)
    lab_name = models.CharField(max_length=200)
    remarks = models.TextField(blank=True)                    # BUG Cat-F: critical flag doesn't require remarks
    created_by = models.ForeignKey(
        'accounts.CTMSUser', on_delete=models.SET_NULL, null=True, related_name='labs_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient} — {self.test_name} ({self.sample_collection_date})"

    class Meta:
        ordering = ['-created_at']
