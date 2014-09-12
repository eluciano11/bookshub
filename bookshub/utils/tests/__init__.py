from django.test import TestCase

from rest_framework.test import APIClient

from ...users.models import User


class BaseTestCase(TestCase):
    users = {}

    def create_user(self):
        self.username = 'jpueblo'
        self.email = 'jpueblo@example.com'
        self.password = 'abc123'
        self.first_name = 'Juan'
        self.last_name = 'Pueblo'
        self.phone = '111-111-111'
        self.type = 'educational'
        self.title = 'student'

        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            phone=self.phone,
            type=self.type,
            title=self.title
        )

        self.users[self.username] = self.user

    def create_another_user(self, username='jsmith'):
        password = 'abc123'
        email = '{}@example.com'.format(username)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=username[:1].upper(),
            last_name=username[1:].upper(),
            phone='111-111-1111',
            type='educational',
            title='student'
        )

        self.users[username] = user

        return user


class AuthenticatedAPITestCase(BaseTestCase):
    """
    This test case class creates a basic user
    and does authentication for you using a JWT token
    """

    def setUp(self):
        self.create_user()

        self.token = self.user.token

        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {0}'.format(self.token))
