import csv
import os

from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model

from recipes.models import Ingredient

User = get_user_model()


def ingredients_create(row):
    Ingredient.objects.get_or_create(
        name=row[0],
        measurement_unit=row[1],
    )

action = {
    'ingredients.csv': ingredients_create,
}


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            nargs='+',
            type=str
        )

    def handle(self, *args, **options):
        for filename in options['filename']:
            path = os.path.join('C:/Dev/foodgram-project-react/data/') + filename
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    action[filename](row)
