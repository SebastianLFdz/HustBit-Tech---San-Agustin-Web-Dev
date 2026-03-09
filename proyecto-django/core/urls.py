from django.urls import path
from . import views

urlpatterns = [
    path('contacto/', views.contacto, name='contacto'),
    path('about/', views.about, name='about'),
    path('referencias/', views.referencias, name='referencias'),
    path('login/', views.login, name='login'),
    path('admin/', views.admin, name='admin'),
]