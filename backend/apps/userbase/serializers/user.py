from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from userbase.models import User


class CustomRegisterSerializer(RegisterSerializer):
    """
    Custom registration serializer extending dj-rest-auth's RegisterSerializer
    Adds first_name and last_name fields
    """
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def get_cleaned_data(self):
        """
        Returns a dict of validated data for creating the user
        """
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        return data
