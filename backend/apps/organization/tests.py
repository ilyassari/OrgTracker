from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from organization.models import Organization
from datetime import date

User = get_user_model()


class OrganizationModelTest(TestCase):
    """Test Organization model"""

    def setUp(self):
        self.org = Organization.objects.create(
            name="Test Organization",
            org_type=Organization.OrgType.SME,
            nation="TR",
            founding_date=date(2020, 1, 1),
            headcount=50
        )

    def test_organization_creation(self):
        """Test organization is created successfully"""
        self.assertEqual(self.org.name, "Test Organization")
        self.assertEqual(self.org.org_type, Organization.OrgType.SME)
        self.assertEqual(self.org.nation, "TR")
        self.assertEqual(self.org.headcount, 50)

    def test_slug_generation(self):
        """Test slug is auto-generated"""
        self.assertIsNotNone(self.org.slug)
        self.assertEqual(self.org.slug, "test-organization")

    def test_organization_str_method(self):
        """Test string representation"""
        self.assertEqual(str(self.org), "Test Organization")

    def test_get_absolute_url(self):
        """Test get_absolute_url method"""
        url = self.org.get_absolute_url()
        self.assertEqual(url, reverse("organization-detail", kwargs={"slug": self.org.slug}))  # pk yerine slug

    def test_unique_slug(self):
        """Test slug uniqueness"""
        org2 = Organization.objects.create(
            name="Test Organization",
            org_type=Organization.OrgType.HOLDING,
            nation="US",
            founding_date=date(2021, 1, 1)
        )
        self.assertNotEqual(self.org.slug, org2.slug)


class OrganizationAPITest(APITestCase):
    """Test Organization API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com"
        )
        self.client.force_authenticate(user=self.user)

        # Create test organizations
        self.org1 = Organization.objects.create(
            name="Google Inc",
            org_type=Organization.OrgType.HOLDING,
            nation="US",
            founding_date=date(1998, 9, 4),
            headcount=150000
        )
        self.org2 = Organization.objects.create(
            name="Small Tech Company",
            org_type=Organization.OrgType.SME,
            nation="TR",
            founding_date=date(2020, 1, 1),
            headcount=25
        )

    def test_list_organizations(self):
        """Test listing organizations"""
        url = reverse('organization-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_organization(self):
        """Test retrieving a single organization"""
        url = reverse('organization-detail', kwargs={'slug': self.org1.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Google Inc')

    def test_create_organization(self):
        """Test creating a new organization"""
        url = reverse('organization-list')
        data = {
            'name': 'New Organization',
            'org_type': Organization.OrgType.NGO,
            'nation': 'DE',
            'founding_date': '2021-05-15',
            'headcount': 100
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Organization.objects.count(), 3)
        self.assertEqual(response.data['name'], 'New Organization')

    def test_update_organization(self):
        """Test updating an organization"""
        url = reverse('organization-detail', kwargs={'slug': self.org2.slug})
        data = {
            'name': 'Updated Company Name',
            'org_type': Organization.OrgType.SME,
            'nation': 'TR',
            'founding_date': '2020-01-01',
            'headcount': 30
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.org2.refresh_from_db()
        self.assertEqual(self.org2.name, 'Updated Company Name')
        self.assertEqual(self.org2.headcount, 30)

    def test_delete_organization(self):
        """Test deleting an organization"""
        url = reverse('organization-detail', kwargs={'slug': self.org2.slug})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Organization.objects.count(), 1)

    def test_unauthenticated_create(self):
        """Test that unauthenticated users cannot create organizations"""
        self.client.force_authenticate(user=None)
        url = reverse('organization-list')
        data = {
            'name': 'Unauthorized Org',
            'org_type': Organization.OrgType.SME,
            'nation': 'TR',
            'founding_date': '2021-01-01'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrganizationFilterTest(APITestCase):
    """Test Organization filtering functionality"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

        # Create test organizations with different attributes
        Organization.objects.create(
            name="Turkish SME",
            org_type=Organization.OrgType.SME,
            nation="TR",
            founding_date=date(2020, 1, 1),
            headcount=30
        )
        Organization.objects.create(
            name="US Holding",
            org_type=Organization.OrgType.HOLDING,
            nation="US",
            founding_date=date(2000, 1, 1),
            headcount=10000
        )
        Organization.objects.create(
            name="German NGO",
            org_type=Organization.OrgType.NGO,
            nation="DE",
            founding_date=date(2015, 6, 15),
            headcount=50
        )

    def test_filter_by_name(self):
        """Test filtering by name"""
        url = reverse('organization-list')
        response = self.client.get(url, {'name': 'Turkish'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Turkish SME')

    def test_filter_by_country(self):
        """Test filtering by country"""
        url = reverse('organization-list')
        response = self.client.get(url, {'country': 'TR'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_by_org_type(self):
        """Test filtering by organization type"""
        url = reverse('organization-list')
        response = self.client.get(url, {'org_type': f'{Organization.OrgType.SME}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_by_multiple_org_types(self):
        """Test filtering by multiple organization types"""
        url = reverse('organization-list')
        response = self.client.get(url, {'org_type': f'{Organization.OrgType.SME},{Organization.OrgType.NGO}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_by_headcount_range(self):
        """Test filtering by headcount range"""
        url = reverse('organization-list')
        response = self.client.get(url, {'headcount_min': 40, 'headcount_max': 100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'German NGO')

    def test_filter_by_founding_date_range(self):
        """Test filtering by founding date range"""
        url = reverse('organization-list')
        response = self.client.get(url, {
            'founding_date_from': '2015-01-01',
            'founding_date_to': '2020-12-31'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_combined_filters(self):
        """Test multiple filters combined"""
        url = reverse('organization-list')
        response = self.client.get(url, {
            'country': 'TR',
            'org_type': f'{Organization.OrgType.SME}',
            'headcount_max': 50
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Turkish SME')


class OrganizationPermissionTest(APITestCase):
    """Test Organization permissions"""

    def setUp(self):
        self.client = APIClient()
        self.org = Organization.objects.create(
            name="Test Org",
            org_type=Organization.OrgType.SME,
            nation="TR",
            founding_date=date(2020, 1, 1)
        )

    def test_list_without_auth(self):
        """Test that listing works without authentication (IsAuthenticatedOrReadOnly)"""
        url = reverse('organization-list')
        response = self.client.get(url)
        # This should work because of IsAuthenticatedOrReadOnly permission
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_without_auth(self):
        """Test that retrieving works without authentication"""
        url = reverse('organization-detail', kwargs={'slug': self.org.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_without_auth(self):
        """Test that creating requires authentication"""
        url = reverse('organization-list')
        data = {
            'name': 'Unauthorized Org',
            'org_type': Organization.OrgType.SME,
            'nation': 'TR',
            'founding_date': '2021-01-01'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
