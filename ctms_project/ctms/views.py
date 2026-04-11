"""
CTMS project-level views (dashboard).
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@login_required
def dashboard(request):
    from patients.models import Patient
    from adverse_events.models import AdverseEvent
    from visits.models import VisitLog
    now = timezone.now()
    context = {
        'total_patients': Patient.objects.count(),
        'open_aes': AdverseEvent.objects.filter(outcome__in=['ongoing', 'recovering']).count(),
        'visits_this_month': VisitLog.objects.filter(
            created_at__year=now.year, created_at__month=now.month
        ).count(),
        'recent_patients': Patient.objects.order_by('-created_at')[:5],
        'recent_aes': AdverseEvent.objects.select_related('patient').order_by('-created_at')[:5],
    }
    return render(request, 'dashboard.html', context)
