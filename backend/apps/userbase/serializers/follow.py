from rest_framework import serializers
from organization.models import Organization


class FollowedOrganizationSerializer(serializers.ModelSerializer):
    """Serializer for followed organizations"""

    class Meta:
        model = Organization
        fields = ["id", "name", "slug", "logo", "org_type", "nation", "founding_date", "headcount"]
