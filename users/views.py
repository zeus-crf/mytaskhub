from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def logout_view(request):
    """Faz um logout do usuário"""
    logout(request)
    return  HttpResponseRedirect(reverse('index'))

def register(request):
    """Faz o cadastro de um novo usuário"""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Faz o login do usuário e o redireciona para a página inicial
            authenticated_user = authenticate(username = new_user.username, password = request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('index'))
        

    context = {'form': form}
    return render(request, 'users/register.html', context)


