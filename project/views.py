from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required

from rest_framework import status, exceptions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView, exception_handler
from rest_framework.permissions import IsAuthenticated

from .forms import SignupForm, LoginForm
from .permissions import CustomIsAuthenticated, CustomNotAuthenticated
from .exceptions import NotAuthenticated, Authenticated

User = get_user_model()

def rest_permission_denied_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, Authenticated):
        if getattr(exc, 'redirect_to_index', False):
            return redirect('index')
    elif isinstance(exc, NotAuthenticated):
        if getattr(exc, 'redirect_to_login', False):
            return redirect('login')

    return response

class Login(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [CustomNotAuthenticated]
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
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

class Logout(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [CustomIsAuthenticated]
    template_name = 'logout.html'

    def get(self, request):
        logout(request)
        return redirect("login")

class Index(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [CustomIsAuthenticated]
    template_name = 'index.html'

    def get(self, request):
        context = {
                "users" : User.objects.all()
                }
        return Response(context)

class Profile(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile.html'

    def get(self, request, **kwargs):
        user = None

        if 'id' in kwargs:
            id = kwargs['id']
            user = User.objects.filter(id=id)

        elif 'username' in kwargs:
            username = kwargs['username']
            user = User.objects.filter(username=username)

        context = {}
        if user and user.exists():
            context["profile"] = user.get()
        return Response(context)
