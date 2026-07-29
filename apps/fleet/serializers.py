from rest_framework import serializers
from .models import VehicleCategory, Vehicle, VehicleImage


# ══════════════════════════════════════════════════════════════════════════════
#  PUBLIC serializers  (frontend uchun)
# ══════════════════════════════════════════════════════════════════════════════

class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = ('id', 'image', 'is_main', 'order')


class VehicleCategorySerializer(serializers.ModelSerializer):
    vehicles_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = VehicleCategory
        fields = ('id', 'name', 'slug', 'icon', 'order', 'vehicles_count')


class VehicleListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    main_image = serializers.SerializerMethodField()
    display_price = serializers.CharField(read_only=True)

    class Meta:
        model = Vehicle
        fields = (
            'id', 'brand', 'name', 'slug',
            'category_name', 'category_slug',
            'seats', 'year', 'location',
            'price_per_day', 'price_negotiable', 'display_price',
            'has_driver', 'available_today', 'has_ac', 'has_climate_control',
            'fuel_type', 'is_active', 'main_image',
        )

    def get_main_image(self, obj) -> str | None:
        request = self.context.get('request')
        main = obj.images.filter(is_main=True).first() or obj.images.first()
        if main and request:
            return request.build_absolute_uri(main.image.url)
        return None


class VehicleDetailSerializer(serializers.ModelSerializer):
    category = VehicleCategorySerializer(read_only=True)
    images = VehicleImageSerializer(many=True, read_only=True)
    display_price = serializers.CharField(read_only=True)
    suitable_for_list = serializers.ListField(child=serializers.CharField(), read_only=True)
    rental_conditions_list = serializers.ListField(child=serializers.CharField(), read_only=True)

    class Meta:
        model = Vehicle
        fields = (
            'id', 'brand', 'name', 'slug', 'category',
            'seats', 'year', 'location', 'description',
            'price_per_day', 'price_negotiable', 'display_price',
            'min_rental_days', 'discount_from_days',
            'has_driver', 'available_today', 'has_ac', 'has_climate_control',
            'fuel_type', 'transmission', 'color',
            'suitable_for', 'suitable_for_list',
            'rental_conditions', 'rental_conditions_list',
            'delivery_time_minutes',
            'is_active', 'images',
            'created_at', 'updated_at',
        )


# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN serializers  (JWT token kerak)
# ══════════════════════════════════════════════════════════════════════════════

class AdminVehicleImageSerializer(serializers.ModelSerializer):
    """Rasm yuklash va boshqarish."""
    class Meta:
        model = VehicleImage
        fields = ('id', 'vehicle', 'image', 'is_main', 'order')
        read_only_fields = ('id',)


class AdminVehicleCategorySerializer(serializers.ModelSerializer):
    """Kategoriya CRUD."""
    vehicles_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = VehicleCategory
        fields = ('id', 'name', 'slug', 'icon', 'order', 'vehicles_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
        extra_kwargs = {
            'slug': {'required': False},  # save() da avtomatik hosil bo'ladi
        }


class AdminVehicleWriteSerializer(serializers.ModelSerializer):
    """
    Vehicle yaratish va tahrirlash.
    Rasmlar alohida /admin/fleet/images/ endpoint orqali yuklanadi.
    """
    class Meta:
        model = Vehicle
        fields = (
            'id', 'category',
            'brand', 'name', 'slug',
            'seats', 'year', 'location', 'description',
            'price_per_day', 'price_negotiable',
            'min_rental_days', 'discount_from_days', 'delivery_time_minutes',
            'has_driver', 'available_today', 'has_ac', 'has_climate_control',
            'fuel_type', 'transmission', 'color',
            'suitable_for', 'rental_conditions',
            'is_active',
            'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
        extra_kwargs = {
            'slug': {'required': False},
        }


class AdminVehicleReadSerializer(serializers.ModelSerializer):
    """Vehicle ro'yxat va detail — admin uchun (barcha maydonlar, is_active=False ham)."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    images = VehicleImageSerializer(many=True, read_only=True)
    display_price = serializers.CharField(read_only=True)
    suitable_for_list = serializers.ListField(child=serializers.CharField(), read_only=True)
    rental_conditions_list = serializers.ListField(child=serializers.CharField(), read_only=True)

    class Meta:
        model = Vehicle
        fields = (
            'id', 'category', 'category_name',
            'brand', 'name', 'slug',
            'seats', 'year', 'location', 'description',
            'price_per_day', 'price_negotiable', 'display_price',
            'min_rental_days', 'discount_from_days', 'delivery_time_minutes',
            'has_driver', 'available_today', 'has_ac', 'has_climate_control',
            'fuel_type', 'transmission', 'color',
            'suitable_for', 'suitable_for_list',
            'rental_conditions', 'rental_conditions_list',
            'is_active', 'images',
            'created_at', 'updated_at',
        )
