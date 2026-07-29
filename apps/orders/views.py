from rest_framework import viewsets, generics, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apps.common.pagination import StandardPagination
from apps.common.permissions import IsDispatcherOrAdmin
from .models import Order
from .serializers import (
    OrderCreateSerializer,
    AdminOrderListSerializer,
    AdminOrderDetailSerializer,
)


# ══════════════════════════════════════════════════════════════════════════════
#  PUBLIC
# ══════════════════════════════════════════════════════════════════════════════

class OrderCreateView(generics.CreateAPIView):
    """
    POST /api/v1/orders/
    Frontend formasi — ariza qoldirish (token kerak emas).
    """
    serializer_class = OrderCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'detail': "Arizangiz qabul qilindi. Tez orada siz bilan bog'lanamiz."},
            status=status.HTTP_201_CREATED
        )


# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN
# ══════════════════════════════════════════════════════════════════════════════

class AdminOrderViewSet(viewsets.ModelViewSet):
    """
    Admin/dispatcher: Arizalar to'liq boshqaruv.

    GET    /api/v1/admin/orders/                — ro'yxat (filtrlash bilan)
    POST   /api/v1/admin/orders/                — admin o'zi ariza yaratishi
    GET    /api/v1/admin/orders/{id}/           — detail
    PUT    /api/v1/admin/orders/{id}/           — to'liq yangilash
    PATCH  /api/v1/admin/orders/{id}/           — qisman yangilash (status o'zgartirish)
    DELETE /api/v1/admin/orders/{id}/           — o'chirish

    Filtrlash:
      ?status=new|processing|done|cancelled
      ?search=ism_yoki_telefon
      ?ordering=-created_at

    Tezkor status o'zgartirish:
    PATCH /api/v1/admin/orders/{id}/set_status/  {"status": "done"}
    """
    permission_classes = [IsDispatcherOrAdmin]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'vehicle', 'service']
    search_fields = ['full_name', 'phone', 'route_from', 'route_to', 'comment']
    ordering_fields = ['created_at', 'date_start', 'status']

    def get_queryset(self):
        return (
            Order.objects
            .select_related('vehicle', 'vehicle__category', 'service')
            .order_by('-created_at')
        )

    def get_serializer_class(self):
        # Ro'yxat uchun qisqa, detail/update uchun to'liq
        if self.action == 'list':
            return AdminOrderListSerializer
        return AdminOrderDetailSerializer

    @action(detail=True, methods=['patch'], url_path='set_status')
    def set_status(self, request, pk=None):
        """
        PATCH /api/v1/admin/orders/{id}/set_status/
        Body: {"status": "processing"}
        Tezkor holat o'zgartirish — faqat status maydoni.
        """
        order = self.get_object()
        new_status = request.data.get('status')
        valid = [c[0] for c in Order.STATUS_CHOICES]
        if new_status not in valid:
            return Response(
                {'detail': f"Noto'g'ri holat. Ruxsat etilganlar: {valid}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.status = new_status
        order.save(update_fields=['status'])
        return Response({
            'id': order.id,
            'status': order.status,
            'status_display': order.get_status_display(),
        })
