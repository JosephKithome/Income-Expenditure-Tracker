from . import  views
from django.urls import path

urlpatterns = [
    path('preferences',views.preferences, name = 'preferences')
]