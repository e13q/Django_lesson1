from django.db import models

from tinymce.models import HTMLField

class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название места")
    short_description = models.TextField(blank=True, verbose_name="Краткое описание")
    long_description = HTMLField(blank=True, verbose_name="Полное описание")
    longitude = models.FloatField(verbose_name="Долгота")
    latitude = models.FloatField(verbose_name="Широта")

    def __str__(self) -> str:
        return self.title


class Image(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images', verbose_name="Интересное место")
    ordinal_number = models.IntegerField(verbose_name="Порядок картинки")
    image = models.ImageField(verbose_name="Картинка")

    def __str__(self):
        return f'{self.ordinal_number} {self.place.title}'
    
    class Meta:
        ordering = ['ordinal_number']
        
