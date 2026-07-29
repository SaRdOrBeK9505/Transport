from rest_framework import serializers
from .models import PartnerClient


# ── Public ────────────────────────────────────────────────────────────────────
class PartnerClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerClient
        fields = ('id', 'name', 'logo', 'website', 'order')


# ── Admin ─────────────────────────────────────────────────────────────────────
class AdminPartnerClientSerializer(serializers.ModelSerializer):
    """Hamkor to'liq CRUD — admin uchun."""
    class Meta:
        model = PartnerClient
        fields = ('id', 'name', 'logo', 'website', 'order', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
