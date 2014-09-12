from ...utils.tests import BaseTestCase
from ..models import User
from ..serializers import (SignupSerializer,
                           ForgotPasswordSerializer, ResetPasswordSerializer,
                           SigninSerializer,
                           UserSerializer,
                           UserSettingsSerializer, ChangePasswordSerializer)


class SignupSerializerTestCase(BaseTestCase):
    def setUp(self):
        self.create_user()

        self.data = {
            'email': 'juan@example.com',
            'username': 'juan',
            'password': 'abc123',
            'first_name': 'Juan',
            'last_name': 'Pueblo',
            'phone': '111-111-1111',
            'type': 'educational',
            'title': 'student'
        }

    def test_serializer_empty_object(self):
        """
        Tests that serializer.object returns expected data when empty.
        """
        serializer = SignupSerializer()
        self.assertEqual(serializer.object, None)

    def test_serializer_should_return_expected_data_if_valid(self):
        """
        Tests that serializer.object should return expected data when valid.
        """
        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        serializer_data = serializer.object

        user = User.objects.get(username='juan')

        expected_data = UserSerializer(user).data

        self.assertEqual(serializer_data, expected_data)

    def test_serializer_should_return_error_email_exists(self):
        """
        Tests that serializer should return an error if an email exists.
        """
        self.data['email'] = 'jpueblo@example.com'

        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        expected_error = {
            'email': ['Email already in use']
        }

        self.assertEqual(serializer.errors, expected_error)

    def test_serializer_should_return_error_username_exists(self):
        """
        Tests that serializer should return error if username exists.
        """
        self.data['username'] = 'jpueblo'
        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        expected_error = {
            'username': ['Username already in use']
        }

        self.assertEqual(serializer.errors, expected_error)

    def test_signup_should_return_created_user(self):
        """
        Tests that serializer.signup() should return the created user.
        """
        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        expected_user = User.objects.filter(username=self.data['username'])

        self.assertEqual(expected_user.count(), 1)

    def test_create_user_should_return_created_user(self):
        """
        Tests that serializer.create_user() should return the created user.
        """
        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()
        expected_user = User.objects.filter(username=self.data['username'])

        self.assertEqual(expected_user.count(), 1)

    def test_serializer_should_validate_password_requirements(self):
        """
        Tests that serializer validates password field.
        """
        self.data['password'] = 'a.'
        serializer = SignupSerializer(data=self.data)
        serializer.is_valid()

        expected_error = {
            'password': [
                'Ensure this value has at least 6 characters (it has 2).'
            ]
        }

        self.assertEqual(serializer.errors, expected_error)


class SigninSerializerTestCase(BaseTestCase):
    def setUp(self):
        self.create_user()

        self.data = {
            'email': self.email,
            'password': self.password
        }

    def test_empty(self):
        serializer = SigninSerializer()
        expected = {
            'email': ''
        }

        self.assertEqual(serializer.data, expected)

    def test_create(self):
        serializer = SigninSerializer(data=self.data)
        is_valid = serializer.is_valid()

        expected_response = UserSerializer(self.user).data

        self.assertTrue(is_valid)
        self.assertEqual(expected_response['username'], self.username)

    def test_invalid_credentials(self):
        self.data['password'] = 'wrongpassword'
        serializer = SigninSerializer(data=self.data)
        is_valid = serializer.is_valid()

        expected_error = {
            'non_field_errors': ['Unable to login with provided credentials.']
        }

        self.assertFalse(is_valid)
        self.assertEqual(serializer.errors, expected_error)

    def test_disabled_user(self):
        self.user.is_active = False
        self.user.save()

        serializer = SigninSerializer(data=self.data)
        is_valid = serializer.is_valid()

        expected_error = {
            'non_field_errors': ['Unable to login with provided credentials.']
        }

        self.assertFalse(is_valid)
        self.assertEqual(serializer.errors, expected_error)

    def test_required_fields(self):
        serializer = SigninSerializer(data={})
        is_valid = serializer.is_valid()

        expected_error = {
            'email': ['This field is required.'],
            'password': ['This field is required.']
        }

        self.assertFalse(is_valid)
        self.assertEqual(serializer.errors, expected_error)


