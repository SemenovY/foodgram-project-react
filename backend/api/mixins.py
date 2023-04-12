"""Custom mixins"""
from rest_framework import mixins, viewsets


class CreateDestroyViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """Базовый класс для ViewSet Избранного и Списка покупок"""


class ListSubscriptionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Вазовый класс для представления списка подписок"""
