from rest_framework import status
from rest_framework.test import APIClient

from ...utils.tests import BaseTestCase, AuthenticatedAPITestCase
from ..models import User
from ..serializers import UserSerializer


class SignupAPIViewTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()

    def test_post_valid_data(self):
        """
        Tests that POST request with valid data to endpoint
        returns expected data.
        """

        data = {
            'first_name': 'Juan',
            'last_name': 'Pueblo',
            'phone': '111-111-1111',
            'type': 'educational',
            'title': 'student',
            'email': 'jpueblo@example.com',
            'username': 'juan',
            'password': 'abc123',
        }

        response = self.client.post(
            '/api/auth/signup/', data, format='json')

        user = User.objects.get(email='jpueblo@example.com')

        expected_response = UserSerializer(user).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_post_valid_data_simple(self):
        """
        Tests that POST request with valid data to endpoint
        returns expected data. Skips signup domains and invites.
        """
        data = {
            'first_name': 'Juan',
            'last_name': 'Pueblo',
            'phone': '111-111-1111',
            'type': 'educational',
            'title': 'student',
            'email': 'jpueblo@example.com',
            'username': 'juan',
            'password': 'abc123',
        }

        response = self.client.post(
            '/api/auth/signup/', data, format='json')

        user = User.objects.get(email='jpueblo@example.com')

        expected_response = UserSerializer(user).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_post_invalid_data(self):
        """
        Tests that POST request with invalid data to endpoint
        returns expected error.
        """
        response = self.client.post('/api/auth/signup/')

        expected_response = {
            'error': {
                'first_name': ['This field is required.'],
                'last_name': ['This field is required.'],
                'phone': ['This field is required.'],
                'type': ['This field is required.'],
                'title': ['This field is required.'],
                'username': ['This field is required.'],
                'password': ['This field is required.'],
                'email': ['This field is required.'],
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)


class SigninAPIEndpoint(BaseTestCase):
    def setUp(self):
        self.client = APIClient()

        self.username = 'jpueblo'
        self.password = 'abc123'
        self.email = 'jpueblo@example.com'

        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            first_name='Juan',
            last_name='Pueblo',
            phone='111-111-1111',
            type='educational',
            title='student',
        )

    def test_post_valid_data_with_email(self):
        """
        Tests that POST request with valid email and password
        to endpoint returns expected data.
        """
        data = {
            'email': self.email,
            'password': self.password
        }

        response = self.client.post(
            '/api/auth/signin/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_post_invalid_data(self):
        """
        Tests that POST request with invalid data to endpoint
        returns expected error.
        """
        response = self.client.post('/api/auth/signin/')

        expected_response = {
            'error': {
                'password': [
                    'This field is required.'
                ],
                'email': [
                    'This field is required.'
                ]
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)

    def test_post_invalid_data_wrong_credentials(self):
        """
        Tests that POST request with wrong credentials to endpoint
        returns expected error.
        """
        data = {
            'email': '1@1.com',
            'password': 'mypassword'
        }

        response = self.client.post('/api/auth/signin/', data, format='json')

        expected_response = {
            'error': {
                'non_field_errors': [
                    'Unable to login with provided credentials.'
                ]
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)


class ForgotPasswordAPIViewTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()

        self.username = 'jpueblo'
        self.password = 'abc123'
        self.email = 'jpueblo@example.com'

        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            first_name='Juan',
            last_name='Pueblo',
            phone='111-111-1111',
            type='educational',
            title='student',
        )

        self.url = '/api/auth/forgot_password/'

    def test_post_valid_data(self):
        """
        Tests that POST request with valid data to endpoint
        returns expected data.
        """
        data = {
            'email': self.email,
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_post_invalid_data(self):
        """
        Tests that POST request with invalid data to endpoint
        returns expected error.
        """
        response = self.client.post(self.url)

        expected_response = {
            'error': {
                'email': ['This field is required.']
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)


class ResetPasswordAPIViewTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_user()

        self.url = '/api/auth/reset_password/'

    def test_post_valid_data(self):
        """
        Tests that POST request with valid data to endpoint
        returns expected data.
        """
        data = {
            'token': self.user.password_reset_token,
            'new_password': 'newpassword'
        }

        response = self.client.post(self.url, data, format='json')
        expected_response = {
            'password_reset': True
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_post_invalid_data(self):
        """
        Tests that POST request with invalid data to endpoint
        returns expected error.
        """
        response = self.client.post(self.url)

        expected_response = {
            'error': {
                'token': ['This field is required.'],
                'new_password': ['This field is required.']
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)


class UserSettingsAPIViewTestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super(UserSettingsAPIViewTestCase, self).setUp()

        self.url = '/api/auth/settings/'

    def test_get_for_loggedin_user(self):
        """
        Tests that endpoint returns expected response for logged in user.
        """
        response = self.client.get(self.url)
        expected_response = {
            'id': self.user.id,
            'username': self.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'phone': self.user.phone,
            'email': self.user.email,
            'title': self.user.title,
            'address_1': '',
            'address_2': '',
            'country': '',
            'city': '',
            'state': '',
            'zip': '',
            'facebook_url': '',
            'twitter_url': '',
            'google_url': '',
            'gravatar_url': self.user.gravatar_url,
            'institution': '',
            'department': '',
            'description': '',
            'logo': '',
            'company_name': '',
            'token': self.user.token,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_get_for_loggedout_user(self):
        """
        Tests that endpoint only works for logged in users.
        """
        self.client = APIClient()
        response = self.client.get(self.url)
        expected_response = {}

        expected_response = {
            'error': 'Authentication credentials were not provided.',
            'status_code': 401
        }

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, expected_response)

    def test_update_should_update_logged_in_user(self):
        """
        Tests that endpoint can be used to update logged in user's data.
        """
        data = {
            'username': self.username,
            'email': 'anotheremail@example.com'
        }

        response = self.client.patch(self.url, data)

        self.user = User.objects.get(username=self.username)

        expected_response = {
            'id': self.user.id,
            'username': self.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'phone': self.user.phone,
            'email': self.user.email,
            'title': self.user.title,
            'address_1': '',
            'address_2': '',
            'country': '',
            'city': '',
            'state': '',
            'zip': '',
            'facebook_url': '',
            'twitter_url': '',
            'google_url': '',
            'gravatar_url': self.user.gravatar_url,
            'institution': '',
            'department': '',
            'description': '',
            'logo': '',
            'company_name': '',
            'token': self.user.token,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_update_should_validate_name_length(self):
        """
        Tests that endpoint can be used to update logged in user's data.
        """
        data = {
            'first_name': 'a' * 40,
            'last_name': 'b' * 40,
            'email': 'anotheremail@example.com'
        }

        response = self.client.put(self.url, data)

        self.user = User.objects.get(email=self.email)

        expected_response = {
            'error': {
                'last_name': [
                    'Ensure this value has at most 30 characters (it has 40).'
                ],
                'first_name': [
                    'Ensure this value has at most 30 characters (it has 40).'
                ]
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)


class ChangePasswordAPIViewTestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super(ChangePasswordAPIViewTestCase, self).setUp()

        self.url = '/api/auth/change_password/'

    def test_post_for_loggedin_user_invalid_current_password(self):
        """
        Tests that endpoint checks for user's current password.
        """
        data = {
            'current_password': 'notmypassword',
            'new_password': 'abc123',
            'new_password_confirmation': 'abc123'
        }

        response = self.client.put(self.url, data)

        expected_response = {
            'error': {
                'current_password': ['Current password is invalid']
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)

    def test_post_for_loggedin_user_valid_current_password(self):
        """
        Tests that endpoint changes user's password.
        """
        data = {
            'current_password': self.password,
            'new_password': 'mynewpassword',
            'new_password_confirmation': 'mynewpassword'
        }

        response = self.client.put(self.url, data)

        self.user = User.objects.get(username=self.username)

        expected_response = {
            'id': self.user.id,
            'username': self.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'phone': self.user.phone,
            'email': self.email,
            'title': self.user.title,
            'address_1': '',
            'address_2': '',
            'country': '',
            'city': '',
            'state': '',
            'zip': '',
            'facebook_url': '',
            'twitter_url': '',
            'google_url': '',
            'gravatar_url': self.user.gravatar_url,
            'institution': '',
            'department': '',
            'description': '',
            'logo': '',
            'company_name': '',
            'token': self.user.token,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)
        self.assertTrue(self.user.check_password('mynewpassword'))


class UserAutoCompleteAPIViewTestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super(UserAutoCompleteAPIViewTestCase, self).setUp()

        self.url = '/api/autocomplete/users/'

    def test_get_for_loggedin_user(self):
        """
        Tests that endpoint returns expected response for logged in user.
        """
        user = self.create_another_user()
        response = self.client.get(self.url, {'search': 'j'})
        expected_response = [{
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'gravatar_url': user.gravatar_url,
            'type': user.type,
            'status': user.status,
            'title': user.title,
        }]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_get_active_users(self):
        """
        Tests that endpoint returns expected response with
        no inactive users.
        """
        user = self.create_another_user()
        user.is_active = False
        user.save()

        response = self.client.get(self.url, {'search': 'j'})

        expected_response = []

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)


class CancelAccountAPIViewTestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super(CancelAccountAPIViewTestCase, self).setUp()

        self.url = '/api/auth/cancel_account/'

    def test_post_deactivates_user_account(self):
        data = {
            'current_password': self.password,
        }

        response = self.client.put(self.url, data)

        user = User.objects.get(pk=self.user.pk)

        self.assertFalse(user.is_active)
        self.assertEqual(response.status_code, 200)
