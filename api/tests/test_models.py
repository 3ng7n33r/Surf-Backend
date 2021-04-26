from django.test import TestCase

from model_bakery import baker

from api.models import Beach

class ModelBeachTest(TestCase):
    def setUp(self):
        self.beaches = baker.make('Beach', _quantity=4)

    def testThatPasses(self):
        self.assertFalse(False)