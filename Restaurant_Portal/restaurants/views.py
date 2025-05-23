from django.shortcuts import get_object_or_404, render
from .models import Restaurant
from django.db.models import Avg

def restaurant_list(request):
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'name')

    # Dozwolone pola sortowania
    allowed_sort_fields = ['name', '-name', 'average_rating', '-average_rating']
    if sort_by not in allowed_sort_fields:
        sort_by = 'name'

    # Pobierz restauracje z filtrem i anotacją średniej oceny
    restaurants = Restaurant.objects.filter(
        name__icontains=search_query
    ).annotate(
        average_rating=Avg('comments__rating')
    ).order_by(sort_by)

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
