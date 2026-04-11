from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Patient
from .forms import PatientForm
from audit.mixins import log_action
from audit.models import AuditLog
from visits.models import VisitLog
from labs.models import LabResult
from adverse_events.models import AdverseEvent

@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.created_by = request.user
            patient.save()
            log_action(request, 'patients', patient.id, 'CREATE', {})
            messages.success(request, 'Patient registered successfully.')
            return redirect('patients:detail', pk=patient.pk)
    else:
        form = PatientForm()
    return render(request, 'patients/form.html', {'form': form, 'title': 'Register New Patient'})

@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    visits = patient.visits.all()
    labs = patient.lab_results.all()
    aes = patient.adverse_events.all()
    audit_logs = AuditLog.objects.filter(module='patients', record_id=pk).select_related('user')
    return render(request, 'patients/detail.html', {
        'patient': patient, 'visits': visits, 'labs': labs,
        'aes': aes, 'audit_logs': audit_logs,
    })

@login_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('edit_reason', '')  # BUG Cat-H: not validated server-side
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            old_data = {f: getattr(patient, f) for f in form.changed_data}
            form.save()
            patient.refresh_from_db()
            new_data = {f: getattr(patient, f) for f in form.changed_data}
            changed = {f: {'old': str(old_data[f]), 'new': str(new_data[f])} for f in form.changed_data}
            log_action(request, 'patients', patient.id, 'UPDATE', changed, reason=reason)
            messages.success(request, 'Patient updated.')
            return redirect('patients:detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/form.html', {'form': form, 'patient': patient, 'title': 'Edit Patient'})

@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('delete_reason', '')
        log_action(request, 'patients', patient.id, 'DELETE', {}, reason=reason)
        patient.delete()
        messages.success(request, 'Patient record deleted.')
        return redirect('reports:listing')
    return render(request, 'patients/confirm_delete.html', {'patient': patient})
