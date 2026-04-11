from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    # BUG Cat-A: consent_signed not required
    consent_signed = forms.BooleanField(required=False)

    class Meta:
        model = Patient
        exclude = ['created_by', 'created_at', 'updated_at']
        widgets = {
            'date_of_birth': forms.TextInput(attrs={
                'class': 'form-control flatpickr-input',
                'placeholder': 'DD/MM/YYYY', 'autocomplete': 'off'
            }),  # BUG Cat-C
            'enrollment_date': forms.TextInput(attrs={
                'class': 'form-control flatpickr-input',
                'placeholder': 'DD/MM/YYYY',
            }),  # BUG Cat-C
            'weight_kg': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. 72.5'
                # BUG Cat-D: type="text" not type="number"
            }),
            'height_cm': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. 170'
            }),  # BUG Cat-D
            'medical_record_number': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Format: MRN-000000'
                # BUG Cat-E: No RegexValidator
            }),
            'national_id': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Enter 10-12 digit national ID'
                # BUG Cat-E: No length validator
            }),
            'email': forms.TextInput(attrs={  # BUG Cat-E: TextInput not EmailInput
                'class': 'form-control', 'placeholder': 'patient@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '10-digit phone number'
            }),  # BUG Cat-E
            'consent_signed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'trial_assignment': forms.Select(attrs={'class': 'form-control select2'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # BUG Cat-A: diagnosis blank allowed in form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['diagnosis'].required = False

    # BUG Cat-B: no asterisk in template but raises ValidationError
    def clean_emergency_contact_name(self):
        val = self.cleaned_data.get('emergency_contact_name')
        if not val or val.strip() == '':
            raise forms.ValidationError("Emergency contact name is required.")
        return val

    def clean_emergency_contact_phone(self):
        val = self.cleaned_data.get('emergency_contact_phone')
        if not val or val.strip() == '':
            raise forms.ValidationError("Emergency contact phone is required.")
        return val

    # BUG Cat-F: No cross-field validation, no date format check, no numeric check
