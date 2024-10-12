from django.db import models

from tinymce.models import HTMLField

class Place(models.Model):
    title = models.CharField(max_length=200)
    description_short = models.TextField()
    description_long = HTMLField()
    coordinates_lng = models.FloatField()
    coordinates_lat = models.FloatField()

    def __str__(self) -> str:
        return self.title


class Image(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
    ordinal_number = models.IntegerField()
    image = models.ImageField()

    def __str__(self):
        return f'{self.ordinal_number} {self.place.title}'
    
    class Meta:
        ordering = ['ordinal_number']
        
