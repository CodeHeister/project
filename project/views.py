from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .forms import SignupForm, LoginForm, LogoutForm
from .models import User

class Login(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("index")

        if 'login' in request.POST:
            form = LoginForm(request.POST)
            
            if form.is_valid():
                username = request.POST["username"]
                password = request.POST["password"]

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user, backend="project.backends.UserAuthBackend")
                    return redirect("index")
                else:
                    form.add_error('password', 'Incorrect password')

            return self.get(request, login_form=form)

        elif 'signup' in request.POST:
            form = SignupForm(request.POST)
            
            if form.is_valid():
                user = form.save()
                login(request, user, backend="project.backends.UserAuthBackend")
                return redirect("index")

            return self.get(request, signup_form=form)

        elif 'logout' in request.POST:
            form = LogoutForm(request.POST)

            if form.is_valid():
                logout(request)
                return redirect("login")

            return redirect('index')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("index")

        login_form = kwargs['login_form'] if 'login_form' in kwargs else LoginForm()
        signup_form = kwargs['signup_form'] if 'signup_form' in kwargs else SignupForm()
        context = {
                'login_form' : login_form,
                'signup_form' : signup_form
                }

        return Response(context)

@login_required(login_url="login")
def main(request):
    user = request.user
    return HttpResponse(user.id)
