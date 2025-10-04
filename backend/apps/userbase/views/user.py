from dj_rest_auth.registration.views import RegisterView
from userbase.serializers import CustomRegisterSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class CustomRegisterView(RegisterView):
    """
    Custom registration view using CustomRegisterSerializer
    Handles user registration with first_name and last_name fields
    """
    serializer_class = CustomRegisterSerializer
