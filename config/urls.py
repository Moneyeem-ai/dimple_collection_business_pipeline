from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path('GcVVDn27GczHMeEAQeyyRShjS3WGwofrXqdFFmju0I/', admin.site.urls),
    path('', include('apps.admin_adminlte.urls')),
    path('product/', include('apps.product.urls')),
    path('department/', include('apps.department.urls')),
    path('test/', TemplateView.as_view(template_name='pages/test.html'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
