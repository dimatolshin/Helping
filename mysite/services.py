"Для того чтоб загружались модели "
import os
import django
import json
from rest_framework.authtoken.models import Token

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'Project.settings')
django.setup()

from mysite.models import *


def all_objects(model):
    return model.objects.all()


def filter_objects(model, **kwargs):
    return model.objects.filter(**kwargs)


def create_object(model, **kwargs):
    return model.objects.create(**kwargs)


def set_token_cookie(response, user):
    token = Token.objects.get(user=user)
    response.set_cookie(
        'access_token',  # Имя куки
        token,  # Значение токена
        httponly=True,  # Куки недоступны для JavaScript на клиенте (для безопасности)
        samesite='Lax'  # Предотвращение отправки куки при запросах с других сайтов
    )
    return response
