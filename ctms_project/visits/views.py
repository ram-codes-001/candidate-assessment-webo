from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import VisitLog
from .forms import VisitForm
from audit.mixins import log_action


@login_required
def visit_list(request):
    visits = VisitLog.objects.select_related('patient', 'coordinator').all()
    return render(request, 'visits/list.html', {'visits': visits})


@login_required
def visit_create(request):
    initial = {}
    patient_pk = request.GET.get('patient')
    if patient_pk:
        initial['patient'] = patient_pk
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.created_by = request.user
            visit.save()
            log_action(request, 'visits', visit.id, 'CREATE', {})
            messages.success(request, 'Visit logged successfully.')
            return redirect('visits:detail', pk=visit.pk)
    else:
        form = VisitForm(initial=initial)
    return render(request, 'visits/form.html', {'form': form, 'title': 'Log New Visit'})


@login_required
def visit_detail(request, pk):
    visit = get_object_or_404(VisitLog, pk=pk)
    return render(request, 'visits/detail.html', {'visit': visit})


@login_required
def visit_edit(request, pk):
    visit = get_object_or_404(VisitLog, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('edit_reason', '')  # BUG Cat-H: not validated server-side
        form = VisitForm(request.POST, instance=visit)
        if form.is_valid():
            old_data = {f: getattr(visit, f) for f in form.changed_data}
            form.save()
            visit.refresh_from_db()
            new_data = {f: getattr(visit, f) for f in form.changed_data}
            changed = {f: {'old': str(old_data[f]), 'new': str(new_data[f])} for f in form.changed_data}
            log_action(request, 'visits', visit.id, 'UPDATE', changed, reason=reason)
            messages.success(request, 'Visit updated.')
            return redirect('visits:detail', pk=visit.pk)
    else:
        form = VisitForm(instance=visit)
    return render(request, 'visits/form.html', {'form': form, 'visit': visit, 'title': 'Edit Visit'})


@login_required
def visit_delete(request, pk):
    visit = get_object_or_404(VisitLog, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('delete_reason', '')
        log_action(request, 'visits', visit.id, 'DELETE', {}, reason=reason)
        patient_pk = visit.patient_id
        visit.delete()
        messages.success(request, 'Visit record deleted.')
        return redirect('patients:detail', pk=patient_pk)
    return render(request, 'visits/confirm_delete.html', {'visit': visit})
