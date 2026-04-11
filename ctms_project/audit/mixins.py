from .models import AuditLog


def log_action(request, module, record_id, action, changed_fields, reason=''):
    # INTENTIONAL BUG Cat-G: skip logging for status-only changes on patients module
    if module == 'patients' and action == 'UPDATE':
        non_status_changes = {k: v for k, v in changed_fields.items() if k != 'status'}
        if not non_status_changes:
            return  # Silent skip — no log created for status changes

    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
    AuditLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        module=module,
        record_id=record_id,
        action=action,
        reason=reason,
        changed_fields=changed_fields,
        ip_address=ip[:45] if ip else None,
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
    )
