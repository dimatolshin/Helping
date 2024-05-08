from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=15, blank=True, null=True)
    surname = models.CharField(max_length=15, blank=True, null=True)
    mobile_number = models.IntegerField(default=0, blank=True, null=True)
    photo = models.ImageField(default='Helping-Project/MAIN/photo/default.jpg', upload_to='photo')
    birth_date = models.DateField(blank=True, auto_now=False, auto_now_add=False, null=True)


class Parent(models.Model):
    profile = models.OneToOneField(Profile, related_name='parent')


class Children(models.Model):
    profile = models.OneToOneField(Profile, related_name='children')


class Relation(models.Model):
    parents = ????????????????????????????????
    requests_to_parents = models.ManyToManyField(Parent, related_name='relation_parents')
    childrens = ??????????????????
    requests_to_childrens = models.ManyToManyField(Children, related_name='relation_parents')

    class InfoStatus(models.TextChoices):
        INITIAL = 'INITIAL',
        COMPLETED = 'COMPLETED'

    class Task(models.Model):
        text = models.TextField(max_length=1000000)
        date = models.DateField(default=now)
        parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='tasks')
        children = models.ForeignKey(Children, on_delete=models.CASCADE, related_name='tasks')
        status = models.CharField(max_length=10, choices=InfoStatus.choices, default=InfoStatus.INITIAL)

        def __str__(self):
            return f'Родитель:{self.user.username},Ребёнок:{self.user.username},Задача:{self.text}, Статус:{self.status}'
