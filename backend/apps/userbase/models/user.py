from django.contrib.auth.models import AbstractUser
from django.db import models
from organization.models import Organization


class User(AbstractUser):
    """
    Custom User model.
    """
    followed_organizations = models.ManyToManyField(
        Organization,
        blank=True,
        related_name="followers"
    )

    def __str__(self):
        return self.username
