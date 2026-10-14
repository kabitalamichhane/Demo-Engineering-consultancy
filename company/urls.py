from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.about_us, name='about'),
    path('i18n/<str:lang>.json', views.i18n_dictionary, name='i18n_dictionary'),
    path('chatbot/faqs/', views.chatbot_faqs, name='chatbot_faqs'),
    path('chatbot/ask/', views.chatbot_ask, name='chatbot_ask'),
    path('chatbot/callback/', views.chatbot_callback, name='chatbot_callback'),
]
