from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from .models import Tasks
from .forms import CreateForm,Registerform,LoginForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.decorators import login_required



def TaskList(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        tasks = Tasks.objects.filter(user=request.user)
    else:
        user_id = None
        tasks = Tasks.objects.filter(is_public=True)  # Filter public tasks for unauthenticated users
    
    context = {
        'user_id': user_id,
        'tasks': tasks,
    }
    
    return render(request, 'pages/task.html', context)


@login_required
def CreateList(request):
    form = CreateForm()
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  
            task.save()
            return redirect('task')  
    return render(request, 'pages/create.html', {'form': form})

@login_required
def deletetask(request, task_id):
    task = get_object_or_404(Tasks, id=task_id)
    task.delete()
    return redirect('task') 

@login_required
def Viewtask(request,view_id):
    view=Tasks.objects.filter(id=view_id).first() 
    context={'views':view}
    return render(request,'pages/view.html',context)
@login_required
def edittask(request, edit_id):
    task = get_object_or_404(Tasks, id=edit_id, user=request.user) 

    if request.method == 'POST':
        form = CreateForm(request.POST, instance=task)  
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Assign the logged-in user to the task
            task.save()
            return redirect('task')  # redirect to task list after saving
    else:
        form = CreateForm(instance=task) 
    
    context = {'form': form}
    return render(request, 'pages/edit.html', context)






def register(request):
    form = Registerform()

    if request.method == 'POST':
        form = Registerform(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(username=name).exists():
                messages.error(request, "Username already taken!")
                return redirect('register')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered!")
                return redirect('register')

            user = User.objects.create_user(username=name, email=email, password=password)
            user.save()
            
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')

        else:
           
            messages.error(request, "Please correct the errors below.")

    return render(request, 'pages/register.html', {'form': form})

def Login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            auth_login(request, user)
            messages.success(request, "Login successful!")
            return redirect('/')
        else:
            messages.error(request, "Invalid email or password")
    
    return render(request, "pages/login.html", {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')


