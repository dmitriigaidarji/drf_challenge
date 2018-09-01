from random import randint

from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from devops.views import DevOpsEngineers


class DevOpsTests(APITestCase):
    def test_initial(self):
        url = reverse('devops')
        data = {
            "DM_capacity": "20",
            "DE_capacity": "8",
            "data_centers": [
                {
                    "name": "Paris",
                    "servers": "20"
                },
                {
                    "name": "Stockholm",
                    "servers": "62"
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['DE'], 8)
        self.assertEqual(response.data['DM_data_center'], 'Paris')

        data = {
            "DM_capacity": "6",
            "DE_capacity": "10",
            "data_centers": [
                {
                    "name": "Paris",
                    "servers": "30"
                },
                {
                    "name": "Stockholm",
                    "servers": "66"
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['DE'], 9)
        self.assertEqual(response.data['DM_data_center'], 'Stockholm')

        data = {
            "DM_capacity": "12",
            "DE_capacity": "7",
            "data_centers": [
                {
                    "name": "Berlin",
                    "servers": "11"
                },
                {
                    "name": "Stockholm",
                    "servers": "21"
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['DE'], 3)
        self.assertEqual(response.data['DM_data_center'], 'Berlin')

    def test_correctness(self):
        url = reverse('devops')

        for i in range(0, 1000):
            data = {
                "DM_capacity": randint(1, 20),
                "DE_capacity": randint(1, 20),
                "data_centers": [
                ]
            }
            for i in range(0, randint(1, 20)):
                data['data_centers'].append({
                    "name": "Dummy",
                    "servers": randint(1, 300)
                })
            response = self.client.post(url, data, format='json')
            instance = DevOpsEngineers()
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(
                response.data['DE'],
                instance.full_search(instance, data['DM_capacity'], data['DE_capacity'], data['data_centers'])['DE']
            )
