from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VehicleCategoryViewSet, VehicleViewSet,
    AdminVehicleCategoryViewSet, AdminVehicleViewSet, AdminVehicleImageViewSet,
)

# ── Public router ─────────────────────────────────────────────────────────────
public_router = DefaultRouter()
public_router.register('categories', VehicleCategoryViewSet, basename='vehicle-category')
public_router.register('vehicles', VehicleViewSet, basename='vehicle')

# ── Admin router ──────────────────────────────────────────────────────────────
admin_router = DefaultRouter()
admin_router.register('categories', AdminVehicleCategoryViewSet, basename='admin-vehicle-category')
admin_router.register('vehicles', AdminVehicleViewSet, basename='admin-vehicle')
admin_router.register('images', AdminVehicleImageViewSet, basename='admin-vehicle-image')

urlpatterns = [
    # Public
    path('', include(public_router.urls)),
    # Admin CRUD
    path('admin/', include(admin_router.urls)),
]
