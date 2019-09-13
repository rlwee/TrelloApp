from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import UserCreationForm,SignUpForm
from django.contrib import messages


# Create your views here.


class SignUp(TemplateView):

    template_name = 'accounts/signup.html'

    def get(self,request, **kwargs):
        form = SignUpForm()
        return render(request, self.template_name, {'form':form})

    def post(self,request, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username = username, password = raw_password)
            # login(request, user)
            return redirect('login')
        return render(request,self.template_name,{'form':form})


class LogIn(TemplateView):

    template_name = 'accounts/login.html'

    def get(self,request,**kwargs):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form':form})

    def post(self,request,**kwargs):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                messages.info(request, f"you are logged in as{username}")
                return redirect('dashboard')
            else:
                messages.error(request, f"Invalid username or password")
        return render(request, self.template_name, {'form':form})

class LogOut(TemplateView):

    template_name = 'accounts.login.html'

    def get(self,request,**kwargs):
        logout(request)
        messages.info(request,"Logged out")
        return redirect('login')
