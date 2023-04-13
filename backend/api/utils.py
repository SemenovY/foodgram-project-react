"""Вспомогательные функции"""
from datetime import datetime as dt
from django.db.models import F, Sum
from django.http import HttpResponse

from backend.settings import DATE_TIME_FORMAT

from recipes.models import Ingredient


def get_shopping_list(self, request):
    """Выгрузка текстового файла со списком покупок.
    Подсчёт суммы ингредиентов по всем рецептам из корзины.
    Адрес: */recipes/download_shopping_cart/.
    """
    user = self.request.user
    filename = f"{user.username}_shopping_list.txt"
    shopping_list = [
        f"Список покупок:\n"
        f"{user.first_name} {user.last_name}\n"
        f"Дата: {dt.now().strftime(DATE_TIME_FORMAT)}\n"
        f"____________________________"
    ]

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

    shopping_list.append("____________________________\n" "За покупками!\n")
    shopping_list = "\n".join(shopping_list)
    response = HttpResponse(
        shopping_list, content_type="text.txt; charset=utf-8"
    )
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response
