from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from djoser.conf import LazySettings, settings
from djoser.serializers import ActivationSerializer
from rest_framework import permissions, generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.utils import json
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.views import APIView
from djoser import utils
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from .models import *
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import *
from .services import all_objects, set_token_cookie


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
        return Response(ArticleSerializer(article).data)


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
        return Response(CommentSerializer(comment).data)

    def update(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.text = self.request.POST['text']
        comment.save()
        return Response(CommentSerializer(comment).data)


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
        return Response(CommentSerializer(comment).data)


class RelationShipView(viewsets.ModelViewSet):
    queryset = all_objects(Relationship)
    serializer_class = RelationshipSerializer

    def create(self, request):
        me = self.request.user.profile
        other = get_object_or_404(Profile, pk=self.request.POST['profile_id'])
        relationship = Relationship.objects.create()
        if me.status == 'Родитель':
            relationship.requests_to_parents.add(me)
            relationship.requests_to_childrens.add(other)
            relationship.owner.add(me)
            relationship.parent.add(me)
        else:
            relationship.request_to_parents.add(other)
            relationship.request_to_childrens.add(me)
            relationship.list_on_invite.add(me)
            relationship.children.add(me)
        return Response(RelationshipSerializer(relationship).data)

    def update(self, request, pk):
        data = get_object_or_404(Relationship, pk=pk)
        me = self.request.user.profile
        if me.status == 'Родитель':
            data.parent.add(me)
        else:
            data.children.add(me)
        data.list_on_invite.remove(me)
        data.save()
        serializer = self.get_serializer(data, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class RelationShipListoninvite(generics.ListAPIView):
    queryset = all_objects(Relationship)
    serializer_class = RelationshipSerializer

    def list(self, request):
        profile = request.user.profile
        list_name = []
        if profile.status == 'Ребёнок':
            relationships = profile.request_to_relation_childrens.all()
        else:
            relationships = profile.request_to_relation_parents.all()
        for relationship in relationships:
            for profile in relationship.owner.all():
                list_name.append({'owner': profile.user.username,
                                  'name': profile.name,
                                  'id': profile.id})
        print(list_name)
        return Response(list_name)


class RoomView(viewsets.ModelViewSet):
    queryset = all_objects(Room)
    serializer_class = RoomSerializer


def index(request):
    return HttpResponse('<h1>Hello</h1>')


class CustomActivationView(APIView):
    token_generator = default_token_generator

    def get(self, request, *args, **kwargs):
        # Декодирование UID и получение пользователя
        try:
            uid = force_str(urlsafe_base64_decode(kwargs['uid']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Неверный UID'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка токена и активация пользователя
        serializer_context = {
            'request': request,
            'view': self,
        }
        serializer = ActivationSerializer(data={'uid': kwargs['uid'], 'token': kwargs['token']},
                                          context=serializer_context)
        if serializer.is_valid():
            user.is_active = True
            user.save()
            # Логирование и получение токена
            settings = LazySettings()
            token = utils.login_user(self.request, user)
            token_serializer_class = settings.SERIALIZERS.token
            # ДОДЕЛАТЬ redirect to Profile create
            # Установка куков
            set_token_cookie(user=user)
            return Response(
                data=token_serializer_class(token).data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Атоматически добавляет uid и токен (сброс пароля)
class CustomPasswordResetView(PasswordResetView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context.get('user')
        context['uid'] = settings.PASSWORD_RESET_CONFIRM_URL.format(**{
            'uid': user.uid,
            'token': default_token_generator.make_token(user)
        })
        return context


# Атоматически добавляет uid и токен (сборс пароля ссылка )
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uid'] = self.kwargs['uid']
        context['token'] = self.kwargs['token']
        return context



