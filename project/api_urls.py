from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'friend', views.Friend, basename='friend')

urlpatterns = [
]

urlpatterns += router.urls
