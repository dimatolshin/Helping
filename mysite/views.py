from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import permissions, generics, status
from rest_framework import renderers
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets
from .models import *
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import *
from rest_framework.decorators import action, api_view
from .services import all_objects


class UserList(generics.ListAPIView):
    queryset = all_objects(User)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


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
    serializer_class = ProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class ProfileDestroy(generics.RetrieveDestroyAPIView):
    queryset = all_objects(Profile)
    serializer_class = ProfileSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ProfileViewSet(generics.ListCreateAPIView):
    queryset = all_objects(Profile)
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class TaskView(viewsets.ModelViewSet):
    queryset = all_objects(Task)
    serializer_class = TaskSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = all_objects(Article)
    serializer_class = ArticleSerializer


class ArticleAddLike(generics.UpdateAPIView):
    queryset = all_objects(Article)
    serializer_class = ArticleAddLikeSerializer

    def update(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        profile = self.request.user.profile
        if profile in article.like_list.all():
            article.like -= 1
            article.like_list.remove(profile)
        else:
            article.like += 1
            article.like_list.add(profile)
        article.save()
        return HttpResponse(article)


class CommentView(viewsets.ModelViewSet):
    queryset = all_objects(Comment)
    serializer_class = CommentSerializer

    def create(self, request):
        text = self.request.POST['text']
        if not text:
            raise Exception('Пустая строка')
        else:
            comment = Comment.objects.create(
                profile=self.request.user.profile,
                article=get_object_or_404(Article, pk=self.request.POST['article_id']),
                text=text)
        comment.save()
        return HttpResponse(comment)

    def update(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.text = self.request.POST['text']
        comment.save()
        return HttpResponse(comment)


class CommentAddLikeView(generics.UpdateAPIView):
    queryset = all_objects(Comment)
    serializer_class = CommentAddLikeSerializer

    def update(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        profile = self.request.user.profile
        if profile in comment.like_list.all():
            comment.like -= 1
            comment.like_list.remove(profile)
        else:
            comment.like += 1
            comment.like_list.add(profile)
        comment.save()
        return HttpResponse(comment)


class RelationShipView(viewsets.ModelViewSet):
    queryset = all_objects(Relationship)
    serializer_class = RelationshipSerializer

    def create(self, request):
        me = self.request.user.profile
        other = get_object_or_404(Profile, pk=self.request.POST['profile_id'])
        if me.status == 'Родитель':
            relationship = Relationship.objects.create()
            relationship.requests_to_parents.add(me)
            relationship.requests_to_childrens.add(other)
            relationship.list_on_invite.add(other)
            relationship.parent.add(me)
        else:
            relationship = Relationship.objects.create()
            relationship.request_to_parents.add(other)
            relationship.request_to_childrens.add(me)
            relationship.list_on_invite.add(other)
        return HttpResponse(relationship)

    def update(self, request, pk):
        data = get_object_or_404(Relationship, pk=pk)
        me = self.request.user.profile
        if me.status == 'Родитель':
            data.parent.add(me)
        else:
            data.children.add(me)
        data.list_on_invite.remove(me)
        data.save()
        return HttpResponse(data)


class RoomView(viewsets.ModelViewSet):
    queryset = all_objects(Room)
    serializer_class = RoomSerializer


def index(request):
    return HttpResponse('<h1>Hello</h1>')
