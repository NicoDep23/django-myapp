from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','importat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','placeholder':'Write a title'}),
            'description': forms.Textarea(attrs={'class': 'form-control','placeholder':'Write a dresciption'}),
            'importat': forms.CheckboxInput (attrs={'class': 'form-check-imput-md-auto'})
        }