class ForgotPasswordSerializerTestCase(BaseTestCase):
    def setUp(self):
        self.create_user()
        self.email = self.user.email

        self.data = {
            'email': self.email
        }

    def test_serializer_empty_object(self):
        """
        Tests that serializer.object returns expected data when empty.
        """
        serializer = ForgotPasswordSerializer()
        self.assertEqual(serializer.object, None)
        self.assertEqual(serializer.data, {'email': ''})

    def test_serializer_should_return_expected_data_if_valid(self):
        """
        Tests that serializer.object should return expected data when valid.
        """
        serializer = ForgotPasswordSerializer(data=self.data)
        serializer.is_valid()

        expected_data = {
            'email': self.email
        }

        self.assertEqual(serializer.object, expected_data)

    def test_serializer_should_return_expected_error_email_required(self):
        """
        Tests that serializer.errors should return expected
        error when invalid.
        """
        self.data['email'] = None
        serializer = ForgotPasswordSerializer(data=self.data)
        serializer.is_valid()

        expected_error = {
            'email': ['This field is required.']
        }

        self.assertEqual(serializer.errors, expected_error)
        self.assertEqual(serializer.object, None)
        self.assertEqual(serializer.data, {'email': ''})

    def test_serializer_should_return_expected_error_no_user_found(self):
        """
        Tests that serializer.object should return expected
        error when no user found for given email.
        """
        self.data['email'] = 'nonexistent@example.com'
        serializer = ForgotPasswordSerializer(data=self.data)
        serializer.is_valid()

        expected_error = {
            'email': ['No user found.']
        }

        self.assertEqual(serializer.errors, expected_error)
        self.assertEqual(serializer.object, None)
        self.assertEqual(serializer.data, {'email': ''})


class ResetPasswordSerializerTestCase(BaseTestCase):
    def setUp(self):
        self.create_user()
        self.email = self.user.email

        self.data = {
            'token': self.user.password_reset_token,
            'new_password': 'newpassword'
        }

    def test_serializer_empty_object(self):
        """
        Tests that serializer.object returns expected data when empty.
        """
        serializer = ResetPasswordSerializer()

        self.assertEqual(serializer.object, None)
        self.assertEqual(serializer.data, {})

    def test_serializer_should_return_expected_data_if_valid(self):
        """
        Tests that serializer.object should return expected data when valid.
        """
        serializer = ResetPasswordSerializer(data=self.data)
        serializer.is_valid()
        expected_data = {
            'password_reset': True
        }

        self.assertEqual(serializer.object, expected_data)

    def test_serializer_should_return_expected_error_if_invalid(self):
        """
        Tests that serializer.errors should return expected
        error when invalid.
        """
        self.data['new_password'] = None
        self.data['token'] = None
        serializer = ResetPasswordSerializer(data=self.data)
        serializer.is_valid()

        expected_error = {
            'new_password': ['This field is required.'],
            'token': ['This field is required.']
        }

        self.assertEqual(serializer.errors, expected_error)
        self.assertEqual(serializer.object, None)
        self.assertEqual(serializer.data, {})

    def test_serializer_should_return_expected_error_invalid_token(self):
        """
        Tests that serializer.errors should return expected
        error for invalid token.
        """
        self.data['token'] = 'invalidtoken'
        self.data['new_password'] = '123456'
        serializer = ResetPasswordSerializer(data=self.data)
        serializer.is_valid()

        expected_error = {
            'token': ['Invalid password reset token.']
        }

        self.assertEqual(serializer.errors, expected_error)
        self.assertEqual(serializer.object, None)
        self.assertEqual(serializer.data, {})

    def test_serializer_validate_should_set_user_password(self):
        """
        Tests that serializer.validate() should set new password.
        """
        serializer = ResetPasswordSerializer(data=self.data)
        serializer.is_valid()

        user = User.objects.get(email=self.user.email)

        self.assertTrue(user.check_password(self.data['new_password']))

    def test_serializer_should_validate_password_requirements(self):
        """
        Tests that serializer validates password field.
        """
        self.data['new_password'] = 'a.'
        serializer = ResetPasswordSerializer(data=self.data)
        serializer.is_valid()

        expected_error = {
            'new_password': [
                'Ensure this value has at least 6 characters (it has 2).'
            ]
        }

        self.assertEqual(serializer.errors, expected_error)


class UserSerializerTestCase(BaseTestCase):
    def setUp(self):
        self.create_user()

    def test_serializer_returns_expected_data_for_object(self):
        user_data = UserSerializer(self.user).data
        data_keys = [key for key in user_data.keys()]

        expected_keys = [
            'id', 'username', 'email', 'first_name', 'last_name', 'phone',
            'type', 'status', 'title', 'address_1', 'address_2',
            'country', 'city', 'state', 'zip', 'facebook_url',
            'twitter_url', 'google_url', 'gravatar_url', 'institution',
            'department', 'description', 'logo', 'company_name', 'token'
        ]

        self.assertEqual(data_keys, expected_keys)


