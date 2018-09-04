from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class DevOpsTests(APITestCase):
    def test_initial(self):
        """
        Test default use cases
        """
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
