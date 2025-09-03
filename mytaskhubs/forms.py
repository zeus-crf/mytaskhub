from django import forms
from .models import Task, Entry, Project, Meta

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']
        labels = {'title': 'Nome da Task', 'description': 'Descrição'}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title']
        labels = {'title': ''}
        widgets = {'title': forms.Textarea(attrs={'cols':80})}

class MetaForm(forms.ModelForm):
    class Meta:
        model = Meta
        fields = ['title', 'description', 'duration'] 
        labels = {'title': 'Texto', 'description': 'Descrição', 'duration': 'Duração'}
        widgets = {
            'duration': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
