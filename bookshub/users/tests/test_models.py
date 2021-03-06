from ...utils.tests import BaseTestCase
from ..models import User


class UserModelTestCase(BaseTestCase):
    def setUp(self):
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

    def test_custom_user_model_should_have_expected_number_of_fields(self):
        """
        Tests the expected number of fields in custom User model.
        """
        self.assertEqual(len(self.user._meta.fields), 32)

    def test_get_full_name_should_concatenate_names(self):
        """
        Tests that get_full_name returns the user's first name
        plus the last name, with a space in between.
        """
        self.assertEqual(self.user.get_full_name(), 'Juan Pueblo')

    def test_get_short_name_should_return_first_name(self):
        """
        Tests that get_short_name returns the user's first name
        """
        self.assertEqual(self.user.get_short_name(), 'Juan')

    def test_user_password_reset_token(self):
        """
        Tests that password_reset_token returns a token that the manager's
        get_from_password_reset_token can use to return a User.
        """
        token = self.user.password_reset_token
        user = User.objects.get_from_password_reset_token(token)

        self.assertEqual(self.user, user)

    def test_user_set_password_changes_token_version(self):
        """
        Tests that set_password set's the user password and
        changes the token_version.
        """
        password = str(self.user.password)
        token_version = self.user.token_version

        self.user.set_password('newpassword')

        self.assertNotEqual(self.user.password, password)
        self.assertNotEqual(self.user.token_version, token_version)

    def test_user_set_email_update_gravatar_url(self):
        """
        Tests that setting/changing email updates gravatar_url.
        """
        gravatar_url = self.user.gravatar_url

        self.user.email = 'anotheremail@example.com'
        self.user.save()

        self.assertFalse(gravatar_url == self.user.gravatar_url)

    def test_active_user_manager(self):
        """
        Tests that active user manager returns active users.
        """
        self.user.is_active = False
        self.user.save()

        self.assertEqual(User.active.count(), 0)
