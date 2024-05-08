from rest_framework import generics
from rest_framework.views import APIView
from .models import *
from .serializer import *
from rest_framework.response import Response
from django.http import HttpResponse


# class ParentView(generics.ListCreateAPIView):
#     queryset = Parent.objects.all()
#     serializer_class = ParentSerializer
#
#
# class ParentDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Parent.objects.all()
#     serializer_class = ParentSerializer



def index(request):
    return HttpResponse('<h1>Hello</h1>')
