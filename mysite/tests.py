from django.test import TestCase
from django.test import APITeasCase
from mysite.models import Profile, Relationship, Task, InfoStatus
from django.contrib.auth.models import User
from django.utils import timezone


class ProfileModelTest(TestCase):
    def test_profile_creation(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        profile = Profile.objects.create(user=user, status='active', birth_date='1990-01-01', name='John', surname='Doe')

        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.status, 'active')
        self.assertEqual(str(profile.birth_date), '1990-01-01')
        self.assertEqual(profile.name, 'John')
        self.assertEqual(profile.surname, 'Doe')


class RelationshipModelTest(TestCase):
    def setUp(self):
        # Создание пользователей Django
        self.parent_user = User.objects.create_user(username='parent_user', email='parent@example.com', password='password')
        self.child_user = User.objects.create_user(username='child_user', email='child@example.com', password='password')

        # Создание тестовых данных для профилей пользователей
        self.parent_profile = Profile.objects.create(user_id=self.parent_user.id, name='Parent', surname='Smith')
        self.child_profile = Profile.objects.create(user_id=self.child_user.id, name='Child', surname='Smith')

    def test_relationship_creation(self):
        # Создание объекта Relationship с указанием родителя, ребенка и запросов отношений
        relationship = Relationship.objects.create(parent=self.parent_profile,
                                                   children=self.child_profile)
        relationship.requests_to_parents.add(self.parent_profile)
        relationship.requests_to_childrens.add(self.child_profile)

        # Проверка, что свойства объекта Relationship установлены правильно
        self.assertEqual(relationship.parent, self.parent_profile)
        self.assertEqual(relationship.children, self.child_profile)
        self.assertIn(self.parent_profile, relationship.requests_to_parents.all())
        self.assertIn(self.child_profile, relationship.requests_to_childrens.all())


class TaskModelTest(TestCase):

    def setUp(self):
        self.parent_profile = Profile.objects.create(user_id=1, name='Parent', surname='Smith')
        self.child_profile = Profile.objects.create(user_id=2, name='Child', surname='Smith')

    def test_task_creation(self):
        # Создаем объект Task
        task = Task.objects.create(
            text='Sample task text',
            date=timezone.now().date(),
            parent=parent_profile,
            children=child_profile,
            status=InfoStatus.INITIAL
        )

        # Проверяем, что объект Task был создан правильно
        self.assertEqual(task.text, 'Sample task text')
        self.assertEqual(task.date, timezone.now().date())
        self.assertEqual(task.parent, parent_profile)
        self.assertEqual(task.children, child_profile)
        self.assertEqual(task.status, InfoStatus.INITIAL)

        # Проверяем, что объект Task сохранен в базе данных
        saved_task = Task.objects.get(id=task.id)
        self.assertEqual(saved_task, task)


