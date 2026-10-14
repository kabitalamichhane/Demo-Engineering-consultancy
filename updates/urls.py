from django.urls import path
from . import views

app_name = 'updates'

urlpatterns = [
    path('', views.update_list, name='update_list'),
    path('<slug:slug>/', views.update_detail, name='update_detail'),
]
