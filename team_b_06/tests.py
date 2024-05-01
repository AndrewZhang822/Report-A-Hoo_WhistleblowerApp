from django.test import TestCase, Client, RequestFactory;

# Create your tests here.
from team_b_06.models import UserProfile;
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .views import profile, home, signup, signin


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.username = "test"
        self.password = "password123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.c = Client()

    def test_user_profile_creation(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(UserProfile.objects.count(), 1)

        user_profile = self.user.profile

        self.assertEqual(user_profile.role, 'Student')
        self.assertFalse(user_profile.site_admin)

    def test_user_login(self):
        logged_in = self.c.login(username='test', password='password123')
        self.assertTrue(logged_in)
    
    def tearDown(self):
        self.user.delete()

class ViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='password')

    def test_view_home(self):
        request = self.factory.get('/')
        response = home(request)
        self.assertEqual(response.status_code, 200)
    
    def test_profile_view_authenticated(self):
        user = User.objects.create_user(username='testuser', password='password123')
        request = self.factory.get('/profile/')
        request.user = user
        response = profile(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Student")