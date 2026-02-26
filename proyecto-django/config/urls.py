from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.view),
    path('', include('core.urls')), # Esto conecta tu app core
]