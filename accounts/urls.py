from django.urls import path
from .views import registration_view

urlpatterns = [
    path("registrazione/",registration_view,name='registration_view'),
]