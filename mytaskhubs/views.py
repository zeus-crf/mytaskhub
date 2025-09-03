from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Entry, Project, Meta
from .forms import TaskForm, EntryForm, ProjectForm, MetaForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.db.models import Count

@login_required
def index(request):# A função request é responsável por fazer a requição feita pelo usuário
    """Página Principal do MyTaskHub"""
    tasks = Task.objects.filter(owner=request.user).order_by('-date_added')[:12]
    tasks_concluidas = Task.objects.filter(owner=request.user, completed=True).count()
    tasks_em_andamento = Task.objects.filter(owner=request.user, completed=False).count()
    metas = Meta.objects.filter(owner=request.user).count()
    context = {'tasks': tasks, 'tasks_concluidas': tasks_concluidas, 'tasks_em_andamento':tasks_em_andamento, 'metas':metas } # Pega as últimas 5 tasks
    return render(request, 'mytaskhubs/index.html',context)
    # A função render renderiza o endereço que for desejado / tente criar a página templates dentro do app

@login_required # Para acessar esta página o usuário precisa estar logado
def tasks(request):
    """Mostra todas as tasks"""
    tasks = Task.objects.filter(owner=request.user).order_by('-date_added') # Traz todas as taks que tem como o dono o usuário, e ordena pela data
    projects = Project.objects.order_by('date_added')
    return render(request, 'mytaskhubs/tasks.html', {
        'tasks': tasks,
        'projects': projects,
    })


@login_required
def meta(request, meta_id):
    meta = get_object_or_404(Meta, pk=meta_id)
    if request.method == 'POST':
        for task in meta.tasks.all(): # percorre todas as tasks dessa meta
            task.completed = f'task_{task.id}' in request.POST # Verifique se o checkbox foi marcado 
            task.save() # Salva as alterações no bando de dados
        return redirect('meta', meta_id=meta.id)

    context = {'meta': meta}
    return render(request, 'mytaskhubs/meta.html', context)

@login_required 
def metas(request):
    """Lista todas as metas"""
    metas = Meta.objects.filter(owner= request.user).order_by('date_added')
    context = {'metas': metas}
    return render(request, 'mytaskhubs/metas.html', context)


@login_required 
def projects(request):
    """Mostra todos os projetos do usuário logado"""
    # Pega todos os projetos do usuário, incluindo arquivados
    projects = Project.objects.all()  # ou .filter(user=request.user) se quiser só do usuário logado

    context = {
        'projects': projects,
        'filter_type': 'all',  # padrão
    }
    return render(request, 'mytaskhubs/projects.html', context)

def mais_tasks(request):
    """Filtra pelos projetos com mais tasks"""
    # Pega todos os projetos do usuário, incluindo arquivados
    projects = Project.objects.filter(owner=request.user).annotate(num_tasks=Count('project_tasks')).order_by('-num_tasks')

    context = {
        'projects': projects,
    }
    return render(request, 'mytaskhubs/projects.html', context)

def menos_tasks(request):
    """Filtra pelos projetos com menos tasks"""
    # Pega todos os projetos do usuário, incluindo arquivados
    projects = Project.objects.filter(owner=request.user).annotate(num_tasks=Count('project_tasks')).order_by('num_tasks')

    context = {
        'projects': projects,
    }
    return render(request, 'mytaskhubs/projects.html', context)


def mais_recentes(request):
    """Filtra pelos projetos mais recentes"""
    # Pega todos os projetos do usuário, incluindo arquivados
    projects = Project.objects.filter(owner=request.user).order_by('-date_added')

    context = {
        'projects': projects,
    }
    return render(request, 'mytaskhubs/projects.html', context)

def mais_antigos(request):
    """Filtra pelos projetos mais antigos"""
    # Pega todos os projetos do usuário, incluindo arquivados
    projects = Project.objects.filter(owner=request.user).order_by('date_added')

    context = {
        'projects': projects,
    }
    return render(request, 'mytaskhubs/projects.html', context)



@login_required 
def task (request, task_id):
    """Mostra apenas uma task e todas as suas entradas"""
    task = Task.objects.get(id = task_id)
    # Garante que a task pertence ao usuário atual
    if task.owner == request.user:
        entries = task.entry_set.order_by('-date_added')# Do mais recente para o mais velho (ordem inversa)
        context = {'task': task, 'entries': entries}
        return render(request, 'mytaskhubs/task.html', context)
    else:
        raise Http404

@login_required 
def project(request, project_id):
    """Mostra apenas um projeto e todas as suas tasks"""
    project = Project.objects.get(id=project_id)

    if project.owner == request.user:

        tasks = project.project_tasks.order_by('date_added')  # Acessa as tasks relacionadas ao projeto
        context = {'project': project, 'tasks': tasks}
        return render(request, 'mytaskhubs/project.html', context)
    else: 
        raise Http404

