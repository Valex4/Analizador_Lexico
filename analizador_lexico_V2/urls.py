from django.urls import path, re_path
from .views import home


urlpatterns = [
    path('V2/', home, name='home'),
]