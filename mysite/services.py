"Для того чтоб загружались модели "
import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'Project.settings')
django.setup()

from mysite.models import *


def all_objects(model):
    return model.objects.all()


def filter_objects(model, **kwargs):
    return model.objects.filter(**kwargs)


def create_object(model, **kwargs):
    return model.objects.create(**kwargs)


# me = Profile.objects.get(id=4)
# print(me.status)
# relationships = me.request_to_relation_childrens.all()
# data = {'name':[]}
# for relationship in relationships:
#     for profile in relationship.owner.all():
#         data['name'].extend([profile.status])
#
#
# data['name'].extend(['dima'])
# print(data)
# print(json.dumps(data))
