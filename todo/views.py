from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def home(request):
   return render(request,'todo/home.html',{})
   

@login_required
def loginuser(request):
   if request.method == 'GET':
      return render(request,'todo/loginuser.html',{
         'form':AuthenticationForm(),
      })
   else:
      user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
      if user is None:
         return render(request,'todo/loginuser.html',{
         'form':AuthenticationForm(),
         'error':'username and password did not match',
      })
      else:
         login(request,user)
         return redirect('todo:currenttodos')

def signupuser(request):
   if request.method == 'GET':
      return render(request,'todo/signupuser.html',{
         'form':UserCreationForm(),
      })
   else:
      if request.POST['password1'] == request.POST['password2']:
         try:
            user  = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
            user.save()
            login(request,user)
            return redirect('todo:currenttodos')
         except IntegrityError:
            return render(request,'todo/signupuser.html',{
         'form':UserCreationForm(),
         'error':'that username has been taken',
      })

      else:
         return render(request,'todo/signupuser.html',{
         'form':UserCreationForm(),
         'error':'password did not match',
      })

@login_required     
def logoutuser(request):
   if request.method == 'POST':
      logout(request)
      return redirect('todo:home')


@login_required
def createtodo(request):
   if request.method == 'GET':
      return render(request,'todo/createtodo.html',{
         'form':TodoForm(),
      })

   else:
      try:
         form = TodoForm(request.POST)
         newtodo = form.save(commit=False)
         newtodo.user = request.user
         newtodo.save()
         return redirect('todo:home')
      except ValueError:
         return render(request,'todo/createtodo.html',{
         'form':TodoForm(),
         'error':'bad data based in',
      })

@login_required
def currenttodos(request):
   todos = Todo.objects.filter(user=request.user,datecompleted__isnull=True)
   return render(request,'todo/currenttodos.html',{
      'todos':todos,
   })

@login_required
def viewtodo(request,id):
   todo = get_object_or_404(Todo,id=id,user=request.user)
   if request.method == 'GET':
      form = TodoForm(instance=todo)
      return render(request,'todo/viewtodo.html',{
         'todo':todo,
         'form':form,
      })
   else:
      try:
         form = TodoForm(request.POST,instance=todo)
         form.save()
         return redirect('todo:home')
      except ValueError:
         return render(request,'todo/viewtodo.html',{
         'todo':todo,
         'form':form,
         'error':'bad info',
      })

@login_required
def completetodo(request):
   todo = get_object_or_404(Todo,id=id,user=request.user)
   if request.method == 'POST':
      todo.datecompleted = timezone.now()
      todo.save()
      return redirect('todo:currenttodos')

@login_required
def deletetodo(request,id):
   todo = get_object_or_404(Todo,id=id,user=request.user)
   if request.method == 'POST':
      todo.datecompleted = timezone.now()
      todo.delete()
      return redirect('todo:currenttodos')

@login_required
def completedtodos(request):
   todos = Todo.objects.filter(user=request.user,datecompleted__isnull=False).order_by('-datecompleted')
   return render(request,'todo/completedtodos.html',{
      'todos':todos,
   })