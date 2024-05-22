from django.urls import path, re_path
from .views import home, examen


urlpatterns = [
    path('V2/', home, name='home'),
    path('V2/examen', examen, name='examen' )
]