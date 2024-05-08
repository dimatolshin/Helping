from django.urls import path

from . import views
from .views import ParentView

app_name = "mysite"

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', ParentView.as_view(), name='api')
]