@login_required 
def new_project(request):
    """Para adicionar um novo Projeto"""
    if request.method != 'POST':
        form = ProjectForm()
    else:
        form = ProjectForm(request.POST)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.owner = request.user
            new_project.save()  # Salva no banco com o owner
            return HttpResponseRedirect(reverse('projects'))
    context = {'form': form}
    return render(request, 'mytaskhubs/new_project.html', context)

@login_required
def new_meta(request):
    """Para adicionar uma nova meta"""
    if request.method != 'POST':
        form = MetaForm()
    else:
        form = MetaForm(request.POST)
        if form.is_valid():
            new_meta = form.save(commit=False) # Somente pega as informções do usuário, mas não salva
            new_meta.owner =  request.user
            new_meta.save()
            return HttpResponseRedirect(reverse('metas'))
    context = {'form' : form}
    return render(request, 'mytaskhubs/new_meta.html', context)

@login_required 
def new_task_no_project(request):
    if request.method != 'POST':
        form = TaskForm()
    else:
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user  # ← CORRETO
            new_task.project = None
            new_task.meta = None
            new_task.save()
            return redirect('tasks')
    context = {'form': form}
    return render(request, 'mytaskhubs/new_task.html',context )


@login_required 
def add_task_to_meta(request, meta_id):
    meta = get_object_or_404(Meta, id=meta_id)

    if meta.owner == request.user:

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
    else:
        raise Http404


@login_required
def new_task(request, project_id=None):
    project = None
    if project_id:
        project = get_object_or_404(Project, id=project_id)

        # Se quiser verificar se o projeto pertence ao usuário, faça:
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
             # ajuste conforme seu fluxo
    else:
        form = TaskForm()

    return render(request, 'mytaskhubs/new_task.html', {
        'form': form,
        'project': project
    })


@login_required
def new_entry(request, task_id):
    """Para adicionar novas entradas nas tasks"""
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
            # Mostra os erros no console para debug
            print("Form errors:", form.errors)
    else:
        form = EntryForm()

    context = {
        'task': task,
        'form': form
    }
    return render(request, 'mytaskhubs/new_entry.html', context)

@login_required 
def edit_entry(request, entry_id):
    """Edita um entrada uma entrada já existente"""
    entry = get_object_or_404(Entry, id=entry_id)
    task = entry.task
    if task.owner == request.user:
        if request.method != 'POST':
            # Não é necessário fazer outro formulário porque ele já existe
            form = EntryForm(instance=entry)# O formulário vai aparecer preenchido / usando entry(entry_id)
        else:
            form = EntryForm(instance=entry, data=request.POST) # Preenche o formulário com os dados antidos, mas modifica com os novos do método POST
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('task', args=[task.id]))
        context = {'entry': entry, 'form': form, 'task': task}
        return render(request, 'mytaskhubs/edit_entry.html', context)
    else:
        raise Http404

@login_required 
def arquivar_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    task.deleted = True
    task.save()
    messages.success(request, f"O projeto '{task.title}' foi arquivado com sucesso!")
    
    # Redireciona para o filtro "archived"
    url = reverse('tasks') + '?filter=archived'
    return redirect(url)

@login_required
def ativar_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    task.deleted = False
    task.completed = False
    task.save()
    messages.success(request, f"A task '{task.title}' foi ativada com sucesso!")
    
    # Redireciona para o filtro "archived"
    url = reverse('tasks') + '?filter=archived'
    return redirect(url)


@login_required 
def concluir_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    if not task.completed:
        task.completed = True
        task.save()
        messages.success(request, f"A task '{task.title}' foi concluído com sucesso!")
    else:
        messages.info(request, f"A task '{task.title}' tá estaca concluída.")
    # Redireciona de volta para a página anterior
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



def arquivar_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    project.deleted = True
    project.save()
    messages.success(request, f"O projeto '{project.title}' foi arquivado com sucesso!")
    
    # Redireciona para o filtro "archived"
    url = reverse('projects') + '?filter=archived'
    return redirect(url)



def ativar_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    
    if project.deleted:
        project.deleted = False
        project.completed = False
        project.save()
        messages.success(request, f"O projeto '{project.title}' foi reativado com sucesso!")
    
    # Redireciona para o filtro "active" para mostrar projetos em andamento
    
    return redirect(f"{reverse('projects')}?filter=active")


@login_required
def tasks_concluidas(request):
    tasks = Task.objects.filter(owner=request.user, completed=True).order_by('-date_added')
    context = {'tasks': tasks}
    return render(request, "mytaskhubs/tasks_concluidas.html", context)

@login_required
def tasks_pendentes(request):
    tasks = Task.objects.filter(owner=request.user, completed=False).order_by('-date_added')
    context = {'tasks': tasks}
    return render(request, "mytaskhubs/tasks_pedentes.html", context)

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
        


