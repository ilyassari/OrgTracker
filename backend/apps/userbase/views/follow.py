from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from organization.models import Organization
from userbase.serializers import FollowedOrganizationSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class FollowOrganizationView(APIView):
    """Add organization to user's followed list"""
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        user = request.user
        org = get_object_or_404(Organization, slug=slug)
        # Check if already following
        if user.followed_organizations.filter(slug=slug).exists():
            return Response(
                {"detail": f"You are already following {org.name}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.followed_organizations.add(org)
        return Response({"detail": f"Followed {org.name}"}, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class UnfollowOrganizationView(APIView):
    """Remove organization from user's followed list"""
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        user = request.user
        org = get_object_or_404(Organization, slug=slug)
        # Check if not following
        if not user.followed_organizations.filter(slug=slug).exists():
            return Response(
                {"detail": f"You are not following {org.name}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.followed_organizations.remove(org)
        return Response({"detail": f"Unfollowed {org.name}"}, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class FollowedOrganizationsListView(APIView):
    """List all organizations followed by the user"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        followed_orgs = user.followed_organizations.all()
        serializer = FollowedOrganizationSerializer(followed_orgs, many=True)
        return Response({
            "count": followed_orgs.count(),
            "results": serializer.data
        })
