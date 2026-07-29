from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PartnerClientViewSet, AdminPartnerClientViewSet

# ── Public router ─────────────────────────────────────────────────────────────
public_router = DefaultRouter()
public_router.register('list', PartnerClientViewSet, basename='client')

# ── Admin router ──────────────────────────────────────────────────────────────
admin_router = DefaultRouter()
admin_router.register('list', AdminPartnerClientViewSet, basename='admin-client')

urlpatterns = [
    # Public:  /api/v1/clients/list/
    path('', include(public_router.urls)),
    # Admin:   /api/v1/clients/admin/list/
    path('admin/', include(admin_router.urls)),
]