class UserSettingsSerializerTestCase(BaseTestCase):
    def setUp(self):
        self.serializer_class = UserSettingsSerializer

    def test_serializer_empty_data(self):
        """
        Tests that serializer.data doesn't return any data.
        """
        serializer = self.serializer_class()
        expected_data = {
            'username': '',
            'email': '',
            'first_name': '',
            'last_name': '',
            'phone': '',
            'title': '',
            'address_1': '',
            'address_2': '',
            'country': '',
            'city': '',
            'state': '',
            'zip': '',
            'facebook_url': '',
            'twitter_url': '',
            'google_url': '',
            'gravatar_url': '',
            'institution': '',
            'department': '',
            'description': '',
            'logo': '',
            'company_name': '',
        }

        self.assertEqual(serializer.data, expected_data)

    def test_serializer_validation(self):
        """
        Tests serializer's expected validation errors.
        """
        serializer = self.serializer_class(data={})
        serializer.is_valid()

        expected_errors = {
            'email': ['This field cannot be blank.'],
        }

        self.assertEqual(serializer.errors, expected_errors)

    def test_serializer_with_user_instance(self):
        """
        Tests serializer's expected data with user instance.
        """
        self.create_user()

        serializer = self.serializer_class(instance=self.user)
        serializer.is_valid()

        expected_data = {
            'id': self.user.id,
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'gravatar_url': self.user.gravatar_url,
            'phone': self.user.phone,
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
            'institution': '',
            'department': '',
            'description': '',
            'logo': '',
            'company_name': '',
            'token': self.user.token,
        }

        self.assertEqual(serializer.data, expected_data)

    def test_serializer_should_validate_unique_email(self):
        """
        Tests serializer should validate email.
        """
        self.create_user()
        self.create_another_user()

        data = {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'username': self.user.username,
            'email': 'jsmith@example.com'
        }

        serializer = self.serializer_class(data=data, instance=self.user)
        serializer.is_valid()

        expected_error = {
            'email': ['Email already exists.']
        }

        self.assertEqual(serializer.errors, expected_error)

    def test_serializer_should_validate_unique_username(self):
        """
        Tests serializer should validate username.
        """
        self.create_user()
        self.create_another_user()

        data = {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'username': 'jsmith',
            'email': self.user.email
        }

        serializer = self.serializer_class(data=data, instance=self.user)
        serializer.is_valid()

        expected_error = {
            'username': ['Username already exists.']
        }

        self.assertEqual(serializer.errors, expected_error)

    def test_serializer_should_validate_username(self):
        """
        Tests serializer should validate username.
        """
        self.create_user()
        self.create_another_user()

        data = {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'username': self.user.email,
            'email': self.user.email
        }

        serializer = self.serializer_class(data=data, instance=self.user)
        serializer.is_valid()

        expected_error = {
            'username': ['Invalid username.']
        }

        self.assertEqual(serializer.errors, expected_error)

    def test_serializer_save_should_update_user(self):
        """
        Tests serializer save should update user.
        """
        self.create_user()
        self.create_another_user()

        data = {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'username': self.user.username,
            'email': self.user.email,
        }

        serializer = self.serializer_class(data=data, instance=self.user)
        serializer.is_valid()
        serializer.save()

        expected_data = {
            'id': self.user.id,
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'gravatar_url': self.user.gravatar_url,
            'phone': self.user.phone,
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
            'institution': '',
            'department': '',
            'description': '',
            'logo': '',
            'company_name': '',
            'token': self.user.token,
        }

        self.assertEqual(serializer.data, expected_data)


class ChangePasswordSerializerTestCase(BaseTestCase):
    def setUp(self):
        self.serializer_class = ChangePasswordSerializer

    def test_serializer_empty_data(self):
        """
        Tests that serializer.data doesn't return any data.
        """
        serializer = self.serializer_class()

        self.assertEqual(serializer.data, {})

    def test_serializer_validation(self):
        """
        Tests serializer's expected validation errors.
        """
        serializer = self.serializer_class(data={})
        serializer.is_valid()

        expected_errors = {
            'current_password': ['This field is required.'],
            'new_password': ['This field is required.'],
            'new_password_confirmation': ['This field is required.']
        }

        self.assertEqual(serializer.errors, expected_errors)

    def test_serializer_should_validate_current_password(self):
        """
        Tests serializer should validate current password.
        """
        self.create_user()

        data = {
            'current_password': 'abc12345',
            'new_password': 'abc1234',
            'new_password_confirmation': 'abc1234'
        }

        serializer = self.serializer_class(data=data, instance=self.user)
        serializer.is_valid()

        expected_error = {
            'current_password': ['Current password is invalid']
        }

        self.assertEqual(serializer.errors, expected_error)

    def test_serializer_should_validate_passwords_match(self):
        """
        Tests serializer should validate if passwords match.
        """
        self.create_user()

        data = {
            'current_password': self.password,
            'new_password': 'abc1234',
            'new_password_confirmation': 'abc12345'
        }

        serializer = self.serializer_class(data=data, instance=self.user)
        serializer.is_valid()

        expected_error = {
            'new_password_confirmation':
            ["The passwords are not the same"]
        }

        self.assertEqual(serializer.errors, expected_error)

    def test_serializer_should_change_password(self):
        """
        Tests serializer should change password.
        """
        self.create_user()

        data = {
            'current_password': self.password,
            'new_password': 'abc12345',
            'new_password_confirmation': 'abc12345'
        }

        serializer = self.serializer_class(data=data, instance=self.user)
        serializer.is_valid()

        self.assertTrue(serializer.object.check_password('abc12345'))
