import csv
import os

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


def ingredients_create(row):
    Ingredient.objects.get_or_create(
        name=row[0],
        measurement_unit=row[1],
    )


class Command(BaseCommand):
    action = {
        'ingredients.csv': ingredients_create,
    }

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            nargs='+',
            type=str
        )

    def handle(self, *args, **options):
        for filename in options['filename']:
            path = os.path.join(
                'C:/Dev/foodgram-project-react/data/'
            ) + filename
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    self.action[filename](row)
