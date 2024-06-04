from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from .views import *
from django.urls import re_path
from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

app_name = "mysite"

router = routers.SimpleRouter()
router.register(r'article', ArticleViewSet)
router.register(r'comment', CommentView)
router.register(r'task', TaskView)
router.register(r'relationship', RelationShipView)
router.register(r'room', RoomView)

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    # _____________________________________________________________________________________________________________________
    #  Profile
    path('api/profiles/', ProfileViewSet.as_view()),
    path('api/profiles/list/<int:pk>/', ProfileUpdate.as_view()),
    path('api/profiles/destroy/<int:pk>/', ProfileDestroy.as_view()),
    # _____________________________________________________________________________________________________________________
    #   Users
    path('api/users/list/<int:pk>/', UserUpdate.as_view()),
    path('api/users/destroy/<int:pk>/', UserDestroy.as_view()),
    path('api/users/', UserList.as_view()),
    # path('api/users/create/', UserCreate.as_view()),
    # _____________________________________________________________________________________________________________________
    #   Article
    path('api/article/add_like/<int:pk>/', ArticleAddLike.as_view()),
    # _____________________________________________________________________________________________________________________
    #   Comment
    path('api/comment/add_like/<int:pk>/', ArticleAddLike.as_view()),
    # _____________________________________________________________________________________________________________________
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

#
