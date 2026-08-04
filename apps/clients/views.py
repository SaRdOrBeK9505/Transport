from rest_framework import viewsets, filters
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny

from apps.common.permissions import IsAdminUser
from apps.common.pagination import StandardPagination
from .models import PartnerClient
from .serializers import PartnerClientSerializer, AdminPartnerClientSerializer


# ══════════════════════════════════════════════════════════════════════════════
#  PUBLIC
# ══════════════════════════════════════════════════════════════════════════════

class PartnerClientViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /clients/list/"""
    queryset = PartnerClient.objects.filter(is_active=True).order_by('order')
    serializer_class = PartnerClientSerializer
    permission_classes = [AllowAny]


# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN
# ══════════════════════════════════════════════════════════════════════════════

class AdminPartnerClientViewSet(viewsets.ModelViewSet):
    """
    Admin: Hamkorlar to'liq CRUD.

    GET    /clients/admin/list/           — barchasi (is_active=False ham)
    POST   /clients/admin/list/           — yangi hamkor + logo yuklash
    GET    /clients/admin/list/{id}/      — detail
    PUT    /clients/admin/list/{id}/      — to'liq yangilash
    PATCH  /clients/admin/list/{id}/      — qisman (masalan faqat order yoki is_active)
    DELETE /clients/admin/list/{id}/      — o'chirish
    """
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # logo yuklash uchun
    serializer_class = AdminPartnerClientSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'website']
    ordering_fields = ['order', 'name', 'created_at']

    def get_queryset(self):
        # Admin is_active=False ni ham ko'radi
        return PartnerClient.objects.order_by('order')
