from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Project(models.Model):
    """Um Projeto que pode conter várias tarefas"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Meta(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)  # corrigido: CharField precisa de max_length
    description = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    duration = models.DateTimeField()  # Duração da meta 
    completed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    @property
    def progress(self):
        total = self.tasks.count()
        concluidas = self.tasks.filter(completed=True).count()
        return int((concluidas / total) * 100) if total > 0 else 0


class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    meta = models.ForeignKey(Meta, related_name='tasks', on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE, related_name='project_tasks')

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="Sem descrição")

    completed = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    PRIORIDADE_CHOICES = [
        ('B', 'Baixa'),
        ('M', 'Média'),
        ('A', 'Alta'),
    ]
    prioridade = models.CharField(max_length=1, choices=PRIORIDADE_CHOICES, default='M')

    def __str__(self):
        # Retorna os primeiros 10 caracteres do texto da task
        return self.title[:10] + ('...' if len(self.title) > 10 else '')


class Entry(models.Model):
    """Algo específico sobre cada Task"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.TextField()  # mantido TextField conforme original
    date_added = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.title[:50] + '...'
