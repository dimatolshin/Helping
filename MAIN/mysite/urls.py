from django.urls import path

from . import views
# from .views import ParentView, ParentDetail

app_name = "mysite"

urlpatterns = [
    path('', views.index, name='index'),
    # path('api_parent/', ParentView.as_view(), name='api_parent'),
    # path('api_parent/<int:pk>', ParentDetail.as_view(), name='api_parent_detail'),
]
