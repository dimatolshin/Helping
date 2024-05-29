from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import permissions, generics, status
from rest_framework import renderers
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets
from .models import *
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import ProfileSearializer, UserSerializer
from rest_framework.decorators import action, api_view

from .services import all_objects


class UserList(generics.ListAPIView):
    queryset = all_objects(User)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


# class UserCreate(generics.CreateAPIView):
#     queryset = all_objects(User)
#     serializer_class = RegisterSerializer


class UserUpdate(generics.RetrieveUpdateAPIView):
    queryset = all_objects(User)
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrReadOnly,)


class UserDestroy(generics.RetrieveDestroyAPIView):
    queryset = all_objects(User)
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ProfileUpdate(generics.RetrieveUpdateAPIView):
    queryset = all_objects(Profile)
    serializer_class = ProfileSearializer
    permission_classes = (IsOwnerOrReadOnly,)


class ProfileDestroy(generics.RetrieveDestroyAPIView):
    queryset = all_objects(Profile)
    serializer_class = ProfileSearializer
    permission_classes = (IsAdminOrReadOnly,)


class ProfileViewSet(generics.ListCreateAPIView):
    queryset = all_objects(Profile)
    serializer_class = ProfileSearializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    # @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


def index(request):
    return HttpResponse('<h1>Hello</h1>')
