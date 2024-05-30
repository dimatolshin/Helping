from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User


class GenderStatus(models.TextChoices):
    Родитель = 'Родитель',
    Ребёнок = 'Ребёнок',
    Другое = 'Другое'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    status = models.CharField(max_length=10, choices=GenderStatus.choices)
    photo = models.ImageField(default='Helping-Project/MAIN/photo/default.jpg', upload_to='photo')
    birth_date = models.DateField(blank=True, auto_now=False, auto_now_add=False, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    surname = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}'


class Relationship(models.Model):
    parent = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='parents', blank=True, null=True)
    children = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='childrens', blank=True, null=True)
    requests_to_parents = models.ManyToManyField(Profile, related_name='relation_parents')
    requests_to_childrens = models.ManyToManyField(Profile, related_name='relation_childrens')

    def __str__(self):
        return f'Родитель:{self.parent.user.username}-Ребенок:{self.children.user.username}'


class InfoStatus(models.TextChoices):
    INITIAL = 'INITIAL',
    COMPLETED = 'COMPLETED'


class Task(models.Model):
    text = models.TextField(max_length=1000000)
    date = models.DateField(default=now)
    parent = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='parents_task')
    children = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='children_task')
    status = models.CharField(max_length=10, choices=InfoStatus.choices, default=InfoStatus.INITIAL)


class Topic(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False, unique=True)
    current_profiles = models.ManyToManyField(Profile, related_name='topics', blank=True)

    def str(self):
        return f'Тема:{self.name}'


class Chat(models.Model):
    room = models.ForeignKey(Topic, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'Профиль:{self.profile.name} Kомната{self.room.name}'


class Article(models.Model):
    name = models.CharField(max_length=250)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='articles')
    text = models.TextField(max_length=100000)
    like_list = models.ManyToManyField(Profile, related_name='articles_like_list', blank=True)
    like = models.IntegerField(default=0)

    def str(self):
        return f'Профиль:{self.profile.name} Cтатья:{self.name} Лайки{self.like}'


class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500)
    like_list = models.ManyToManyField(Profile, related_name='comments_like_list', blank=True)
    like = models.IntegerField(default=0)

    def str(self):
        return f'Профиль:{self.profile.name} Статья:{self.article.name} Лайки{self.like}'
