from django.urls import path, include
from .views import (
    CustomRegisterView,
    FollowOrganizationView,
    UnfollowOrganizationView,
    FollowedOrganizationsListView
)

urlpatterns = [
    # Registration
    path("auth/registration/", CustomRegisterView.as_view(), name="custom_register"),
    # Login/logout etc.
    path("auth/", include("dj_rest_auth.urls")),
    # Follow / Unfollow
    path("follow/<slug:slug>/", FollowOrganizationView.as_view(), name="follow_organization"),
    path("unfollow/<slug:slug>/", UnfollowOrganizationView.as_view(), name="unfollow_organization"),
    path("followed-organizations/", FollowedOrganizationsListView.as_view(), name="followed_organizations"),
]
