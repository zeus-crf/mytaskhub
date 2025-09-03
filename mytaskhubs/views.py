from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Entry, Project, Meta
from .forms import TaskForm, EntryForm, ProjectForm, MetaForm
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.db.models import Count


@login_required
def index(request):
    """Página Principal do MyTaskHub"""
    tasks = Task.objects.filter(owner=request.user).order_by('-date_added')[:12]
    tasks_concluidas = Task.objects.filter(owner=request.user, completed=True).count()
    tasks_em_andamento = Task.objects.filter(owner=request.user, completed=False).count()
    metas = Meta.objects.filter(owner=request.user).count()

    context = {
        'tasks': tasks,
        'tasks_concluidas': tasks_concluidas,
        'tasks_em_andamento': tasks_em_andamento,
        'metas': metas
    }
    return render(request, 'mytaskhubs/index.html', context)


@login_required
def tasks(request):
    """Mostra todas as tasks"""
    tasks = Task.objects.filter(owner=request.user).order_by('-date_added')
    projects = Project.objects.order_by('date_added')
    return render(request, 'mytaskhubs/tasks.html', {
        'tasks': tasks,
        'projects': projects,
    })


@login_required
def meta(request, meta_id):
    meta = get_object_or_404(Meta, pk=meta_id)
    if request.method == 'POST':
        for task in meta.tasks.all():
            task.completed = f'task_{task.id}' in request.POST
            task.save()
        return redirect('meta', meta_id=meta.id)

    return render(request, 'mytaskhubs/meta.html', {'meta': meta})


@login_required
def metas(request):
    """Lista todas as metas"""
    metas = Meta.objects.filter(owner=request.user).order_by('date_added')
    return render(request, 'mytaskhubs/metas.html', {'metas': metas})


@login_required
def projects(request):
    """Mostra todos os projetos do usuário logado"""
    projects = Project.objects.all()
    return render(request, 'mytaskhubs/projects.html', {
        'projects': projects,
        'filter_type': 'all',
    })


def mais_tasks(request):
    projects = Project.objects.filter(owner=request.user).annotate(
        num_tasks=Count('project_tasks')
    ).order_by('-num_tasks')
    return render(request, 'mytaskhubs/projects.html', {'projects': projects})


def menos_tasks(request):
    projects = Project.objects.filter(owner=request.user).annotate(
        num_tasks=Count('project_tasks')
    ).order_by('num_tasks')
    return render(request, 'mytaskhubs/projects.html', {'projects': projects})


def mais_recentes(request):
    projects = Project.objects.filter(owner=request.user).order_by('-date_added')
    return render(request, 'mytaskhubs/projects.html', {'projects': projects})


def mais_antigos(request):
    projects = Project.objects.filter(owner=request.user).order_by('date_added')
    return render(request, 'mytaskhubs/projects.html', {'projects': projects})


@login_required
def task(request, task_id):
    """Mostra apenas uma task e todas as suas entradas"""
    task = get_object_or_404(Task, id=task_id)
    if task.owner != request.user:
        raise Http404
    entries = task.entry_set.order_by('-date_added')
    return render(request, 'mytaskhubs/task.html', {'task': task, 'entries': entries})


@login_required
def project(request, project_id):
    """Mostra apenas um projeto e todas as suas tasks"""
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
            return HttpResponseRedirect(reverse('projects'))
    return render(request, 'mytaskhubs/new_project.html', {'form': form})


@login_required
def new_meta(request):
    if request.method != 'POST':
        form = MetaForm()
    else:
        form = MetaForm(request.POST)
        if form.is_valid():
            new_meta = form.save(commit=False)
            new_meta.owner = request.user
            new_meta.save()
            return HttpResponseRedirect(reverse('metas'))
    return render(request, 'mytaskhubs/new_meta.html', {'form': form})


@login_required
def new_task_no_project(request):
    if request.method != 'POST':
        form = TaskForm()
    else:
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.project = None
            new_task.meta = None
            new_task.save()
            return redirect('tasks')
    return render(request, 'mytaskhubs/new_task.html', {'form': form})


@login_required
def add_task_to_meta(request, meta_id):
    meta = get_object_or_404(Meta, id=meta_id)
    if meta.owner != request.user:
        raise Http404

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.meta = meta
            new_task.save()
            return redirect('meta', meta_id=meta.id)
    else:
        form = TaskForm()

    return render(request, 'mytaskhubs/add_task_to_meta.html', {
        'form': form,
        'meta': meta
    })


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
            new_task.save()
            if project:
                return redirect('project', project_id=project.id)
    else:
        form = TaskForm()

    return render(request, 'mytaskhubs/new_task.html', {'form': form, 'project': project})


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


@login_required
def arquivar_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    task.deleted = True
    task.save()
    messages.success(request, f"A task '{task.title}' foi arquivada com sucesso!")
    return redirect(reverse('tasks') + '?filter=archived')


@login_required
def ativar_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    task.deleted = False
    task.completed = False
    task.save()
    messages.success(request, f"A task '{task.title}' foi ativada com sucesso!")
    return redirect(reverse('tasks') + '?filter=archived')


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
    return redirect(reverse('projects') + '?filter=archived')


@login_required
def arquivar_meta(request, meta_id):
    meta = get_object_or_404(Meta, id=meta_id, owner=request.user)
    meta.deleted = True
    meta.save()
    messages.success(request, f"A meta '{meta.title}' foi arquivada com sucesso!")
    return redirect(reverse('metas') + '?filter=archived')


@login_required
def ativar_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if project.deleted:
        project.deleted = False
        project.completed = False
        project.save()
        messages.success(request, f"O projeto '{project.title}' foi reativado com sucesso!")
    return redirect(f"{reverse('projects')}?filter=active")


@login_required
def ativar_meta(request, meta_id):
    meta = get_object_or_404(Meta, id=meta_id, owner=request.user)
    if meta.deleted:
        meta.deleted = False
        meta.completed = False
        meta.save()
        messages.success(request, f"A meta '{meta.title}' foi reativada com sucesso!")
    return redirect(f"{reverse('metas')}?filter=active")


@login_required
def concluir_meta(request, meta_id):
    meta = get_object_or_404(Meta, id=meta_id, owner=request.user)
    if not meta.completed:
        meta.completed = True
        meta.save()
        messages.success(request, f"A meta '{meta.title}' foi concluída com sucesso!")
    else:
        messages.info(request, f"A meta '{meta.title}' já estava concluída.")
    return redirect('metas')


@login_required
def tasks_concluidas(request):
    tasks = Task.objects.filter(owner=request.user, completed=True).order_by('-date_added')
    return render(request, "mytaskhubs/tasks_concluidas.html", {'tasks': tasks})


@login_required
def tasks_pendentes(request):
    tasks = Task.objects.filter(owner=request.user, completed=False).order_by('-date_added')
    return render(request, "mytaskhubs/tasks_pendentes.html", {'tasks': tasks})


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


@login_required
def calendario_tasks(request):
    return render(request, "mytaskhubs/calendario_tasks.html")
