"""Загружаем данные ингредиентов из файла"""
import json

from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    """Команда для загрузки ингредиентов из файла"""

    def handle(self, *args, **options):
        """Загружаем данные ингредиентов из файла"""
        with open("/app/data/ingredients.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                ingredient = Ingredient.objects.create(
                    name=item["name"],
                    measurement_unit=item["measurement_unit"],
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully created {ingredient.name}"
                    )
                )
