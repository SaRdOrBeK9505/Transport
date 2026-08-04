from rest_framework import serializers
from .models import PartnerClient


# ── Public ────────────────────────────────────────────────────────────────────
class PartnerClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerClient
        fields = ('id', 'name', 'logo', 'website', 'order')


# ── Admin ─────────────────────────────────────────────────────────────────────
class AdminPartnerClientSerializer(serializers.ModelSerializer):
    """Hamkor to'liq CRUD — admin uchun.
    Yaratishda is_active yuborilmasa default=True (model darajasida).
    Tahrirlashda (PUT/PATCH) is_active o'zgartirilishi mumkin.
    """

    class Meta:
        model = PartnerClient
        fields = ('id', 'name', 'logo', 'website', 'order', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_fields(self):
        fields = super().get_fields()
        # POST (yaratish) da is_active ni required emas, model default=True ishlatadi
        if self.context.get('request') and self.context['request'].method == 'POST':
            fields['is_active'].required = False
            fields['is_active'].read_only = True
        return fields
