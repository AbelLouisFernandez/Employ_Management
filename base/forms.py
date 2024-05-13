from django.forms import ModelForm 
from .models import Work
from django import forms
from django.utils.timezone import now, timedelta

class workform(ModelForm):
    class Meta:
     model = Work
     fields='name','description','skills_needed','deadline'
     widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date', 'min': (now() + timedelta(days=1)).strftime('%Y-%m-%d')})
        }
     
class PresenceForm(forms.Form):
    is_present = forms.BooleanField(label='I am present', required=False)
    is_absent = forms.BooleanField(label='I am absent', required=False)

