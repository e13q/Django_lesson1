from django.db import models


class Image(models.Model):
    ordinal_number = models.IntegerField()
    title = models.CharField(max_length=200)
    image = models.ImageField()

    def __str__(self):
        return f'{self.ordinal_number} {self.title}'


class Coordinates(models.Model):
    lng = models.FloatField()
    lat = models.FloatField()

    def __str__(self):
        return f'{self.lng} {self.lat}'


class Place(models.Model):
    title = models.CharField(max_length=200)
    images = models.ManyToManyField(
        Image, blank=True
    )
    description_short = models.CharField(max_length=200)
    description_long = models.TextField()
    coordinates = models.ForeignKey(Coordinates, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.title
