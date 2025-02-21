from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

User = get_user_model()

class RegistrationTest(APITestCase):
    def test_registration(self):
        url = reverse('accounts:register')
        data = {
            'username': 'testuser',
            'password': 'TestPassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Vérifier que l'utilisateur a bien été créé
        self.assertTrue(User.objects.filter(username='testuser').exists())



class LoginTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='TestPassword123')
    
    def test_login(self):
        url = reverse('accounts:login')
        data = {
            'username': 'testuser',
            'password': 'TestPassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Le test attend la présence d'un token dans la réponse
        self.assertIn('token', response.data)