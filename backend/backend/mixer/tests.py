from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

class AccountTests(APITestCase):
    def test_01_mixer_post(self):
        """
        Test post method for  mixer api.
        Expected output: unique deposit address
        """
        data = {'addresses': ['NS1', 'NS2']}

        response = self.client.post('http://127.0.0.1:8000/api/mixer/address/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('deposit_address' in response.json())


    def test_02_mixer_post_neg(self):
        """
        Test post method for mixer api with no destination address.
        Expected output: 400 Bad request
        """
        data = {'addresses': []}

        response = self.client.post('http://127.0.0.1:8000/api/mixer/address/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_03_mixer_unique_deposit_address(self):
        """
        Test post method for mixer api with no destination address.
        Expected output: unique deposit address
        """
        data = {'addresses': ['KP1', 'KP2', 'KP3']}

        response = self.client.post('http://127.0.0.1:8000/api/mixer/address/', data, format='json')
        deposit_address_kp = response.json()['deposit_address']
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'addresses': ['NP1', 'NP2', 'NP3']}

        response = self.client.post('http://127.0.0.1:8000/api/mixer/address/', data, format='json')
        deposit_address_np = response.json()['deposit_address']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(deposit_address_kp, deposit_address_np)
