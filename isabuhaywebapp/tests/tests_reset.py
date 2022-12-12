from django.test import TestCase
from django.urls import reverse_lazy

# Create your tests here.
class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse_lazy('reset_password')
        self.user = {
            'email' : 'testemail@gmail.com'
        }

        return super().setUp()

class ResetTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resetPassword.html')
    
    def test_can_login_user(self):
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 302)