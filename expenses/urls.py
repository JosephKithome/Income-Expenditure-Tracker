from django.urls import path
from . import views

urlpatterns = [
    path('',views.Index, name = "index"),
    path('add_expense', views.add_expense,name ='add_expense')
]