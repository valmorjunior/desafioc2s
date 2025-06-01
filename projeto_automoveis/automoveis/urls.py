from django.urls import path
from . import views

app_name = 'automoveis'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.api_automoveis, name='api_automoveis'),
    path('busca-rapida/', views.busca_rapida, name='busca_rapida'),
]
