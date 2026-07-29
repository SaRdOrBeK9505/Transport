from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import UserMeSerializer


class MeView(generics.RetrieveUpdateAPIView):
    """Joriy autentifikatsiyalangan foydalanuvchi ma'lumotlari."""
    serializer_class = UserMeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
