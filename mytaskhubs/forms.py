from django import forms
from .models import Task, Entry, Project, Goal  # 🔹 alterado de Meta para Goal

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

class GoalForm(forms.ModelForm):  # 🔹 alterado de MetaForm para GoalForm
    class Meta:
        model = Goal  # 🔹 alterado de Meta para Goal
        fields = ['title', 'description', 'end_date']  # 🔹 end_date substitui duration
        labels = {'title': 'Texto', 'description': 'Descrição', 'end_date': 'Data Limite'}
        widgets = {
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
