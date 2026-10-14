from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('metal-fabrication/', views.metal_fabrication, name='metal_fabrication'),
    path('<slug:slug>/', views.service_detail, name='service_detail'),
]
