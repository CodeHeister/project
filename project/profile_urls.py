from django.urls import path, include

from . import views

urlpatterns = [
    path('qr-code/', views.QrCode.as_view(), name='qr-code'),
    path('<uuid:id>/', views.Profile.as_view(), name='profile-id'),
    path('<str:username>/', views.Profile.as_view(), name='profile-username'),
]
