from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AdverseEvent
from .forms import AdverseEventForm
from audit.mixins import log_action


@login_required
def ae_list(request):
    events = AdverseEvent.objects.select_related('patient').all()
    return render(request, 'adverse_events/list.html', {'events': events})


@login_required
def ae_create(request):
    initial = {}
    patient_pk = request.GET.get('patient')
    if patient_pk:
        initial['patient'] = patient_pk
    if request.method == 'POST':
        form = AdverseEventForm(request.POST, request.FILES)
        if form.is_valid():
            ae = form.save(commit=False)
            ae.created_by = request.user
            ae.save()
            log_action(request, 'adverse_events', ae.id, 'CREATE', {})
            messages.success(request, 'Adverse event reported successfully.')
            return redirect('adverse_events:detail', pk=ae.pk)
    else:
        form = AdverseEventForm(initial=initial)
    return render(request, 'adverse_events/form.html', {'form': form, 'title': 'Report Adverse Event'})


@login_required
def ae_detail(request, pk):
    ae = get_object_or_404(AdverseEvent, pk=pk)
    return render(request, 'adverse_events/detail.html', {'ae': ae})


@login_required
def ae_edit(request, pk):
    ae = get_object_or_404(AdverseEvent, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('edit_reason', '')  # BUG Cat-H: not validated server-side
        form = AdverseEventForm(request.POST, request.FILES, instance=ae)
        if form.is_valid():
            old_data = {f: getattr(ae, f) for f in form.changed_data}
            form.save()
            ae.refresh_from_db()
            new_data = {f: getattr(ae, f) for f in form.changed_data}
            changed = {f: {'old': str(old_data[f]), 'new': str(new_data[f])} for f in form.changed_data}
            log_action(request, 'adverse_events', ae.id, 'UPDATE', changed, reason=reason)
            messages.success(request, 'Adverse event updated.')
            return redirect('adverse_events:detail', pk=ae.pk)
    else:
        form = AdverseEventForm(instance=ae)
    return render(request, 'adverse_events/form.html', {'form': form, 'ae': ae, 'title': 'Edit Adverse Event'})


@login_required
def ae_delete(request, pk):
    ae = get_object_or_404(AdverseEvent, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('delete_reason', '')
        log_action(request, 'adverse_events', ae.id, 'DELETE', {}, reason=reason)
        patient_pk = ae.patient_id
        ae.delete()
        messages.success(request, 'Adverse event deleted.')
        return redirect('patients:detail', pk=patient_pk)
    return render(request, 'adverse_events/confirm_delete.html', {'ae': ae})
