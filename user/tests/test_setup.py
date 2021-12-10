from rest_framework.test import  APITestCase, APIClient
from django.urls import reverse


class TestSetUp(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')

        self.user_data = {
            'email': 'email@gmail.com',
            'username': "email",
            'password': 'email1234'
        }

        return super().setUp()

    def tearDown(self):

        return super().tearDown()

