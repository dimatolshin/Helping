from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import permissions, generics
from rest_framework import renderers
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets
from .models import *
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import ProfileSearializer, UserSerializer
from rest_framework.decorators import action


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class ProfileUpdate(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSearializer
    permission_classes = (IsOwnerOrReadOnly,IsAdminUser)


class ProfileDestroy(generics.RetrieveDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSearializer
    permission_classes = (IsAdminOrReadOnly,)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSearializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


def index(request):
    return HttpResponse('<h1>Hello</h1>')
