
from rest_framework import serializers
from organization.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for Organization model"""

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "slug",
            "logo",
            "org_type",
            "nation",
            "founding_date",
            "headcount",
        ]
