from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError

class CuisineType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    cuisine_types = models.ManyToManyField(CuisineType, related_name='restaurants')
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    def __str__(self):
        return self.name

    def get_average_rating(self):
        average = self.comments.aggregate(avg=Avg('rating'))['avg']
        return round(average, 1) if average is not None else 0.0
    
    @property
    def cuisine_list(self):
        return ", ".join(self.cuisine_types.values_list('name', flat=True))
    
    def save(self, *args, **kwargs):
        # Jeśli nie mamy współrzędnych, spróbuj geokodować na podstawie adresu
        if self.address and (self.latitude is None or self.longitude is None):
            geolocator = Nominatim(user_agent="restaurant_portal")
            try:
                location = geolocator.geocode(self.address, language='pl')
                if location:
                    self.latitude = round(location.latitude, 6)
                    self.longitude = round(location.longitude, 6)
                print(location)
                print(self.address)
            except GeocoderServiceError:
                pass

        super().save(*args, **kwargs)

class Comment(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    author = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Ocena od 1 do 5"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} ({self.rating}/5)"