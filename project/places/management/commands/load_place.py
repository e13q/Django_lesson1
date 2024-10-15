import json
import os
from urllib.request import urlopen

from django.core.management.base import BaseCommand

from places.models import Place, Image


class Command(BaseCommand):
    help = 'Add places from JSON data'

    def add_arguments(self, parser):
        parser.add_argument('json_url', type=str, help='URL to the JSON file')

    def handle(self, *args, **kwargs):
        json_url = kwargs['json_url']
        try:
            with urlopen(json_url) as file:
                data = json.load(file)
                place, created = Place.objects.get_or_create(
                    title=data['title'],
                    defaults={
                        'short_description': data['description_short'],
                        'long_description': data['description_long'],
                        'longitude': data['coordinates']['lng'],
                        'latitude': data['coordinates']['lat'],
                    }
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f"Place '{place.title}' created")
                    )
                    for index, img_url in enumerate(data['imgs']):
                        img_temp = urlopen(img_url)
                        img, _ = Image.objects.get_or_create(
                            place=place, ordinal_number=index + 1,
                            defaults={
                                'ordinal_number': index + 1,
                                'place': place,
                            }
                        )
                        img.image.save(
                            os.path.basename(img_url),
                            img_temp,
                            save=True
                        )
                        img.save()
                    self.stdout.write(self.style.SUCCESS(
                        f"Images added to place '{place.title}'"
                    ))
                else:
                    self.stdout.write(self.style.WARNING(
                        f"Place '{place.title}' already exists"
                    ))
                    return None
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
