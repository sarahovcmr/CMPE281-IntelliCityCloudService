from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Device  # Make sure to import the model if you want to test


class AddDeviceAPITest(APITestCase):
    def test_add_device(self):
        url = reverse('add_device')  # make sure 'add_device' is the name of the url
        data = {'station_id': 400000}  # Provide valid station id here

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_device_already_exists(self):
        url = reverse('add_device')  # make sure 'add_device' is the name of the url
        data = {'station_id': 400000}  # Provide a station id that already exists

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
