from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ServiceDirectionViewSet, ServiceFeatureViewSet,
    AdminServiceDirectionViewSet, AdminServiceFeatureViewSet,
)

# ── Public router ─────────────────────────────────────────────────────────────
public_router = DefaultRouter()
public_router.register('features', ServiceFeatureViewSet, basename='service-feature')
public_router.register('directions', ServiceDirectionViewSet, basename='service')

# ── Admin router ──────────────────────────────────────────────────────────────
admin_router = DefaultRouter()
admin_router.register('features', AdminServiceFeatureViewSet, basename='admin-service-feature')
admin_router.register('directions', AdminServiceDirectionViewSet, basename='admin-service')

urlpatterns = [
    # Public:  /api/v1/services/directions/      /api/v1/services/features/
    path('', include(public_router.urls)),
    # Admin:   /api/v1/services/admin/directions/  /api/v1/services/admin/features/
    path('admin/', include(admin_router.urls)),
]
