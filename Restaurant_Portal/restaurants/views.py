from django.shortcuts import get_object_or_404, render
from .models import Restaurant
from django.db.models import Avg
from geopy.distance import distance as geopy_distance
from geopy.geocoders import Nominatim
import requests

def get_coordinates_from_address(address):
    geolocator = Nominatim(user_agent="restaurant_app")
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    return None

def get_coordinates_from_ip(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            return (data['lat'], data['lon'])
    except:
        return None
    
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def safe_sort_key(r, field):
    value = getattr(r, field)
    # Jeśli None, to daj -1 dla ocen (bo skala to 0-5) lub pusty string dla nazw
    if value is None:
        return -1 if 'rating' in field else ''
    return value
    
def restaurant_list(request):
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'name')
    address_input = request.GET.get('address', '')
    max_distance_km = float(request.GET.get('distance', 10))

    allowed_sort_fields = ['name', '-name', 'average_rating', '-average_rating']
    if sort_by not in allowed_sort_fields:
        sort_by = 'name'

    # Pobranie współrzędnych użytkownika
    if address_input:
        user_location = get_coordinates_from_address(address_input)
    else:
        user_ip = get_client_ip(request)
        if user_ip == '127.0.0.1':
            user_ip = '83.8.161.168'
        user_location = get_coordinates_from_ip(user_ip)

    # Filtrowanie i anotacja
    restaurants = Restaurant.objects.filter(
        name__icontains=search_query
    ).annotate(
        average_rating=Avg('comments__rating')
    )

    # Filtruj według odległości jeśli lokalizacja dostępna
    if user_location:
        filtered_restaurants = []
        for restaurant in restaurants:
            if restaurant.latitude and restaurant.longitude:
                rest_location = (restaurant.latitude, restaurant.longitude)
                dist = geopy_distance(user_location, rest_location).km
                if dist <= max_distance_km:
                    restaurant.distance_km = round(dist, 2)
                    filtered_restaurants.append(restaurant)
        field = sort_by.strip('-')
        reverse = sort_by.startswith('-')
        restaurants = sorted(
            filtered_restaurants,
            key=lambda r: safe_sort_key(r, field),
            reverse=reverse
        )

    return render(request, 'restaurants/restaurant_list.html', {
        'restaurants': restaurants
    })

def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    comments = restaurant.comments.all()
    return render(request, 'restaurants/restaurant_detail.html', {
        'restaurant': restaurant,
        'comments': comments,
    })
