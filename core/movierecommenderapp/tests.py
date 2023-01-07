from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class ViewTest(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        self.assertTrue(User.objects.filter(username='testuser').exists())

        user.delete()

        self.assertFalse(User.objects.filter(username='testuser').exists())