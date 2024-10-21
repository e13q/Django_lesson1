import os
import requests

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile

from places.models import Place, Image


class Command(BaseCommand):
    help = 'Add places from JSON data'

    def add_arguments(self, parser):
        parser.add_argument('json_url', type=str, help='URL to the JSON file')

    def handle(self, *args, **kwargs):
        json_url = kwargs['json_url']
        try:
            raw_place = requests.get(json_url)
            raw_place.raise_for_status()
            raw_place = raw_place.json()
            place, created = Place.objects.get_or_create(
                title=raw_place['title'],
                defaults={
                    'short_description': raw_place['description_short'],
                    'long_description': raw_place['description_long'],
                    'longitude': raw_place['coordinates']['lng'],
                    'latitude': raw_place['coordinates']['lat'],
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Place {place.title} created')
                )
                for index, img_url in enumerate(raw_place['imgs']):
                    raw_img = requests.get(img_url)
                    raw_img.raise_for_status()
                    img_content = ContentFile(
                        raw_img.content, name=os.path.basename(img_url)
                    )
                    Image.objects.get_or_create(
                        place=place, ordinal_number=index + 1,
                        defaults={
                            'ordinal_number': index + 1,
                            'place': place,
                            'image': img_content
                        }
                    )
                self.stdout.write(self.style.SUCCESS(
                    f'Images added to place {place.title}'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Place {place.title} already exists'
                ))
                return None
        except Place.MultipleObjectsReturned as e:
            self.stdout.write(self.style.ERROR(
                f'Multiple objects returned: {str(e)}'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
