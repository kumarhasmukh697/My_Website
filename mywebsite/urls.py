# import all the necessary modules
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('portfolio_details/<int:id>/', views.portfolio_details, name='portfolio_details'),
    path('send_message/', views.send_message, name='send_message'),
]