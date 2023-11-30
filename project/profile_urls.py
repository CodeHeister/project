from django.urls import path, include

from . import views

urlpatterns = [
    path('<uuid:id>/', views.Profile.as_view(), name='profile-id'),
    path('<str:username>/', views.Profile.as_view(), name='profile-username'),
]
