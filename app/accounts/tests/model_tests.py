from django.test import TestCase
from accounts.models import MCCUser, UserManager, EmailRequiredException


class UserManagerTestCase(TestCase):
    def setUp(self):
        self.user = MCCUser.objects._create_user(
            first_name="test",
            last_name="user",
            email="tess1@TEST.com",
            password="1234"
        )
        self.admin_user = MCCUser.objects.create_admin_user(
            first_name="admin",
            last_name="user",
            email="admin@TEST.com",
            password="1234"
        )

    def tearDown(self) -> None:
        pass

    def test_private_create_user(self):
        """Test normalisation email, default user is staff, and is not superuser"""

        # Test email is normalised
        self.assertEqual(self.user.email, "tess1@test.com")
        with self.assertRaises(
            EmailRequiredException,
        ):
            MCCUser.objects._create_user(
                email=None,
                first_name="Dave",
                last_name="Help",
                password="my password is cool"
            )

        self.assertTrue(self.user.pk is not None)

    def test_create_user(self):
        """Test the expected behaviour, test Exception is raised if not expected"""
        self.assertFalse(self.user.is_staff, "User should not be staff by default")
        self.assertFalse(self.user.is_superuser, "Staff member should not default to superuser")

    def test_create_admin_user(self):
        """Test the expected behaviour, test Exception is raised if not expected"""
        self.assertTrue(self.admin_user.is_staff, "Admin should be staff by default")
        self.assertFalse(self.admin_user.is_superuser, "Staff member should not default to superuser")

    def test_create_superuser(self):
        """Test the expected behaviour, test Exception is raised if not expected"""
        superuser = UserManager.create_superuser(MCCUser.objects, "test2@test.com", password=None, is_staff=True)
        self.assertTrue(superuser.is_staff, "Super users should always be staff")
        self.assertTrue(superuser.is_superuser, "Super used should be a super user in the model")
        self.assertIsInstance(superuser, MCCUser)
