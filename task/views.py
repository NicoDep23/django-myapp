from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .form import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'home.html', {
        'form': UserCreationForm
    })

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect(tasks)
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Usuer alreay exists'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password do not mach'
        })

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None :
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username o password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')

@login_required
def tasks(request):
    #devuelve todas las tareas no completadas del user a la lista tasks
    tasks = Task.objects.filter(user=request.user, datecompeleted__isnull=True)
    #luego las pasamos al front 
    return render(request, 'tasks.html',{'tasks': tasks})

@login_required
def tasks_completed(request):
    #devuelve todas las tareas  completadas del user a la lista tasks
    tasks = Task.objects.filter(user=request.user, datecompeleted__isnull=False).order_by('-datecompeleted')
    #luego las pasamos al front 
    return render(request, 'tasks.html',{'tasks': tasks})

@login_required
def task_detail(request, task_id):

    if request.method == 'GET':
        #obtiene la tarea con el id de ususario  logueado
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        #le pasamos la tarea al task form para editarla
        form = TaskForm(instance=task)
        #le pasamos la lista de tareas del usuario al html
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
            'task': task,
            'form': form,
            'error':'Error updating task'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method=='POST':
        task.datecompeleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required    
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method=='POST':
        task.delete()
        return redirect('tasks')

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'form': TaskForm,
        })
    else:
        try:
            form = TaskForm(request.POST)
            print(form)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html',{
            'form': TaskForm,
            'error': 'Please provide valida data'
            })

    
