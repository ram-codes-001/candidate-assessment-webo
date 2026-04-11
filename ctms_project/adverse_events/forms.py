from django import forms
from .models import AdverseEvent
from patients.models import Patient


class AdverseEventForm(forms.ModelForm):
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
    )
    attachment = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        # BUG: No allowed_extensions validation — unsafe upload bug
    )

    class Meta:
        model = AdverseEvent
        exclude = ['created_by', 'created_at', 'updated_at']
        widgets = {
            'event_title': forms.TextInput(attrs={'class': 'form-control'}),
            # BUG Cat-C: TextInput not DateInput for date fields
            'onset_date': forms.TextInput(attrs={
                'class': 'form-control flatpickr-input',
                'placeholder': 'DD/MM/YYYY',
                'autocomplete': 'off',
            }),
            'resolution_date': forms.TextInput(attrs={
                'class': 'form-control flatpickr-input',
                'placeholder': 'DD/MM/YYYY',
                'autocomplete': 'off',
            }),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'causality': forms.Select(attrs={'class': 'form-control'}),
            # BUG Cat-A: event_description blank=True in Meta — not required
            'event_description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 4,
            }),
            'action_taken': forms.Select(attrs={'class': 'form-control'}),
            'outcome': forms.Select(attrs={'class': 'form-control'}),
            'is_sae': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # BUG Cat-A/F: sae_report_number blank=True in Meta — not required even when is_sae=True
            'sae_report_number': forms.TextInput(attrs={'class': 'form-control'}),
            'reported_by': forms.TextInput(attrs={'class': 'form-control'}),
            # BUG Cat-C: TextInput not DateInput
            'report_date': forms.TextInput(attrs={
                'class': 'form-control flatpickr-input',
                'placeholder': 'DD/MM/YYYY',
                'autocomplete': 'off',
            }),
            'regulatory_reported': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    # BUG Cat-F: No clean() to compare resolution_date >= onset_date
    # BUG Cat-A/F: No clean() to require sae_report_number when is_sae=True
