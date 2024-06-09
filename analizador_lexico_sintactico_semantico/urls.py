# # user_chat/urls.py Rutas de la aplicación
from django.urls import path, re_path
from .views import home


urlpatterns = [
    path('semantico/', home, name='semantico')
]