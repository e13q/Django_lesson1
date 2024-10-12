from django.db import models

from tinymce.models import HTMLField

class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название места")
    description_short = models.TextField(verbose_name="Краткое описание")
    description_long = HTMLField(verbose_name="Полное описание")
    coordinates_lng = models.FloatField(verbose_name="Долгота")
    coordinates_lat = models.FloatField(verbose_name="Широта")

    def __str__(self) -> str:
        return self.title


class Image(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images', verbose_name="Интересное место")
    ordinal_number = models.IntegerField(verbose_name="Порядок картинки")
    image = models.ImageField("Картинка")

    def __str__(self):
        return f'{self.ordinal_number} {self.place.title}'
    
    class Meta:
        ordering = ['ordinal_number']
        
