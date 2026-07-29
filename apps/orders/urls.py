from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderCreateView, AdminOrderViewSet

# ── Admin router ──────────────────────────────────────────────────────────────
admin_router = DefaultRouter()
admin_router.register('', AdminOrderViewSet, basename='admin-order')

urlpatterns = [
    # Public: ariza qoldirish
    path('', OrderCreateView.as_view(), name='order-create'),
    # Admin: to'liq CRUD
    path('admin/', include(admin_router.urls)),
]
