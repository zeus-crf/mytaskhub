from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('tasks', views.tasks, name='tasks'),
    path('task/<task_id>/', views.task, name='task'),#Busca a task através do id do bando de dados
    path('new_task/<project_id>/', views.new_task, name='new_task'),
    path('new_task/', views.new_task_no_project, name='new_task_no_project'),
    path('new_entry/<task_id>', views.new_entry, name='new_entry'),
    path('edit_entry/<entry_id>', views.edit_entry, name='edit_entry'),
    path('projects', views.projects, name='projects'),
    path('new_project/', views.new_project, name='new_project'),
    path('project/<project_id>/', views.project, name='project'),
    path('meta/', views.metas, name='metas'),   
    path('meta/<int:meta_id>/', views.meta, name='meta'),
    path('new_meta/', views.new_meta, name = 'new_meta'),
    path('add_task_to_meta/<meta_id>/', views.add_task_to_meta, name='add_task_to_meta'),
    path('task/concluir/<int:task_id>/', views.concluir_task, name='concluir_task'),
    path('project/concluir/<int:project_id>/', views.concluir_project, name='concluir_project'),
    path('projects/<int:project_id>/arquivar/', views.arquivar_project, name='arquivar_project'),
    path('tasks/<int:task_id>/arquivar/', views.arquivar_task, name='arquivar_task'),
    path('projects/<int:project_id>/ativar/', views.ativar_project, name='ativar_project'),
    path('tasks/<int:task_id>/ativar/', views.ativar_task, name='ativar_task'),
    path('tasks_concluidas/', views.tasks_concluidas, name='tasks_concluidas'),
    path('tasks_pendentes/', views.tasks_pendentes, name='tasks_pendentes'),
    path('calendario_tasks/', views.calendario_tasks, name='calendario_tasks'),
    path('api/calendario_tasks/', views.calendario_tasks_api, name='calendario_tasks_api'),
]
