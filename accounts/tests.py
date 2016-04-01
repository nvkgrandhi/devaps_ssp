from django.core.urlresolvers import reverse
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from .views import login


# Create your tests here.


class UserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='abc123', email='abc@gmail.com', password='pass@123')

    def tearDown(self):
        # del self.a
        pass

    def test_index(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        # self.client.login(username='username1', password='password1')
        # response = self.client.get('/accounts/login/')
        # self.assertEquals(response.status_code, 200)

        request = self.factory.get('/accounts/login/')
        request.user = self.user

        response = login(request)
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please fill the below details to create user')

        response = self.client.post('/accounts/register/', {'first_name': 'fname',
                                                            'last_name': 'lname',
                                                            'username': 'myname',
                                                            'password': 'mypassword',
                                                            'email': 'myname@gmail.com',
                                                            'role': 'developer'})
        self.assertEqual(response.status_code, 200)


