from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    cuisine_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_average_rating(self):
        average = self.comments.aggregate(avg=Avg('rating'))['avg']
        return round(average, 1) if average is not None else 0.0

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