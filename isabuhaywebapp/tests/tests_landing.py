from django.test import TestCase
from django.urls import reverse_lazy

# Create your tests here.
class BaseTest(TestCase):
    def setUp(self):
        self.landing_url = reverse_lazy('DisplayLandingPage')
        return super().setUp()

class LandingPageTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.landing_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'displayLandingPage.html')