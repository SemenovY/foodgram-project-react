"""Custom mixins"""
from rest_framework import mixins, viewsets


class CreateDestroyViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """Базовый класс для вьюсетов Избранного и Списка покупок.
    Создание и удаление.
    """


class ListSubscriptionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Вазовый класс представления списка подписок"""
