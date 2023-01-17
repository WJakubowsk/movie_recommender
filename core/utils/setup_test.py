from django.test import TestCase
from authentication.models import User
from faker import Faker


class TestSetup(TestCase):

    def setUp(self):
        self.faker = Faker()
        self.password = self.faker.paragraph(nb_sentences=5)

        self.user = {
            "username": self.faker.name().split(" ")[0],
            "email": self.faker.email(),
            "first_name": self.faker.name().split(" ")[0],
            "last_name": self.faker.name().split(" ")[0],
            "password": self.password,
            "password2": self.password
        }

    def create_test_user(self):
        user = User.objects.create_user(
            username='user', email='user@app.com',
            password='password12!', first_name='user',
            last_name='user')
        user.set_password('password12!')
        user.is_email_verified = True
        user.save()
        return user

    def create_test_user_two(self):
        user = User.objects.create_user(
            username='user2', email='user2@app.com',
            password='password12!', first_name='user',
            last_name='user')
        user.set_password('password12!')
        user.save()
        return user

    def tearDown(self):
        return super().tearDown()
