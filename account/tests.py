from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='jkariuki',
            email='jkariuki@email.com',
            password='somepassword',
        )
        self.assertEqual(user.username, 'jkariuki')
        self.assertEqual(user.email, 'jkariuki@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='mzito',
            email='mzito@email.com',
            password='superpassword'
        )
        self.assertEqual(admin_user.username, 'mzito')
        self.assertEqual(admin_user.email, 'mzito@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
