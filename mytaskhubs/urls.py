from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks', views.tasks, name='tasks'),
    path('task/<int:task_id>/', views.task, name='task'),
    path('new_task/<int:project_id>/', views.new_task, name='new_task'),
    path('new_task/', views.new_task_no_project, name='new_task_no_project'),
    path('new_entry/<int:task_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    
    path('projects', views.projects, name='projects'),
    path('new_project/', views.new_project, name='new_project'),
    path('project/<int:project_id>/', views.project, name='project'),
    
    # URLs atualizadas para Goal
    path('goals/', views.goals, name='goals'),
    path('goal/<int:goal_id>/', views.goal, name='goal'),
    path('new_goal/', views.new_goal, name='new_goal'),
    path('add_task_to_goal/<int:goal_id>/', views.add_task_to_goal, name='add_task_to_goal'),
    path('goal/concluir/<int:goal_id>/', views.concluir_goal, name='concluir_goal'),
    path('goals/<int:goal_id>/arquivar/', views.arquivar_goal, name='arquivar_goal'),
    path('goals/<int:goal_id>/ativar/', views.ativar_goal, name='ativar_goal'),

    # Concluir/arquivar/ativar projetos e tasks
    path('task/concluir/<int:task_id>/', views.concluir_task, name='concluir_task'),
    path('project/concluir/<int:project_id>/', views.concluir_project, name='concluir_project'),
    path('projects/<int:project_id>/arquivar/', views.arquivar_project, name='arquivar_project'),
    path('tasks/<int:task_id>/arquivar/', views.arquivar_task, name='arquivar_task'),
    path('projects/<int:project_id>/ativar/', views.ativar_project, name='ativar_project'),
    path('tasks/<int:task_id>/ativar/', views.ativar_task, name='ativar_task'),
    path("update_task/<int:task_id>/", views.update_task, name="update_task"),

    # Excluir anotação
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),


    # Filtros e calendário
    path('tasks_concluidas/', views.tasks_concluidas, name='tasks_concluidas'),
    path('tasks_pendentes/', views.tasks_pendentes, name='tasks_pendentes'),
    path('calendario_tasks/', views.calendario_tasks, name='calendario_tasks'),
    path('api/calendario_tasks/', views.calendario_tasks_api, name='calendario_tasks_api'),
]
