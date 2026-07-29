from rest_framework import serializers
from .models import Order


# ══════════════════════════════════════════════════════════════════════════════
#  PUBLIC
# ══════════════════════════════════════════════════════════════════════════════

class OrderCreateSerializer(serializers.ModelSerializer):
    """Frontend forma: car.html va contacts.html dan ariza."""
    class Meta:
        model = Order
        fields = (
            'full_name', 'phone',
            'route_from', 'route_to',
            'date_start', 'date_end',
            'vehicle', 'service',
            'comment',
        )

    def validate(self, data):
        d1, d2 = data.get('date_start'), data.get('date_end')
        if d1 and d2 and d2 < d1:
            raise serializers.ValidationError(
                {'date_end': 'Tugash sanasi boshlanish sanasidan oldin bo\'lishi mumkin emas.'}
            )
        return data


# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN
# ══════════════════════════════════════════════════════════════════════════════

class AdminOrderListSerializer(serializers.ModelSerializer):
    """Admin ro'yxat uchun — qisqa."""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    vehicle_name = serializers.SerializerMethodField()
    service_title = serializers.CharField(source='service.title', read_only=True, default='')
    rental_days = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'full_name', 'phone',
            'route_from', 'route_to',
            'date_start', 'date_end', 'rental_days',
            'vehicle', 'vehicle_name',
            'service', 'service_title',
            'status', 'status_display',
            'comment', 'created_at', 'updated_at',
        )

    def get_vehicle_name(self, obj) -> str:
        if obj.vehicle:
            brand = f'{obj.vehicle.brand} ' if obj.vehicle.brand else ''
            return f'{brand}{obj.vehicle.name}'
        return ''


class AdminOrderDetailSerializer(serializers.ModelSerializer):
    """Admin detail va yangilash uchun — barcha maydonlar."""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    rental_days = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'full_name', 'phone',
            'route_from', 'route_to',
            'date_start', 'date_end', 'rental_days',
            'vehicle', 'service',
            'comment',
            'status', 'status_display',
            'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'rental_days', 'status_display')
