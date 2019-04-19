from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APIClient

from profile.models import UserProfile
from profile.serializer import ProfileSerializer


class TestProfile(TestCase):
    api_client = APIClient()

    @classmethod
    def setUpTestData(cls):
        for i in range(1, 5):
            user = User.objects.create_user(username=f'{i}@mail.com', email=f'{i}@mail.com', password=f'{i}')
            UserProfile.objects.create(user_id=user.id)

    def test_login(self):
        i = 4
        response = self.api_client.post(reverse('login'),
                                        data={'email': f'{i}@mail.com',
                                              'password': f'{i}'},
                                        format='json')
        self.assertEqual(response.status_code, 201)

        new_response = self.api_client.get((reverse('userinfo')))
        self.assertEqual(new_response.status_code, 200)

    def test_wrong_password(self):
        i = 4
        response = self.api_client.post(reverse('login'),
                                        data={'email': f'{i}@mail.com',
                                              'password': f'{i+1}'},
                                        format='json')
        self.assertEqual(response.status_code, 400)

    def test_userinfo(self):
        user = User.objects.first()
        self.api_client.force_authenticate(user)
        response = self.api_client.get(reverse('userinfo'))
        self.assertEqual(response.data, ProfileSerializer(user.userprofile).data)
