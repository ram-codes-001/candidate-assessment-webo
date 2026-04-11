from django import forms
from .models import VisitLog, VISIT_TYPE_CHOICES
from accounts.models import CTMSUser
from patients.models import Patient


class VisitForm(forms.ModelForm):
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
    )
    coordinator = forms.ModelChoiceField(
        queryset=CTMSUser.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = VisitLog
        exclude = ['created_by', 'created_at', 'updated_at']
        widgets = {
            'visit_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Format: V-001',
                # BUG Cat-E: no RegexValidator
            }),
            'visit_date': forms.TextInput(attrs={
                'class': 'form-control flatpickr-input',
                'placeholder': 'DD/MM/YYYY',
                'autocomplete': 'off',
                # BUG Cat-C: TextInput not DateInput
            }),
            'visit_type': forms.Select(attrs={'class': 'form-control'}),
            'investigator_name': forms.TextInput(attrs={'class': 'form-control'}),
            # Vitals — BUG Cat-D: all TextInput type="text" not type="number"
            'systolic_bp': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. 120',
            }),
            'diastolic_bp': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. 80',
            }),
            'heart_rate': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. 72',
            }),
            'body_temperature': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. 36.6',
            }),
            'oxygen_saturation': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. 98',
            }),
            'visit_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'next_visit_date': forms.TextInput(attrs={
                'class': 'form-control flatpickr-input',
                'placeholder': 'DD/MM/YYYY',
                'autocomplete': 'off',
                # BUG Cat-C/F: TextInput, no date comparison validation
            }),
            'protocol_deviation': forms.RadioSelect(choices=[
                (True, 'Yes'), (False, 'No')
            ]),
            'deviation_notes': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                # BUG Cat-A/F: not required even when protocol_deviation=True
            }),
        }

    # BUG Cat-F: No clean() to compare next_visit_date > visit_date
    # BUG Cat-A/F: No clean() to require deviation_notes when protocol_deviation=True
