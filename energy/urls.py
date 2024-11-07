from django.urls import path
from . import views

urlpatterns = [
    path('calculator/', views.energy_calculator, name='energy_calculator'),
    path('map/', views.renewable_map, name='renewable_map'),
    path('news/', views.renewable_news, name='renewable_news'),
    path('windmap/', views.wind_map, name='wind_map'),
    path('home/', views.home_page, name='home_page'),
    path('news/', views.renewable_news, name='renewable_news'),
    path('why/', views.why_renewable, name='why_renewable'),
    path('get_started/', views.get_started, name='get_started'),
    path('chat/', views.chat_view, name='chat_view'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),



]
