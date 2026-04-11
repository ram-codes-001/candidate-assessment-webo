from django import forms
from .models import LabResult
from patients.models import Patient
from visits.models import VisitLog


class LabForm(forms.ModelForm):
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
    )
    visit = forms.ModelChoiceField(
        queryset=VisitLog.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = LabResult
        exclude = ['created_by', 'created_at', 'updated_at']
        widgets = {
            'sample_collection_date': forms.TextInput(attrs={
                'class': 'form-control flatpickr-input',
                'placeholder': 'DD/MM/YYYY',
                'autocomplete': 'off',
                # BUG Cat-C: TextInput not DateInput
            }),
            'sample_type': forms.Select(attrs={'class': 'form-control'}),
            'test_name': forms.TextInput(attrs={'class': 'form-control'}),
            # BUG Cat-D: result_value, reference_range_low, reference_range_high as TextInput type="text"
            'result_value': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
            }),
            # BUG Cat-D: unit as free TextInput, no dropdown
            'unit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. mg/dL',
            }),
            'reference_range_low': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
            }),
            'reference_range_high': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
            }),
            'abnormal_flag': forms.Select(attrs={'class': 'form-control'}),
            'lab_technician': forms.TextInput(attrs={'class': 'form-control'}),
            'lab_name': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                # BUG Cat-F: not required even when abnormal_flag='critical'
            }),
        }

    # BUG Cat-F: No clean() to require remarks when abnormal_flag == 'critical'
