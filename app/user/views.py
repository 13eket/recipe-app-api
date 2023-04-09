"""
Views for the user API.
"""
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from user.serializers import UserSerializer, AuthTokenSerializer

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """Create a new token using user email and password"""
    serializer_class = AuthTokenSerializer
    #renderer_class = Something that I will customise in the future