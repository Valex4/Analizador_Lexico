from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('analizador_lexico.urls')),
    path('', include('analizador_lexico_V2.urls')),
    path('', include('analizardor_lexico_sinonimos.urls')),
    path('',include('analizador_lexico_sintactico_semantico.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
