from django.test import TestCase
from django.urls import reverse_lazy
from datetime import date

# Create your tests here.
class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse_lazy('CreateAccountPage')
        self.user = {
            'username' : 'testusername',
            'email' : 'testemail@gmail.com',
            'password' : 'samplePassword123',
            'firstname' : 'testfname',
            'lastname' : 'testlname',
            'phone_number' : '09563626568',
            'birthdate' : date(1999,8,8), 
            'blood_type' : 'A+',
            'height' : 150.75,
            'weight' : 78,
            'is_admin' : False,
            'is_active' : True,
            'is_staff' : False,
            'is_superuser' : False,
            'date_created' : date.today()
        }
        return super().setUp()

class RegistrationTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'createAccountPage.html')
    
    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 200)