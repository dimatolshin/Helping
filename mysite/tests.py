from django.test import TestCase
from rest_framework.test import APITestCase
from mysite.models import Profile, Relationship, Task, InfoStatus
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from rest_framework import status
from mysite.serializers import UserSerializer


# class ProfileModelTest(TestCase):
#     def test_profile_creation(self):
#         user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
#         profile = Profile.objects.create(user=user, status='active', birth_date='1990-01-01', name='John', surname='Doe')
#
#         self.assertEqual(profile.user.username, 'testuser')
#         self.assertEqual(profile.status, 'active')
#         self.assertEqual(str(profile.birth_date), '1990-01-01')
#         self.assertEqual(profile.name, 'John')
#         self.assertEqual(profile.surname, 'Doe')
#
#
# class RelationshipModelTest(TestCase):
#     def setUp(self):
#         # Создание пользователей Django
#         self.parent_user = User.objects.create_user(username='parent_user', email='parent@example.com', password='password')
#         self.child_user = User.objects.create_user(username='child_user', email='child@example.com', password='password')
#
#         # Создание тестовых данных для профилей пользователей
#         self.parent_profile = Profile.objects.create(user_id=self.parent_user.id, name='Parent', surname='Smith')
#         self.child_profile = Profile.objects.create(user_id=self.child_user.id, name='Child', surname='Smith')
#
#     def test_relationship_creation(self):
#         # Создание объекта Relationship с указанием родителя, ребенка и запросов отношений
#         relationship = Relationship.objects.create(parent=self.parent_profile,
#                                                    children=self.child_profile)
#         relationship.requests_to_parents.add(self.parent_profile)
#         relationship.requests_to_childrens.add(self.child_profile)
#
#         # Проверка, что свойства объекта Relationship установлены правильно
#         self.assertEqual(relationship.parent, self.parent_profile)
#         self.assertEqual(relationship.children, self.child_profile)
#         self.assertIn(self.parent_profile, relationship.requests_to_parents.all())
#         self.assertIn(self.child_profile, relationship.requests_to_childrens.all())
#
#
# class TaskModelTest(TestCase):
#
#     def setUp(self):
#         self.parent_profile = Profile.objects.create(
#             user=User.objects.create_user(username='parent_user', password='password'), name='Parent', surname='Smith')
#         self.child_profile = Profile.objects.create(
#             user=User.objects.create_user(username='child_user', password='password'), name='Child', surname='Smith')
#
#     def test_task_creation(self):
#         # Создаем объект Task
#         task = Task.objects.create(
#             text='Sample task text',
#             parent=self.parent_profile,
#             children=self.child_profile,
#             date=datetime.date(2022, 1, 28),
#             status=InfoStatus.COMPLETED,
#         )
#
#         # Проверяем, что объект Task был создан правильно
#         self.assertEqual(task.text, 'Sample task text')
#         self.assertEqual(task.parent, self.parent_profile)
#         self.assertEqual(task.children, self.child_profile)
#         self.assertEqual(task.date, datetime.date(2022, 1, 28))
#         self.assertEqual(task.status, InfoStatus.COMPLETED)
#
#         # Проверяем, что объект Task сохранен в базе данных
#         saved_task = Task.objects.get(id=task.id)
#         self.assertEqual(saved_task, task)


class UserViewSetTest(APITestCase):

    def test_list_users(self):
        url = '/users/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        self.assertEqual(response.data, serializer.data)