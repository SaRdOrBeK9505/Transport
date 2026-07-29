from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.common.permissions import IsAdminUser
from .models import SiteConfig
from .serializers import SiteConfigSerializer


class SiteConfigPublicView(generics.RetrieveAPIView):
    """
    GET /api/v1/site-settings/
    Barcha sahifalarda ishlatiladigan dinamik ma'lumotlar.
    Token kerak emas.
    """
    serializer_class = SiteConfigSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return SiteConfig.get_solo()


class SiteConfigAdminView(generics.RetrieveUpdateAPIView):
    """
    Admin: Sayt sozlamalarini ko'rish va yangilash.

    GET   /api/v1/admin/site-settings/   — joriy sozlamalar
    PUT   /api/v1/admin/site-settings/   — to'liq yangilash
    PATCH /api/v1/admin/site-settings/   — qisman yangilash
                                           (masalan faqat telefon raqamini)
    JWT token kerak (is_staff=True).
    """
    serializer_class = SiteConfigSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        return SiteConfig.get_solo()
