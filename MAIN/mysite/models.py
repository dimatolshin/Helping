from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default='Helping-Project/MAIN/photo/default.jpg', upload_to='photo')
    birth_date = models.DateField(blank=True, auto_now=False, auto_now_add=False, null=True)

    def __str__(self):
        return f'{self.user.username}'


class Children(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default='Helping-Project/MAIN/photo/default.jpg', upload_to='photo')
    birth_date = models.DateField(blank=True, auto_now=False, auto_now_add=False, null=True)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='childrens')

    def __str__(self):
        return f'{self.user.username}'


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
