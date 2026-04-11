from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import get_user_model

from .models import AuditLog

User = get_user_model()


@login_required
def audit_trail(request):
    logs = AuditLog.objects.select_related('user')

    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    user_id = request.GET.get('user_id')
    module = request.GET.get('module')
    action = request.GET.get('action')

    if date_from:
        logs = logs.filter(timestamp__date__gte=date_from)
    if date_to:
        logs = logs.filter(timestamp__date__lte=date_to)
    if user_id:
        logs = logs.filter(user_id=user_id)
    if module:
        logs = logs.filter(module=module)
    if action:
        logs = logs.filter(action=action)

    users = User.objects.all()
    modules = AuditLog.objects.values_list('module', flat=True).distinct()
    from .models import ACTION_CHOICES

    context = {
        'logs': logs,
        'users': users,
        'modules': modules,
        'action_choices': ACTION_CHOICES,
        'filters': {
            'date_from': date_from or '',
            'date_to': date_to or '',
            'user_id': user_id or '',
            'module': module or '',
            'action': action or '',
        },
    }
    return render(request, 'audit/trail.html', context)


@login_required
def patient_audit_trail(request, patient_id):
    logs = AuditLog.objects.select_related('user').filter(
        module='patients', record_id=patient_id
    )
    context = {'logs': logs, 'patient_id': patient_id}
    return render(request, 'audit/trail.html', context)


@login_required
def module_audit_trail(request, module_name):
    logs = AuditLog.objects.select_related('user').filter(module=module_name)
    context = {'logs': logs, 'module_name': module_name}
    return render(request, 'audit/trail.html', context)
