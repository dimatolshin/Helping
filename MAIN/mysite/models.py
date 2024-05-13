from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User


class GenderStatus(models.TextChoices):
    Родитель = 'Родитель',
    Ребёнок = 'Ребёнок',
    Другое = 'Другое'


class UserUpgrade(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=GenderStatus.choices)
    photo = models.ImageField(default='Helping-Project/MAIN/photo/default.jpg', upload_to='photo')
    birth_date = models.DateField(blank=True, auto_now=False, auto_now_add=False, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    surname = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}'


class Relationship(models.Model):
    parent = models.ForeignKey(UserUpgrade, on_delete=models.CASCADE, related_name='parents', blank=True, null=True)
    children = models.ForeignKey(UserUpgrade, on_delete=models.CASCADE, related_name='childrens', blank=True, null=True)
    requests_to_parents = models.ManyToManyField(UserUpgrade, related_name='relation_parents')
    requests_to_childrens = models.ManyToManyField(UserUpgrade, related_name='relation_childrens')

    def __str__(self):
        return f'Родитель:{self.parent.user.username}-Ребенок:{self.children.user.username}'

class InfoStatus(models.TextChoices):
    INITIAL = 'INITIAL',
    COMPLETED = 'COMPLETED'


class Task(models.Model):
    text = models.TextField(max_length=1000000)
    date = models.DateField(default=now)
    parent = models.ForeignKey(UserUpgrade, on_delete=models.CASCADE, related_name='parents_task')
    children = models.ForeignKey(UserUpgrade, on_delete=models.CASCADE, related_name='children_task')
    status = models.CharField(max_length=10, choices=InfoStatus.choices, default=InfoStatus.INITIAL)
