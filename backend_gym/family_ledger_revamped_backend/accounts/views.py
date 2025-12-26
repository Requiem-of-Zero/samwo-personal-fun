from rest_framework import generics, permissions
from rest_framework import response

from .serializers import RegisterSerializer, MeSerializer
# Create your views here.

class RegisterView(generics.CreateAPIView):
    """
    POST /api/v1/auth/register/
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class MeView(generics.CreateAPIView):
    """
    POST /api/v1/auth/me/
    """
    serializer_class = MeSerializer

    def get_current_user_obj(self):
        return self.request.user # Returns current authenticated user || null