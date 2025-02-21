from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

User = get_user_model()
registration_url = reverse('accounts:register')
login_url = reverse('accounts:login')
user_creation_data = {
    'username': 'testuser',
    'email': 'labalette.antoine@gmail.com',
    'first_name': 'Antoine',
    'last_name': 'Labalette',
    'password': '#TestPassword123'
}

class RegistrationTest(APITestCase):

    def test_registration(self):
        response = self.client.post(registration_url, user_creation_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.filter(username='testuser')
        self.assertTrue(user.exists())
        user_instance = user.first()

        for field_name, value in user_creation_data.items():
            if field_name != "password":
                self.assertEqual(getattr(user_instance, field_name), value)


    def test_user_already_exists(self):
        self.user = User.objects.create_user(**user_creation_data)
        response = self.client.post(registration_url, user_creation_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



    def test_password_too_simple(self):
        wrong_data = user_creation_data.copy()
        wrong_data['password'] = "Anton"
        response = self.client.post(registration_url, wrong_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_invalid(self):
        wrong_data = user_creation_data.copy()
        wrong_data['email'] = "Anton"
        response = self.client.post(registration_url, wrong_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class LoginTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(**user_creation_data)
    
    def test_login(self):

        data = {
            'username': 'testuser',
            'password': '#TestPassword123'
        }
        response = self.client.post(login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Le test attend la présence d'un token dans la réponse
        self.assertIn('token', response.data)

    def test_wrong_login(self):

        data = {
            'username': 'testuser',
            'password': 'TestPassword123'
        }
        response = self.client.post(login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)