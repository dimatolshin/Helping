import datetime
from datetime import date

from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User


class GenderStatus(models.TextChoices):
    Родитель = 'Родитель',
    Ребёнок = 'Ребёнок',
    Эксперт = 'Эксперт'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    status = models.CharField(max_length=10, choices=GenderStatus.choices)
    photo = models.ImageField(default='Helping-Project/MAIN/photo/default.jpg', upload_to='photo')
    birth_date = models.DateField(blank=True, auto_now=False, auto_now_add=False, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    surname = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f'Username:{self.user.username} -- Name:{self.name} '


class Relationship(models.Model):
    parent = models.ManyToManyField(Profile, related_name='relation_parents', blank=True)
    children = models.ManyToManyField(Profile, related_name='relation_childrens', blank=True)
    requests_to_parents = models.ManyToManyField(Profile, related_name='request_to_relation_parents', blank=True)
    requests_to_childrens = models.ManyToManyField(Profile, related_name='request_to_relation_childrens', blank=True)
    owner = models.ManyToManyField(Profile, related_name='owner', blank=True)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'Имя:{self.name}'



class PodCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='podcategory', on_delete=models.CASCADE)

    def __str__(self):
        return f'Имя:{self.name} -- Категория:{self.category.name}'


class Picture(models.Model):
    image = models.ImageField(upload_to='all_picture')
    category = models.ForeignKey(Category, related_name='picture', on_delete=models.CASCADE, blank=True, null=True)
    podcategory = models.ForeignKey(PodCategory, related_name='picture', on_delete=models.CASCADE, blank=True,
                                    null=True)

    def __str__(self):
        return f'Категория:{self.category.name} -- Подкатегория:{self.podcategory.name}'


class InfoStatus(models.TextChoices):
    INITIAL = 'В разработке',
    COMPLETED = 'Сделал'
    NEGATIVE = 'Не сделал'
    WrongTime = 'Сделал не вовремя'


class Calendar(models.Model):
    parent = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='parent_calendar')
    date = models.DateField(default=date.today)


class Task(models.Model):
    #
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='tasks', null=True)
    text = models.CharField(max_length=100)
    start_time = models.TimeField(blank=True, null=True)
    finish_time = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=25, choices=InfoStatus.choices, default=InfoStatus.INITIAL)
    children = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='tasks_for_children', null=True)
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name='tasks', null=True)


class StatusOrder(models.TextChoices):
    Svobodno = 'Свободно',
    Busy = 'Занято'


class Order(models.Model):
    expert = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='order_expert')
    date = models.DateField(default=date.today)
    parent = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='order_parent')
    vk = models.CharField(max_length=100, blank=True, null=True)
    zoom = models.CharField(max_length=100, blank=True, null=True)
    telegram = models.CharField(max_length=100, blank=True, null=True)
    at_home = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=15, choices=StatusOrder.choices, default=StatusOrder.Svobodno)


class Time(models.Model):
    time = models.TimeField(blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='time')


class Room(models.Model):
    other = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_room', null=True)
    me = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='me_room', null=True)

    def __str__(self):
        return f'Другой:{self.other.name} -- Я:{self.me.name}'


class Message(models.Model):
    image = models.OneToOneField(Picture, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Профиль:{self.profile.name} Kомната:{self.room.name}'


class Article(models.Model):
    name = models.CharField(max_length=250)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='articles')
    text = models.TextField(max_length=100000)
    like_list = models.ManyToManyField(Profile, related_name='articles_like_list', blank=True)
    like = models.IntegerField(default=0)

    def __str__(self):
        return f'Профиль:{self.profile.user.username} -- Cтатья:{self.name} -- Лайки:{self.like}'


class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500)
    like_list = models.ManyToManyField(Profile, related_name='comments_like_list', blank=True)
    like = models.IntegerField(default=0)

    def str(self):
        return f'Профиль:{self.profile.name} Статья:{self.article.name} Лайки:{self.like}'
