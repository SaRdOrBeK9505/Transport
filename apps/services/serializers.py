from rest_framework import serializers
from apps.fleet.serializers import VehicleListSerializer
from .models import ServiceDirection, ServiceFeature


# ══════════════════════════════════════════════════════════════════════════════
#  PUBLIC serializers
# ══════════════════════════════════════════════════════════════════════════════

class ServiceFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceFeature
        fields = ('id', 'title', 'description', 'icon', 'order')


class ServiceDirectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceDirection
        fields = ('id', 'title', 'slug', 'short_description', 'icon', 'image', 'order')


class ServiceDirectionDetailSerializer(serializers.ModelSerializer):
    what_is_included_list = serializers.ListField(child=serializers.CharField(), read_only=True)
    suitable_vehicles = VehicleListSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceDirection
        fields = (
            'id', 'title', 'slug', 'short_description',
            'description', 'icon', 'image', 'order',
            'what_is_included', 'what_is_included_list',
            'suitable_vehicles',
            'created_at', 'updated_at',
        )


# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN serializers
# ══════════════════════════════════════════════════════════════════════════════

class AdminServiceFeatureSerializer(serializers.ModelSerializer):
    """ServiceFeature to'liq CRUD."""
    class Meta:
        model = ServiceFeature
        fields = ('id', 'title', 'description', 'icon', 'order', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class AdminServiceDirectionWriteSerializer(serializers.ModelSerializer):
    """
    ServiceDirection yaratish va yangilash.
    suitable_vehicles — ID lar ro'yxati bilan yuboriladi: [1, 3, 5]

    Lazy queryset: module darajasida import qilmaslik uchun
    get_fields() ichida Vehicle import qilinadi.
    """
    suitable_vehicles_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        help_text='Vehicle ID lar ro\'yxati: [1, 3, 5]'
    )

    class Meta:
        model = ServiceDirection
        fields = (
            'id', 'title', 'slug',
            'short_description', 'description',
            'icon', 'image', 'order',
            'what_is_included',
            'suitable_vehicles_ids',
            'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
        extra_kwargs = {'slug': {'required': False}}

    def _set_suitable_vehicles(self, instance, ids):
        from apps.fleet.models import Vehicle
        if ids is not None:
            vehicles = Vehicle.objects.filter(id__in=ids)
            instance.suitable_vehicles.set(vehicles)

    def create(self, validated_data):
        ids = validated_data.pop('suitable_vehicles_ids', None)
        instance = super().create(validated_data)
        self._set_suitable_vehicles(instance, ids)
        return instance

    def update(self, instance, validated_data):
        ids = validated_data.pop('suitable_vehicles_ids', None)
        instance = super().update(instance, validated_data)
        self._set_suitable_vehicles(instance, ids)
        return instance


class AdminServiceDirectionReadSerializer(serializers.ModelSerializer):
    """ServiceDirection ro'yxat va detail — admin uchun."""
    what_is_included_list = serializers.ListField(child=serializers.CharField(), read_only=True)
    suitable_vehicles = VehicleListSerializer(many=True, read_only=True)
    suitable_vehicles_ids = serializers.SerializerMethodField()

    class Meta:
        model = ServiceDirection
        fields = (
            'id', 'title', 'slug',
            'short_description', 'description',
            'icon', 'image', 'order',
            'what_is_included', 'what_is_included_list',
            'suitable_vehicles', 'suitable_vehicles_ids',
            'created_at', 'updated_at',
        )

    def get_suitable_vehicles_ids(self, obj) -> list:
        return list(obj.suitable_vehicles.values_list('id', flat=True))
