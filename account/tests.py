from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from django.core.urlresolvers import reverse
from rest_framework import status


factory = APIRequestFactory()
request = factory.post('/account/signup/',
                       {
                           'email': 'aryankeshri1111@gmail.com',
                           'password': 'Ary@n_1111',
                           'full_name': 'Aryan Keshri',
                           'role': 1
                       },
                       format='json'
                       )


print(request)


class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def test_api_can_create_a_user1(self):
        """Test the api has bucket creation capability."""
        self.client = APIClient()
        self.user_data = {
                           'email': 'aryankeshri1111@gmail.com',
                           'password': 'Ary@n_1111',
                           'full_name': 'Aryan Keshri',
                           'role': 1
        }
        self.response = self.client.post(
            reverse('registration'),
            self.user_data,
            format='json')

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_create_a_user2(self):
        """Test the api has bucket creation capability."""
        self.client = APIClient()
        self.user_data = {
                           'email': 'aryankeshri1111@gmail.com',
                           'password': '',
                           'full_name': 'Aryan Keshri',
                           'role': 1
        }
        self.response = self.client.post(
            reverse('registration'),
            self.user_data,
            format='json')

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_create_a_user3(self):
        """Test the api has bucket creation capability."""
        self.client = APIClient()
        self.user_data = {
                           'email': 'aryankeshri1111@gmail.com',
                           'password': 'Ary@n_1111',
                           'full_name': '',
                           'role': 1
        }
        self.response = self.client.post(
            reverse('registration'),
            self.user_data,
            format='json')

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
