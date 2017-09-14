from django.test import TestCase

# Create your tests here.
from django.test import Client


class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        pass
