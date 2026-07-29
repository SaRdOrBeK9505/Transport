from django.urls import path
from .views import SiteConfigPublicView, SiteConfigAdminView

urlpatterns = [
    # Public
    path('', SiteConfigPublicView.as_view(), name='site-settings'),
    # Admin
    path('admin/', SiteConfigAdminView.as_view(), name='admin-site-settings'),
]
