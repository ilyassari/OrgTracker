from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationTest(APITestCase):
    """Test user registration"""

    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/userbase/auth/registration/'
        self.valid_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123456',
            'password2': 'testpass123456',
            'first_name': 'New',
            'last_name': 'User'
        }

    def test_registration_success(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        user = User.objects.get(username='newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.last_name, 'User')

    def test_registration_with_existing_username(self):
        """Test registration with existing username fails"""
        User.objects.create_user(
            username='existinguser',
            password='pass123',
            email='existing@example.com'
        )

        data = self.valid_data.copy()
        data['username'] = 'existinguser'
        data['email'] = 'different@example.com'

        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_registration_with_mismatched_passwords(self):
        """Test registration with mismatched passwords fails"""
        data = self.valid_data.copy()
        data['password2'] = 'differentpass123'

        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_short_password(self):
        """Test registration with too short password fails"""
        data = self.valid_data.copy()
        data['password1'] = 'short'
        data['password2'] = 'short'

        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_registration_without_required_fields(self):
    #     """Test registration without required fields fails"""
    #     # Test without username
    #     data = self.valid_data.copy()
    #     del data['username']
    #     response = self.client.post(self.register_url, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #     # Test without email
    #     # data = self.valid_data.copy()
    #     # del data['email']
    #     # response = self.client.post(self.register_url, data)
    #     # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #     # Test without password
    #     data = self.valid_data.copy()
    #     del data['password1']
    #     response = self.client.post(self.register_url, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTest(APITestCase):
    """Test user login"""

    def setUp(self):
        self.client = APIClient()
        self.login_url = '/api/userbase/auth/login/'
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

    def test_login_success(self):
        """Test successful login"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('key', response.data)  # Token returned

    def test_login_with_wrong_password(self):
        """Test login with wrong password fails"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_nonexistent_user(self):
        """Test login with non-existent user fails"""
        data = {
            'username': 'nonexistent',
            'password': 'somepassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_without_credentials(self):
        """Test login without credentials fails"""
        response = self.client.post(self.login_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserAuthenticationTest(APITestCase):
    """Test authenticated endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )

    def test_access_user_profile_authenticated(self):
        """Test accessing user profile when authenticated"""
        self.client.force_authenticate(user=self.user)
        url = '/api/userbase/auth/user/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_access_user_profile_unauthenticated(self):
        """Test accessing user profile when not authenticated"""
        url = '/api/userbase/auth/user/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        """Test user logout"""
        self.client.force_authenticate(user=self.user)
        url = '/api/userbase/auth/logout/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserModelTest(TestCase):
    """Test User model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )

    def test_user_creation(self):
        """Test user is created successfully"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_user_str_method(self):
        """Test string representation of user"""
        self.assertEqual(str(self.user), 'testuser')

    def test_user_full_name(self):
        """Test user's full name"""
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')

    def test_superuser_creation(self):
        """Test superuser creation"""
        admin = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)

    def test_user_has_followed_organizations_field(self):
        """Test user has followed_organizations field"""
        self.assertTrue(hasattr(self.user, 'followed_organizations'))
        self.assertEqual(self.user.followed_organizations.count(), 0)
