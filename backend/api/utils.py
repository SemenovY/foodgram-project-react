"""Вспомогательные функции, выгружаем список покупок"""
from django.db.models import F, Sum
from django.http import HttpResponse
from recipes.models import Ingredient


def get_shopping_list(self, request):
    """Выгрузка txt файла со списком покупок.
    Подсчёт суммы ингредиентов по всем рецептам.
    """
    user = self.request.user
    filename = f"{user.username}_shopping_list.txt"
    shopping_list = "Список покупок:"
    ingredients = (
        Ingredient.objects.filter(
            amount__recipe__shopping_cart_recipe__user=user
        )
        .values("name", measurement=F("measurement_unit"))
        .annotate(amount=Sum("amount__amount"))
    )

    for ing in ingredients:
        shopping_list.append(
            f'- {ing["name"]}: {ing["amount"]} {ing["measurement"]}'
        )
    response = HttpResponse(
        shopping_list, content_type="text.txt; charset=utf-8"
    )
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response
