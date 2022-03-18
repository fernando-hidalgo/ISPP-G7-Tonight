from typing_extensions import Self
from django.test import TestCase

# Create your tests here.
class ToNightTestCase(TestCase):
    def test_mock():
        Self.assertEquals(1,1)