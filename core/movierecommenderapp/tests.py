from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Show


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

    def test_search(self):
        # add a show to the database
        Show.objects.create(
            show_id='420',
            title='Test Movie',
            category='Test Category',
            year='2020',
            poster='https://www.test.com',
            director='Test Director',
            actors='Test Actor',
            runtime='100 min',
            plot='Test Plot',
            box_office='Test Box Office'
        )

        response = self.client.get(reverse('search'), {'q': 'Test Movie'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Movie')
        self.assertTemplateUsed(response, 'api_results.html')

        response2 = self.client.get(reverse('search'), {'q': 'Not Existing Movie'})
        self.assertEqual(response2.status_code, 200)
        self.assertNotContains(response2, 'Not Existing Movie')
        self.assertTemplateUsed(response2, 'home.html')
