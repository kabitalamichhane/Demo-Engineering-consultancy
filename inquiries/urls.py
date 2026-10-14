from django.urls import path
from . import views

app_name = 'inquiries'

urlpatterns = [
    path('contact-us/', views.contact_view, name='contact'),
    path('get-a-quote/', views.get_a_quote_view, name='get_a_quote'),
    path('work-with-us/', views.work_with_us_view, name='work_with_us'),
]
