from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model

from rest_framework import status, exceptions, viewsets
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView, exception_handler
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .forms import SignupForm, LoginForm, SearchForm
from .permissions import CustomIsAuthenticated, CustomIsNotAuthenticated
from .exceptions import IsNotAuthenticated, IsAuthenticated
from .exceptions import PermissionDenied as CustomPermissionDenied
from .serializers import UserSerializer, FriendSerializer

from .extra.algorithms import *
from .qr_code import QrCodeFactory

import uuid

User = get_user_model()

def rest_permission_denied_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, IsAuthenticated):
        if getattr(exc, 'redirect_to_index', False):
            return redirect('index')
    elif isinstance(exc, IsNotAuthenticated):
        if getattr(exc, 'redirect_to_login', False):
            return redirect('login')

    return response

class Login(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [CustomIsNotAuthenticated]
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
        login_form = kwargs['login_form'] if 'login_form' in kwargs else LoginForm()
        signup_form = kwargs['signup_form'] if 'signup_form' in kwargs else SignupForm()
        context = {
                'login_form' : login_form,
                'signup_form' : signup_form
                }

        return Response(context)

class Logout(APIView):
    permission_classes = [CustomIsAuthenticated]

    def get(self, request):
        logout(request)
        return redirect("login")

class Index(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [CustomIsAuthenticated]
    template_name = 'index.html'

    def post(self, request, **kwargs):
        form = SearchForm(request.POST)
        context = {
                "search_form" : form,
                "users" : []
                }

        if form.is_valid():
            username = request.POST["username"]
            users = User.objects.all()
            users = quicksort_users(users)
            first_index = binary_search_first(users, username)
            last_index = binary_search_last(users, username)
            context["users"] = users[first_index:last_index+1]

        return Response(context)

    def get(self, request):
        context = {
                "search_form" : SearchForm(),
                "users" : User.objects.all()
                }
        return Response(context)

class Profile(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile.html'

    def get(self, request, id=None, username=None):
        user = None
        search_form = SearchForm()

        if id:
            user = User.objects.filter(id=id)
        elif username:
            user = User.objects.filter(username=username)

        context = {
                'search_form' : search_form
                }
        if user and user.exists():
            context["profile"] = user.get()
            context["intersection"] = []
            intersection = find_intersection(request.user.id, user.get().id, 3)
            for id in intersection["targets"]:
                user = User.objects.filter(id=id)
                if user and user.exists():
                    context["intersection"].append(user.get())
                    print(context["intersection"])

        return Response(context)

class Friend(viewsets.ViewSet):
    permission_classes = [CustomIsAuthenticated]
    serializer_class = FriendSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=['post'])
    def view(self, request):
        user = request.user

        serializer = FriendSerializer(data=request.data)
        if serializer.is_valid():
            friend_data = serializer.validated_data
            friend = User.objects.filter(id=friend_data.get("id"))

            if friend.exists():
                friend = friend.get()
                friend_data = UserSerializer(friend).data

                return Response(UserSerializer(friend).data)

            return Response(UserSerializer(user).data)
        else:
            return Response(serializer.errors, status=400)


    @action(detail=False, methods=['post'])
    def add(self, request):
        user = request.user
        serializer = FriendSerializer(data=request.data)

        if serializer.is_valid():
            friend_data = serializer.validated_data
            friend = User.objects.filter(id=friend_data.get("id"))

            if friend.exists():
                friend = friend.get()
                friend_id = str(friend.id)
                user_id = str(user.id)

                if friend_id not in user.friends and friend.id != user.id:
                    try:
                        user.friends.append(friend_id)
                        friend.friends.append(user_id)
                    except Exception as e:
                        print(e)
                    finally:
                        user.save()
                        friend.save()
                        return Response(FriendSerializer(friend).data)

                return Response({})
        else:
            return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'])
    def remove(self, request):
        user = request.user
        serializer = FriendSerializer(data=request.data)

        if serializer.is_valid():
            friend_data = serializer.validated_data
            friend = User.objects.filter(id=friend_data.get("id"))

            if friend.exists():
                friend = friend.get()
                friend_id = str(friend.id)
                user_id = str(user.id)

                if friend_id in user.friends and friend.id != user.id:
                    try:
                        user.friends.remove(friend_id)
                        friend.friends.remove(user_id)
                    except Exception as e:
                        print(e)
                    finally:
                        user.save()
                        friend.save()
                        return Response(FriendSerializer(friend).data)

                return Response({})
        else:
            return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'])
    def intersection(self, request):
        user = request.user
        serializer = FriendSerializer(data=request.data)

        if serializer.is_valid():
            friend_data = serializer.validated_data
            friend = User.objects.filter(id=friend_data.get("id"))

            if friend.exists():
                friend = friend.get()
                friend_id = str(friend.id)

                return Response(find_intersection(user.id, friend.id, 3))
        else:
            return Response(serializer.errors, status=400)

class QrCode(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [CustomIsAuthenticated]
    template_name = 'qr-code.html'

    def get(self, request):
        img = QrCodeFactory(str(request.user.id))
        context = {
                "type" : "svg",
                "img" : img.svg(),
                "img_data_uri" : img.png(text="{0}: {1}".format("Name", request.user.name))
                }

        return Response(context)
