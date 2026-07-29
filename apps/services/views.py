from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from apps.common.permissions import IsAdminUser
from apps.common.pagination import StandardPagination
from .models import ServiceDirection, ServiceFeature
from .serializers import (
    ServiceDirectionListSerializer,
    ServiceDirectionDetailSerializer,
    ServiceFeatureSerializer,
    AdminServiceFeatureSerializer,
    AdminServiceDirectionWriteSerializer,
    AdminServiceDirectionReadSerializer,
)


# ══════════════════════════════════════════════════════════════════════════════
#  PUBLIC
# ══════════════════════════════════════════════════════════════════════════════

class ServiceDirectionViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/v1/services/  &  /{slug}/"""
    queryset = (
        ServiceDirection.objects
        .prefetch_related('suitable_vehicles__images', 'suitable_vehicles__category')
        .order_by('order')
    )
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ServiceDirectionDetailSerializer
        return ServiceDirectionListSerializer


class ServiceFeatureViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/v1/services/features/"""
    queryset = ServiceFeature.objects.order_by('order')
    serializer_class = ServiceFeatureSerializer
    permission_classes = [AllowAny]


# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN
# ══════════════════════════════════════════════════════════════════════════════

class AdminServiceDirectionViewSet(viewsets.ModelViewSet):
    """
    Admin: Xizmat yo'nalishlari to'liq CRUD.

    GET    /api/v1/admin/services/              — ro'yxat
    POST   /api/v1/admin/services/              — yaratish
    GET    /api/v1/admin/services/{id}/         — detail
    PUT    /api/v1/admin/services/{id}/         — to'liq yangilash
    PATCH  /api/v1/admin/services/{id}/         — qisman yangilash
    DELETE /api/v1/admin/services/{id}/         — o'chirish

    suitable_vehicles ni yangilash:
    PATCH /api/v1/admin/services/{id}/  {"suitable_vehicles": [1, 3, 5]}
    """
    permission_classes = [IsAdminUser]
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'short_description', 'description']
    ordering_fields = ['order', 'title', 'created_at']

    def get_queryset(self):
        return (
            ServiceDirection.objects
            .prefetch_related('suitable_vehicles__images', 'suitable_vehicles__category')
            .order_by('order')
        )

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return AdminServiceDirectionWriteSerializer
        return AdminServiceDirectionReadSerializer


class AdminServiceFeatureViewSet(viewsets.ModelViewSet):
    """
    Admin: Xizmat afzalliklari to'liq CRUD.

    GET    /api/v1/admin/services/features/         — ro'yxat
    POST   /api/v1/admin/services/features/         — yaratish
    GET    /api/v1/admin/services/features/{id}/    — detail
    PUT    /api/v1/admin/services/features/{id}/    — to'liq yangilash
    PATCH  /api/v1/admin/services/features/{id}/    — qisman yangilash
    DELETE /api/v1/admin/services/features/{id}/    — o'chirish
    """
    permission_classes = [IsAdminUser]
    queryset = ServiceFeature.objects.order_by('order')
    serializer_class = AdminServiceFeatureSerializer
