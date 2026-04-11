from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CTMSAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label='Remember Me')
