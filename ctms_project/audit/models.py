from django.db import models

ACTION_CHOICES = [
    ('CREATE', 'Create'), ('UPDATE', 'Update'), ('DELETE', 'Delete'),
    ('LOGIN', 'Login'), ('LOGOUT', 'Logout'), ('EXPORT', 'Export'),
]


class AuditLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        'accounts.CTMSUser', on_delete=models.SET_NULL,
        null=True, related_name='audit_logs'
    )
    module = models.CharField(max_length=50)
    record_id = models.IntegerField(null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    reason = models.TextField(blank=True)
    changed_fields = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    # BUG Cat-G: Status-only changes on Patient module are silently skipped in log_action()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.timestamp}] {self.user} — {self.action} on {self.module}#{self.record_id}"
