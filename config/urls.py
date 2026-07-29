from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # ── Django admin panel ────────────────────────────────────────────────────
    path('admin/', admin.site.urls),

    # ── Fleet (Avtopark) ──────────────────────────────────────────────────────
    # PUBLIC:
    #   GET  /api/v1/fleet/categories/               — kategoriyalar ro'yxati
    #   GET  /api/v1/fleet/categories/{slug}/        — kategoriya detail
    #   GET  /api/v1/fleet/vehicles/                 — mashinalar (filtrlash bilan)
    #   GET  /api/v1/fleet/vehicles/{slug}/          — mashina detail
    # ADMIN (JWT):
    #   CRUD /api/v1/fleet/admin/categories/{id}/
    #   CRUD /api/v1/fleet/admin/vehicles/{id}/
    #   CRUD /api/v1/fleet/admin/images/{id}/
    #   PATCH /api/v1/fleet/admin/vehicles/{id}/toggle_active/
    path('fleet/', include('apps.fleet.urls')),

    # ── Services (Xizmatlar) ──────────────────────────────────────────────────
    # PUBLIC:
    #   GET  /api/v1/services/directions/            — xizmatlar ro'yxati
    #   GET  /api/v1/services/directions/{slug}/     — xizmat detail
    #   GET  /api/v1/services/features/              — afzalliklar
    # ADMIN (JWT):
    #   CRUD /api/v1/services/admin/directions/{id}/
    #   CRUD /api/v1/services/admin/features/{id}/
    path('services/', include('apps.services.urls')),

    # ── Clients (Hamkorlar) ───────────────────────────────────────────────────
    # PUBLIC:
    #   GET  /api/v1/clients/list/                   — hamkorlar logotipi
    # ADMIN (JWT):
    #   CRUD /api/v1/clients/admin/list/{id}/
    path('clients/', include('apps.clients.urls')),

    # ── Orders (Arizalar) ─────────────────────────────────────────────────────
    # PUBLIC:
    #   POST /api/v1/orders/                         — ariza qoldirish
    # ADMIN (JWT):
    #   CRUD /api/v1/orders/admin/{id}/
    #   PATCH /api/v1/orders/admin/{id}/set_status/  — tezkor holat o'zgartirish
    path('orders/', include('apps.orders.urls')),

    # ── Site Settings (Sayt sozlamalari) ──────────────────────────────────────
    # PUBLIC:
    #   GET  /api/v1/site-settings/                  — dinamik ma'lumotlar
    # ADMIN (JWT):
    #   GET  /api/v1/site-settings/admin/
    #   PUT  /api/v1/site-settings/admin/
    #   PATCH /api/v1/site-settings/admin/
    path('site-settings/', include('apps.sitesettings.urls')),

    # ── Auth (Foydalanuvchilar) ───────────────────────────────────────────────
    #   POST /api/v1/auth/login/                     — JWT token olish
    #   POST /api/v1/auth/refresh/                   — token yangilash
    #   GET  /api/v1/auth/me/                        — o'z profili
    path('', include('apps.users.urls')),

    # ── Swagger / OpenAPI ─────────────────────────────────────────────────────
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('',   SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/',  SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
