from django.test import TestCase
from django.urls import reverse

class ViewTest(TestCase):
    def test_view(self):
        response = self.client.get(reverse('hello'))
        self.assertEqual(response.status_code, 200)