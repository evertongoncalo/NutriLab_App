
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.urls import path



urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('', include('plataforma.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
