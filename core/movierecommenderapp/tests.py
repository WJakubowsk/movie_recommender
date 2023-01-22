from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Show


class ViewTest(TestCase):

    def test_search(self):
        # add a show to the database
        Show.objects.create(
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

