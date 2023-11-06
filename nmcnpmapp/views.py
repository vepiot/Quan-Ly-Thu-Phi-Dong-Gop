from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import FamilyMember
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import Group
from .models import CustomUser


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_approved:
                login(request, user)
                return redirect('homepage') 
            else:
                return render(request, 'myapp/wait.html')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required
def homepage(request):
    user = request.user
    user_groups = user.groups.all()
    group_name = user_groups[0].name if user_groups else None

    context = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'group_name': group_name,
    }

    return render(request, 'myapp/homepage.html', context)


def about(request):
    return render(request, 'myapp/about.html')

def contact(request):
    return render(request, 'myapp/contact.html')
    
@login_required
def service(request):
    return render(request, 'myapp/service.html')

@login_required
def wait(request):
    form = CustomAuthenticationForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        if user.is_approved:
            login(request, user)
            return redirect('homepage')
        else:
            return render(request, 'myapp/hompage.html')
    else:
        return redirect('homepage') 


def service_view(request):
    users_donggop = CustomUser.objects.filter(donggop__gt=0)
    return render(request, 'service.html', {'users_donggop': users_donggop})