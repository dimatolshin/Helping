from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from .views import *

router = DefaultRouter()
router.register(r'profiles', views.ProfileViewSet)
router.register(r'users', views.UserViewSet)

app_name = "mysite"

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('api/profiles/list/<int:pk>/', ProfileUpdate.as_view()),
    path('api/profiles/destroy/<int:pk>/', ProfileDestroy.as_view()),
    path('api/users/list/<int:pk>/', UserUpdate.as_view()),
    path('api/users/destroy/<int:pk>/', UserDestroy.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
