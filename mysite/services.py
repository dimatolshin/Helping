"Для того чтоб загружались модели "
import os

from django.http import HttpResponse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'Project.settings')
import django

django.setup()

from mysite.models import *


def all_objects(model):
    return model.objects.all()


def filter_objects(model, **kwargs):
    return model.objects.filter(**kwargs)


def create_object(model, **kwargs):
    return model.objects.create(**kwargs)


