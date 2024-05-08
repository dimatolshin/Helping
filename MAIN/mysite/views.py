from rest_framework.views import APIView
from .models import *
from .serializer import *
from rest_framework.response import Response
from django.http import HttpResponse


class ParentView(APIView):
    def get(self, request):
        parents = Parent.objects.all()
        return Response({'posts': ParentSerializer(parents, many=True).data})

    def post(self, request):
        serializer = ParentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


def index(request):
    return HttpResponse('<h1>Hello</h1>')
