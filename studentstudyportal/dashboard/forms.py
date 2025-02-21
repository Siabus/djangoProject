from  django import forms
from . models import *
from django.contrib.auth.forms import UserCreationForm


class DateInput(forms.DateInput):
    input_type='date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model= Homework
        widgets={'due':DateInput()}
        fields = ['subject','title','description','due','is_finished']


class Dashboardfom(forms.Form):
    text = forms.CharField(max_length=200, label= "Enter your search: ")





class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields= ['username','password1','password2']