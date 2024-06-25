from asyncio import mixins
from datetime import date,datetime
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.conf import LazySettings, settings
from djoser.serializers import ActivationSerializer
from rest_framework import permissions, generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.views import APIView
from djoser import utils
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import *
from .services import all_objects
from .models import *


class UserList(generics.ListAPIView):
    queryset = all_objects(User)
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)


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

    def create(self, request):
        other = Profile.objects.get(id=self.request.POST['profile_id'])
        room = Room.objects.filter(me=self.request.user.profile, other=other)
        if room:
            return Response(RoomSerializer(room).data)

        room = Room.objects.filter(other=self.request.user.profile, me=other)
        if room:
            return Response(RoomSerializer(room).data)

        else:
            room = Room.objects.create(me=self.request.user.profile, other=other)

            return Response(RoomSerializer(room).data)

    def list(self, request):

        me_room = Room.objects.filter(me=self.request.user.profile)

        other_room = Room.objects.filter(other=self.request.user.profile)

        data = []

        for room in me_room:
            last_message = Message.objects.get(room=room).last()  # ili [-1]

            data.append({'id': room.id, 'name_room': room.other.user.username, 'photo_room': room.other.photo,
                         'last_message': last_message.text})

        for room in other_room:
            last_message = Message.objects.get(room=room).last()  # ili [-1]
            data.append({'id': room.id, 'name_room': room.me.user.username, 'photo_room': room.me.photo,
                         'last_message': last_message.text})

        return Response(data)


class MessageView(viewsets.ModelViewSet):
    queryset = all_objects(Message)
    serializer_class = MessageSerializer


class CustomMessageList(generics.ListAPIView):
    queryset = all_objects(Message)
    serializer_class = MessageSerializer

    def list(self, request):
        room = Room.objects.get(id=self.request.POST['room_id'])
        all_message = Message.objects.all(room=room)
        return Response(MessageSerializer(all_message).data)


class CalendarView(viewsets.ModelViewSet):
    queryset = all_objects(Calendar)
    serializer_class = CalendarSerializer


class CategoryView(viewsets.ModelViewSet):
    queryset = all_objects(Category)
    serializer_class = CategorySerializer


class PodCategoryView(viewsets.ModelViewSet):
    queryset = all_objects(PodCategory)
    serializer_class = PodCategorySerializer


class PictureView(viewsets.ModelViewSet):
    queryset = all_objects(Picture)
    serializer_class = PictureSerializer


class TaskView(viewsets.ModelViewSet):
    queryset = all_objects(Task)
    serializer_class = TaskSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        if self.request.user.profile.status != 'Родитель':
            return Response({'Ошибка': 'У вас нет доступа к данному контенту'})
        serializer = TaskSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


    def list(self, request, *args, **kwargs):
        if self.request.user.profile.status != 'Родитель':
            return Response({'Ошибка': 'У вас нет доступа к данному контенту'})

        data = Task.objects.filter(calendar__parent=self.request.user.profile).select_related('calendar', 'children',
                                                                                              'picture')
        return Response(TaskSerializer(data, many=True).data)


    @transaction.atomic
    def delete(self, request, pk, *args, **kwargs):
        if self.request.user.profile.status != 'Родитель':
            return Response({'Ошибка': 'Только "Родитель" может удалять задания'})

        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return Response({'Уведомление': 'Задание успешно удалено'})


# import datetime
class TasksForChildrenView(mixins.RetrieveModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        children = self.request.user.profile
        if children.status == 'Ребенок':
            today = date.today()
            new_form_data = today.strftime("%Y-%m-%d")
            data = Task.objects.filter(children=children, calendar__date=new_form_data)
            if not data:
                return Response({'Error': 'У вас нет заданий'})
            serializer = TaskSerializer(data, many=True)
            return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        task = get_object_or_404(Task, pk=pk)
        children = self.request.user.profile
        today_date = date.today()
        new_form_data = today_date.strftime("%Y-%m-%d")
        new_form_time = datetime.now().strftime("%H:%M:%S")
        if children.status == 'Ребенок' and task.children == children and task.calendar.date == new_form_data:
            if task.start_time and new_form_time < task.start_time.strftime("%H:%M:%S"):
                return Response({'Error': f'Ещё слишком рано, вы сможете начать в {task.start_time}'})
            else:
                serializer = TaskSerializer(task)
                return Response(serializer.data)


class CompleteTask(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = all_objects(Task)
    serializer_class = TaskSerializer

    def get(self, request, pk):
        task = get_object_or_404(Task,pk=pk)
        time = datetime.now()
        new_form_time = time.strftime("%H:%M:%S")
        if task.finish_time < new_form_time:
            task.status = InfoStatus.COMPLETED
            task.save()
        else:
            task.status = InfoStatus.WrongTime

        return Response(TaskSerializer(task).data)


class OrderView(viewsets.ModelViewSet):
    queryset = all_objects(Order)
    serializer_class = OrderSerializer

class OrderForParent(mixins.RetrieveModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # Конкретный приём
    def get(self, request, pk):
        if self.request.user.profile.status == 'Родитель':
            data = Order.objects.get(parent=self.request.user.profile,pk=pk)
            if not data.exists():
                return Response({'Error': 'Запись не найдена'})
            serializer = OrderSerializer(data)
            return Response(serializer.data)


    # Все его приемы
    def list(self, request):
        if self.request.user.profile.status == 'Родитель':
            data = Order.objects.filter(parent=self.request.user.profile, status=StatusOrder.Busy)
            if not data.exists():
                return Response({'Error': 'Записи не найдены'})
            serializer = OrderSerializer(data, many=True)
            return Response(serializer.data)


class SubscribeOrder(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = all_objects(Order)
    serializer_class = OrderSerializer

# Записаться на приём
    def get(self, request, pk):
        data = get_object_or_404(Order,pk=pk)
        if self.request.user.profile.status == 'Родитель' and data.parent == None:
            data.parent = self.request.user.profile
            data.status = StatusOrder.Busy
            data.save()
            return Response(OrderSerializer(data).data)


class UnsubscribeOrder(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


# Отписаться от приёма
    def get(self, request, pk):
        data = Order.objects.get(pk=pk)
        parent = self.request.user.profile
        if parent.status == 'Родитель' and data.parent == parent:
            data.parant = None
            data.status = StatusOrder.Svobodno
            data.save()
            return Response(OrderSerializer(data).data)


def index(request):
    return HttpResponse('<h1>Hello</h1>')


# _________________________________________________________________________________________________
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
