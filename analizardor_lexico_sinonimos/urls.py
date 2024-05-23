from django.urls import path, re_path
from .views import home


urlpatterns = [
    path('sinonimos/', home, name='home'),

]