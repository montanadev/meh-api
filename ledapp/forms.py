from django import forms
from .models import LED

class LEDForm(forms.ModelForm):
    class Meta:
        model = LED
        fields = ['red', 'blue', 'green']