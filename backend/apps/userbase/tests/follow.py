from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from organization.models import Organization
from datetime import date

User = get_user_model()


class FollowSystemTest(APITestCase):
    """Test Follow/Unfollow functionality"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com",
            first_name="Test",
            last_name="User"
        )
        self.client.force_authenticate(user=self.user)

        # Create test organizations
        self.org1 = Organization.objects.create(
            name="Organization One",
            org_type=Organization.OrgType.HOLDING,
            nation="US",
            founding_date=date(2000, 1, 1),
            headcount=1000
        )
        self.org2 = Organization.objects.create(
            name="Organization Two",
            org_type=Organization.OrgType.SME,
            nation="TR",
            founding_date=date(2020, 1, 1),
            headcount=50
        )

    def test_follow_organization(self):
        """Test following an organization"""
        url = f'/api/userbase/follow/{self.org1.slug}/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Followed', response.data['detail'])

        # Verify organization is in user's followed list
        self.assertTrue(self.user.followed_organizations.filter(id=self.org1.id).exists())

    def test_follow_nonexistent_organization(self):
        """Test following a non-existent organization"""
        url = '/api/userbase/follow/nonexistent-org/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_follow_already_followed_organization(self):
        """Test following an organization that is already followed"""
        # First follow
        self.user.followed_organizations.add(self.org1)

        # Try to follow again
        url = f'/api/userbase/follow/{self.org1.slug}/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already following', response.data['detail'])

    def test_unfollow_organization(self):
        """Test unfollowing an organization"""
        # First follow the organization
        self.user.followed_organizations.add(self.org1)

        # Now unfollow
        url = f'/api/userbase/unfollow/{self.org1.slug}/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Unfollowed', response.data['detail'])

        # Verify organization is not in user's followed list
        self.assertFalse(self.user.followed_organizations.filter(id=self.org1.id).exists())

    def test_unfollow_not_followed_organization(self):
        """Test unfollowing an organization that is not followed"""
        url = f'/api/userbase/unfollow/{self.org1.slug}/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('not following', response.data['detail'])

    def test_list_followed_organizations(self):
        """Test listing followed organizations"""
        # Follow both organizations
        self.user.followed_organizations.add(self.org1, self.org2)

        url = '/api/userbase/followed-organizations/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

    def test_list_followed_organizations_empty(self):
        """Test listing followed organizations when none are followed"""
        url = '/api/userbase/followed-organizations/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)

    def test_follow_requires_authentication(self):
        """Test that following requires authentication"""
        self.client.force_authenticate(user=None)
        url = f'/api/userbase/follow/{self.org1.slug}/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unfollow_requires_authentication(self):
        """Test that unfollowing requires authentication"""
        self.client.force_authenticate(user=None)
        url = f'/api/userbase/unfollow/{self.org1.slug}/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_followed_requires_authentication(self):
        """Test that listing followed organizations requires authentication"""
        self.client.force_authenticate(user=None)
        url = '/api/userbase/followed-organizations/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_multiple_users_follow_same_organization(self):
        """Test that multiple users can follow the same organization"""
        user2 = User.objects.create_user(
            username="testuser2",
            password="testpass123"
        )

        # User1 follows
        self.user.followed_organizations.add(self.org1)

        # User2 follows
        user2.followed_organizations.add(self.org1)

        # Verify both users follow the organization
        self.assertTrue(self.user.followed_organizations.filter(id=self.org1.id).exists())
        self.assertTrue(user2.followed_organizations.filter(id=self.org1.id).exists())

        # Verify organization has 2 followers
        self.assertEqual(self.org1.followers.count(), 2)


class UserModelFollowTest(TestCase):
    """Test User model's follow relationship"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.org = Organization.objects.create(
            name="Test Org",
            org_type=Organization.OrgType.SME,
            nation="TR",
            founding_date=date(2020, 1, 1)
        )

    def test_user_followed_organizations_relationship(self):
        """Test ManyToMany relationship between User and Organization"""
        # Initially no follows
        self.assertEqual(self.user.followed_organizations.count(), 0)

        # Add follow
        self.user.followed_organizations.add(self.org)
        self.assertEqual(self.user.followed_organizations.count(), 1)

        # Remove follow
        self.user.followed_organizations.remove(self.org)
        self.assertEqual(self.user.followed_organizations.count(), 0)

    def test_organization_followers_reverse_relationship(self):
        """Test reverse relationship from Organization to Users"""
        # Create multiple users
        user2 = User.objects.create_user(username="user2", password="pass")
        user3 = User.objects.create_user(username="user3", password="pass")

        # All follow the organization
        self.user.followed_organizations.add(self.org)
        user2.followed_organizations.add(self.org)
        user3.followed_organizations.add(self.org)

        # Check followers count from organization side
        self.assertEqual(self.org.followers.count(), 3)
        self.assertIn(self.user, self.org.followers.all())
        self.assertIn(user2, self.org.followers.all())
        self.assertIn(user3, self.org.followers.all())
