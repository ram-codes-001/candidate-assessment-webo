from django.contrib.auth.models import AbstractUser
from django.db import models


class CTMSUser(AbstractUser):
    ROLE_CHOICES = [('coordinator', 'Coordinator'), ('admin', 'Admin')]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='coordinator')
    employee_id = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
