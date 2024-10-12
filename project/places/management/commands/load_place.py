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
                        'description_short': data['description_short'],
                        'description_long': data['description_long'],
                        'coordinates_lng': data['coordinates']['lng'],
                        'coordinates_lat': data['coordinates']['lat'],
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Place '{place.title}' created"))
                else:
                    self.stdout.write(self.style.WARNING(f"Place '{place.title}' already exists"))
                    return None

                for index, img_url in enumerate(data['imgs']):
                    img_temp = urlopen(img_url)
                    img, _ = Image.objects.get_or_create(
                        place=place, ordinal_number=index + 1,
                        defaults={
                            'ordinal_number': index + 1,
                            'place': place,
                        }
                    )
                    img.image.save(os.path.basename(img_url), img_temp, save=True)
                    img.save()
                    
                self.stdout.write(self.style.SUCCESS(f"Images added to place '{place.title}'"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))