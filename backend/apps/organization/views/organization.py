from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from organization.models import Organization
from organization.serializers import OrganizationSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from datetime import datetime


@method_decorator(csrf_exempt, name='dispatch')
class OrganizationViewSet(viewsets.ModelViewSet):
    """CRUD for Organization with advanced filtering"""

    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"  # detail page with slug

    def get_queryset(self):
        """
        Filter organizations based on query parameters

        Supported filters:
        - name: Organization name (contains, case-insensitive)
        - org_type: Organization type(s) - comma separated for multiple
        - country: Country code (e.g., 'TR', 'US')
        - founding_date_from: Start date (YYYY-MM-DD)
        - founding_date_to: End date (YYYY-MM-DD)
        - headcount_min: Minimum employee count
        - headcount_max: Maximum employee count

        Example: /api/organizations/?country=TR&org_type=2,3&headcount_max=10
        """
        queryset = Organization.objects.all()

        # Name filtering (case-insensitive contains)
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)

        # Organization type filtering (supports multiple types)
        org_types = self.request.query_params.get('org_type')
        if org_types:
            # Handle comma-separated values: "2,3" -> [2, 3]
            type_list = [int(t.strip()) for t in org_types.split(',') if t.strip().isdigit()]
            if type_list:
                queryset = queryset.filter(org_type__in=type_list)

        # Country filtering
        country = self.request.query_params.get('country')
        if country:
            queryset = queryset.filter(nation=country.upper())

        # Founding date range filtering
        date_from = self.request.query_params.get('founding_date_from')
        date_to = self.request.query_params.get('founding_date_to')

        if date_from:
            try:
                start_date = datetime.strptime(date_from, '%Y-%m-%d').date()
                queryset = queryset.filter(founding_date__gte=start_date)
            except ValueError:
                pass  # Invalid date format, ignore filter

        if date_to:
            try:
                end_date = datetime.strptime(date_to, '%Y-%m-%d').date()
                queryset = queryset.filter(founding_date__lte=end_date)
            except ValueError:
                pass  # Invalid date format, ignore filter

        # Employee count range filtering
        headcount_min = self.request.query_params.get('headcount_min')
        headcount_max = self.request.query_params.get('headcount_max')

        if headcount_min:
            try:
                min_count = int(headcount_min)
                queryset = queryset.filter(headcount__gte=min_count)
            except ValueError:
                pass  # Invalid number, ignore filter

        if headcount_max:
            try:
                max_count = int(headcount_max)
                queryset = queryset.filter(headcount__lte=max_count)
            except ValueError:
                pass  # Invalid number, ignore filter

        # Handle None values in headcount filtering
        # If filtering by headcount, exclude organizations with no headcount data
        if headcount_min or headcount_max:
            queryset = queryset.filter(headcount__isnull=False)

        return queryset.order_by('name')
