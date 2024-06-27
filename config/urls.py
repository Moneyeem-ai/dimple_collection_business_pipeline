from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic import RedirectView


urlpatterns = [
    path('dimplecollection/admin/', admin.site.urls),
    path('product/', include('apps.product.urls')),
    path('department/', include('apps.department.urls')),
    path('user/', include('apps.user.urls')),
    path('po/', include('apps.procurement.urls')),
    path('', RedirectView.as_view(url=reverse_lazy('user:login'))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
