from django.db.models import Count, Q
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apps.common.pagination import StandardPagination
from apps.common.permissions import IsAdminOrReadOnly, IsAdminUser
from .models import VehicleCategory, Vehicle, VehicleImage
from .serializers import (
    VehicleCategorySerializer,
    VehicleListSerializer,
    VehicleDetailSerializer,
    AdminVehicleCategorySerializer,
    AdminVehicleWriteSerializer,
    AdminVehicleReadSerializer,
    AdminVehicleImageSerializer,
)
from .filters import VehicleFilter


# ══════════════════════════════════════════════════════════════════════════════
#  PUBLIC ViewSets  (frontend)
# ══════════════════════════════════════════════════════════════════════════════

class VehicleCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/v1/fleet/categories/  &  /{slug}/"""
    queryset = VehicleCategory.objects.annotate(
        vehicles_count=Count('vehicles', filter=Q(vehicles__is_active=True))
    ).order_by('order')
    serializer_class = VehicleCategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class VehicleViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/v1/fleet/vehicles/  &  /{slug}/"""
    queryset = (
        Vehicle.objects
        .filter(is_active=True)
        .select_related('category')
        .prefetch_related('images')
    )
    permission_classes = [AllowAny]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = VehicleFilter
    search_fields = ['name', 'brand', 'description', 'category__name']
    ordering_fields = ['seats', 'price_per_day', 'year', 'name']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return VehicleDetailSerializer
        return VehicleListSerializer


# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN ViewSets  (JWT token kerak)
# ══════════════════════════════════════════════════════════════════════════════

class AdminVehicleCategoryViewSet(viewsets.ModelViewSet):
    """
    Admin: Kategoriyalar to'liq CRUD.

    GET    /api/v1/admin/fleet/categories/          — ro'yxat
    POST   /api/v1/admin/fleet/categories/          — yaratish
    GET    /api/v1/admin/fleet/categories/{id}/     — detail
    PUT    /api/v1/admin/fleet/categories/{id}/     — to'liq yangilash
    PATCH  /api/v1/admin/fleet/categories/{id}/     — qisman yangilash
    DELETE /api/v1/admin/fleet/categories/{id}/     — o'chirish
    """
    permission_classes = [IsAdminUser]
    serializer_class = AdminVehicleCategorySerializer

    def get_queryset(self):
        return VehicleCategory.objects.annotate(
            vehicles_count=Count('vehicles', filter=Q(vehicles__is_active=True))
        ).order_by('order')


class AdminVehicleViewSet(viewsets.ModelViewSet):
    """
    Admin: Transport vositalari to'liq CRUD.

    GET    /api/v1/admin/fleet/vehicles/            — barchasi (is_active=False ham)
    POST   /api/v1/admin/fleet/vehicles/            — yangi mashina
    GET    /api/v1/admin/fleet/vehicles/{id}/       — detail
    PUT    /api/v1/admin/fleet/vehicles/{id}/       — to'liq yangilash
    PATCH  /api/v1/admin/fleet/vehicles/{id}/       — qisman yangilash (masalan faqat is_active)
    DELETE /api/v1/admin/fleet/vehicles/{id}/       — o'chirish

    Extra actions:
    PATCH  /api/v1/admin/fleet/vehicles/{id}/toggle_active/  — faol/nofaol almashtirish
    GET    /api/v1/admin/fleet/vehicles/{id}/images/         — mashina rasmlari
    """
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = VehicleFilter
    search_fields = ['name', 'brand', 'description', 'category__name']
    ordering_fields = ['seats', 'price_per_day', 'year', 'name', 'created_at']
    pagination_class = StandardPagination

    def get_queryset(self):
        # Admin barcha mashinalarni ko'radi (is_active=False ham)
        return (
            Vehicle.objects
            .select_related('category')
            .prefetch_related('images')
            .order_by('category__order', 'name')
        )

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return AdminVehicleWriteSerializer
        return AdminVehicleReadSerializer

    def create(self, request, *args, **kwargs):
        write_serializer = AdminVehicleWriteSerializer(
            data=request.data,
            context={'request': request}
        )
        write_serializer.is_valid(raise_exception=True)
        vehicle = write_serializer.save()
        read_serializer = AdminVehicleReadSerializer(
            vehicle,
            context={'request': request}
        )
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        write_serializer = AdminVehicleWriteSerializer(
            instance,
            data=request.data,
            partial=partial,
            context={'request': request}
        )
        write_serializer.is_valid(raise_exception=True)
        vehicle = write_serializer.save()
        read_serializer = AdminVehicleReadSerializer(
            vehicle,
            context={'request': request}
        )
        return Response(read_serializer.data)

    @action(detail=True, methods=['patch'], url_path='toggle_active')
    def toggle_active(self, request, pk=None):
        """PATCH /api/v1/admin/fleet/vehicles/{id}/toggle_active/"""
        vehicle = self.get_object()
        vehicle.is_active = not vehicle.is_active
        vehicle.save(update_fields=['is_active'])
        return Response({
            'id': vehicle.id,
            'is_active': vehicle.is_active,
            'detail': f"{'Faollashtirildi' if vehicle.is_active else 'Nofaol qilindi'}: {vehicle}"
        })

    @action(detail=True, methods=['get'], url_path='images')
    def images(self, request, pk=None):
        """GET /api/v1/admin/fleet/vehicles/{id}/images/"""
        vehicle = self.get_object()
        serializer = AdminVehicleImageSerializer(
            vehicle.images.order_by('order'),
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


class AdminVehicleImageViewSet(viewsets.ModelViewSet):
    """
    Admin: Mashina rasmlari to'liq CRUD.

    GET    /api/v1/admin/fleet/images/              — barcha rasmlar
    POST   /api/v1/admin/fleet/images/              — rasm yuklash (multipart/form-data)
    GET    /api/v1/admin/fleet/images/{id}/         — detail
    PATCH  /api/v1/admin/fleet/images/{id}/         — is_main yoki order o'zgartirish
    DELETE /api/v1/admin/fleet/images/{id}/         — o'chirish
    """
    permission_classes = [IsAdminUser]
    serializer_class = AdminVehicleImageSerializer

    def get_queryset(self):
        qs = VehicleImage.objects.select_related('vehicle').order_by('vehicle', 'order')
        vehicle_id = self.request.query_params.get('vehicle')
        if vehicle_id:
            qs = qs.filter(vehicle_id=vehicle_id)
        return qs
