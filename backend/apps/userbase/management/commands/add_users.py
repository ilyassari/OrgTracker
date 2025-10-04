import os
import json

from django.core.management.base import BaseCommand
from django.conf import settings

from userbase.models import User


class Command(BaseCommand):
    """
    Custom Django management command to create users by list.

    Usage:
        python manage.py add_users
    """

    def handle(self, *args, **options):
        """
        This method is called when the management command is run.
        """

        # Open the file which info is stored
        with open("sample_data/users.json", 'r') as file:
            data = json.load(file)

        # Iterate info list to create instances
        for item in data:
            user = User()
            user.username = item["username"]
            user.email = item["email"]
            user.set_password(item["password"])
            user.save()
            user.first_name = item["first_name"]
            user.last_name = item["last_name"]
            user.is_staff = item["is_staff"]
            user.is_superuser = item["is_superuser"]
            user.save()
        print("Info:", "Users are created.")