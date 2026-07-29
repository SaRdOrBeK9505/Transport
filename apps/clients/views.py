from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny

from apps.common.permissions import IsAdminUser
from apps.common.pagination import StandardPagination
from .models import PartnerClient
from .serializers import PartnerClientSerializer, AdminPartnerClientSerializer


# ══════════════════════════════════════════════════════════════════════════════
#  PUBLIC
# ══════════════════════════════════════════════════════════════════════════════

class PartnerClientViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/v1/clients/"""
    queryset = PartnerClient.objects.filter(is_active=True).order_by('order')
    serializer_class = PartnerClientSerializer
    permission_classes = [AllowAny]


# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN
# ══════════════════════════════════════════════════════════════════════════════

class AdminPartnerClientViewSet(viewsets.ModelViewSet):
    """
    Admin: Hamkorlar to'liq CRUD.

    GET    /api/v1/admin/clients/           — barchasi (is_active=False ham)
    POST   /api/v1/admin/clients/           — yangi hamkor + logo yuklash
    GET    /api/v1/admin/clients/{id}/      — detail
    PUT    /api/v1/admin/clients/{id}/      — to'liq yangilash
    PATCH  /api/v1/admin/clients/{id}/      — qisman (masalan faqat order yoki is_active)
    DELETE /api/v1/admin/clients/{id}/      — o'chirish
    """
    permission_classes = [IsAdminUser]
    serializer_class = AdminPartnerClientSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'website']
    ordering_fields = ['order', 'name', 'created_at']

    def get_queryset(self):
        # Admin is_active=False ni ham ko'radi
        return PartnerClient.objects.order_by('order')
