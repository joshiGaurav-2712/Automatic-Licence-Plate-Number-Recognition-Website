from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home Page'),
    path('processed_image/', views.processed_image, name='Image Processed Page')
]