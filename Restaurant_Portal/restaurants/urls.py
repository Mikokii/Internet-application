from django.urls import path
from .views import restaurant_detail, restaurant_list

urlpatterns = [
    path('', restaurant_list, name='restaurant_list'),
    path('restaurant/<int:pk>/', restaurant_detail, name='restaurant_detail'),
]
