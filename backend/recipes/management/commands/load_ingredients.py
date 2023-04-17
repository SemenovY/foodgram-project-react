"""Загружаем данные ингредиентов из файла"""
import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    """Команда для загрузки ингредиентов из файла"""

    help = "Загружаем данные ингредиентов из файла"

    def handle(self, **options):
        """Загружаем данные ингредиентов из файла"""
        with open("data/ingredients.csv", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            Ingredient.objects.bulk_create(
                [
                    Ingredient(id=num, name=line[0], measurement_unit=line[1])
                    for num, line in enumerate(reader)
                ]
            )
