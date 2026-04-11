from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LabResult
from .forms import LabForm
from audit.mixins import log_action


@login_required
def lab_list(request):
    labs = LabResult.objects.select_related('patient', 'visit').all()
    return render(request, 'labs/list.html', {'labs': labs})


@login_required
def lab_create(request):
    initial = {}
    patient_pk = request.GET.get('patient')
    if patient_pk:
        initial['patient'] = patient_pk
    if request.method == 'POST':
        form = LabForm(request.POST)
        if form.is_valid():
            lab = form.save(commit=False)
            lab.created_by = request.user
            lab.save()
            log_action(request, 'labs', lab.id, 'CREATE', {})
            messages.success(request, 'Lab result recorded successfully.')
            return redirect('labs:detail', pk=lab.pk)
    else:
        form = LabForm(initial=initial)
    return render(request, 'labs/form.html', {'form': form, 'title': 'Add Lab Result'})


@login_required
def lab_detail(request, pk):
    lab = get_object_or_404(LabResult, pk=pk)
    return render(request, 'labs/detail.html', {'lab': lab})


@login_required
def lab_edit(request, pk):
    lab = get_object_or_404(LabResult, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('edit_reason', '')  # BUG Cat-H: not validated server-side
        form = LabForm(request.POST, instance=lab)
        if form.is_valid():
            old_data = {f: getattr(lab, f) for f in form.changed_data}
            form.save()
            lab.refresh_from_db()
            new_data = {f: getattr(lab, f) for f in form.changed_data}
            changed = {f: {'old': str(old_data[f]), 'new': str(new_data[f])} for f in form.changed_data}
            log_action(request, 'labs', lab.id, 'UPDATE', changed, reason=reason)
            messages.success(request, 'Lab result updated.')
            return redirect('labs:detail', pk=lab.pk)
    else:
        form = LabForm(instance=lab)
    return render(request, 'labs/form.html', {'form': form, 'lab': lab, 'title': 'Edit Lab Result'})


@login_required
def lab_delete(request, pk):
    lab = get_object_or_404(LabResult, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('delete_reason', '')
        log_action(request, 'labs', lab.id, 'DELETE', {}, reason=reason)
        patient_pk = lab.patient_id
        lab.delete()
        messages.success(request, 'Lab result deleted.')
        return redirect('patients:detail', pk=patient_pk)
    return render(request, 'labs/confirm_delete.html', {'lab': lab})
