from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Entry, Project, Goal
from .forms import TaskForm, EntryForm, ProjectForm, GoalForm
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.db.models import Count

# ----------------------------
# PÁGINA INICIAL / DASHBOARD
# ----------------------------
@login_required
def index(request):
    """Página Principal do MyTaskHub"""
    tasks = Task.objects.filter(owner=request.user).order_by('-date_added')[:12]
    tasks_concluidas = Task.objects.filter(owner=request.user, completed=True).count()
    tasks_em_andamento = Task.objects.filter(owner=request.user, completed=False).count()
    goals = Goal.objects.filter(owner=request.user).count()

    context = {
        'tasks': tasks,
        'tasks_concluidas': tasks_concluidas,
        'tasks_em_andamento': tasks_em_andamento,
        'goals': goals
    }
    return render(request, 'mytaskhubs/index.html', context)

# ----------------------------
# TASKS
# ----------------------------
@login_required
def tasks(request):
    tasks = Task.objects.filter(owner=request.user).order_by('-date_added')
    projects = Project.objects.order_by('date_added')
    return render(request, 'mytaskhubs/tasks.html', {'tasks': tasks, 'projects': projects})

@login_required
def task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.owner != request.user:
        raise Http404
    entries = task.entry_set.order_by('-date_added')
    return render(request, 'mytaskhubs/task.html', {'task': task, 'entries': entries})

@login_required
def new_task(request, project_id=None):
    project = None
    if project_id:
        project = get_object_or_404(Project, id=project_id)
        if project.owner != request.user:
            raise Http404

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.project = project
            new_task.goal = None
            new_task.save()
            if project:
                return redirect('project', project_id=project.id)
            return redirect('tasks')
    else:
        form = TaskForm()

    return render(request, 'mytaskhubs/new_task.html', {'form': form, 'project': project})

@login_required
def new_task_no_project(request):
    return new_task(request)

@login_required
def concluir_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    if not task.completed:
        task.completed = True
        task.save()
        messages.success(request, f"A task '{task.title}' foi concluída com sucesso!")
    else:
        messages.info(request, f"A task '{task.title}' já estava concluída.")
    return redirect('tasks')

@login_required
def arquivar_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    task.deleted = True
    task.save()
    messages.success(request, f"A task '{task.title}' foi arquivada com sucesso!")
    return redirect('tasks')

@login_required
def ativar_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    if task.deleted:
        task.deleted = False
        task.completed = False
        task.save()
        messages.success(request, f"A task '{task.title}' foi reativada com sucesso!")
    return redirect('tasks')

# ----------------------------
# ENTRIES
# ----------------------------
@login_required
def new_entry(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.owner != request.user:
        raise Http404

    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.task = task
            new_entry.save()
            return HttpResponseRedirect(reverse('task', args=[task_id]))
    else:
        form = EntryForm()

    return render(request, 'mytaskhubs/new_entry.html', {'task': task, 'form': form})

@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    task = entry.task
    if task.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('task', args=[task.id]))

    return render(request, 'mytaskhubs/edit_entry.html', {'entry': entry, 'form': form, 'task': task})

# ----------------------------
# PROJECTS
# ----------------------------
@login_required
def projects(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'mytaskhubs/projects.html', {'projects': projects})

@login_required
def project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.owner != request.user:
        raise Http404
    tasks = project.project_tasks.order_by('date_added')
    return render(request, 'mytaskhubs/project.html', {'project': project, 'tasks': tasks})

@login_required
def new_project(request):
    if request.method != 'POST':
        form = ProjectForm()
    else:
        form = ProjectForm(request.POST)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.owner = request.user
            new_project.save()
            return redirect('projects')
    return render(request, 'mytaskhubs/new_project.html', {'form': form})

@login_required
def concluir_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if not project.completed:
        project.completed = True
        project.save()
        messages.success(request, f"O projeto '{project.title}' foi concluído com sucesso!")
    else:
        messages.info(request, f"O projeto '{project.title}' já estava concluído.")
    return redirect('projects')

@login_required
def arquivar_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    project.deleted = True
    project.save()
    messages.success(request, f"O projeto '{project.title}' foi arquivado com sucesso!")
    return redirect('projects')

@login_required
def ativar_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if project.deleted:
        project.deleted = False
        project.completed = False
        project.save()
        messages.success(request, f"O projeto '{project.title}' foi reativado com sucesso!")
    return redirect('projects')

# ----------------------------
# GOALS / METAS
# ----------------------------
@login_required
def goals(request):
    goals = Goal.objects.filter(owner=request.user).order_by('date_added')
    return render(request, 'mytaskhubs/goals.html', {'goals': goals})

@login_required
def goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    if goal.owner != request.user:
        raise Http404
    if request.method == 'POST':
        for task in goal.tasks.all():
            task.completed = f'task_{task.id}' in request.POST
            task.save()
        return redirect('goal', goal_id=goal.id)
    return render(request, 'mytaskhubs/goal.html', {'goal': goal})

@login_required
def new_goal(request):
    if request.method != 'POST':
        form = GoalForm()
    else:
        form = GoalForm(request.POST)
        if form.is_valid():
            new_goal = form.save(commit=False)
            new_goal.owner = request.user
            new_goal.save()
            return redirect('goals')
    return render(request, 'mytaskhubs/new_goal.html', {'form': form})

@login_required
def add_task_to_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    if goal.owner != request.user:
        raise Http404

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.goal = goal
            new_task.save()
            return redirect('goal', goal_id=goal.id)
    else:
        form = TaskForm()

    return render(request, 'mytaskhubs/add_task_to_goal.html', {'form': form, 'goal': goal})

@login_required
def concluir_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, owner=request.user)
    if not goal.completed:
        goal.completed = True
        goal.save()
        messages.success(request, f"A meta '{goal.title}' foi concluída com sucesso!")
    else:
        messages.info(request, f"A meta '{goal.title}' já estava concluída.")
    return redirect('goals')

@login_required
def arquivar_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, owner=request.user)
    goal.deleted = True
    goal.save()
    messages.success(request, f"A meta '{goal.title}' foi arquivada com sucesso!")
    return redirect('goals')

@login_required
def ativar_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, owner=request.user)
    if goal.deleted:
        goal.deleted = False
        goal.completed = False
        goal.save()
        messages.success(request, f"A meta '{goal.title}' foi reativada com sucesso!")
    return redirect('goals')

# ----------------------------
# FILTROS / CALENDÁRIO
# ----------------------------
@login_required
def tasks_concluidas(request):
    tasks = Task.objects.filter(owner=request.user, completed=True).order_by('-date_added')
    return render(request, "mytaskhubs/tasks_concluidas.html", {'tasks': tasks})

@login_required
def tasks_pendentes(request):
    tasks = Task.objects.filter(owner=request.user, completed=False).order_by('-date_added')
    return render(request, "mytaskhubs/tasks_pendentes.html", {'tasks': tasks})

@login_required
def calendario_tasks(request):
    return render(request, "mytaskhubs/calendario_tasks.html")

@login_required
def calendario_tasks_api(request):
    tasks = Task.objects.filter(owner=request.user)
    events = []
    for task in tasks:
        events.append({
            "id": task.id,
            "title": task.title,
            "start": task.date_added.strftime("%Y-%m-%d"),
            "color": "#4CAF50" if task.completed else "#FF9800",
            'url': reverse('task', args=[task.id]),
        })
    return JsonResponse(events, safe=False)
