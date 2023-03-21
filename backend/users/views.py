# ice_cream/views.py
from django.http import HttpResponse
from django.shortcuts import render


# Главная страница
def index(request):
    return HttpResponse('Главная страница')


# Страница со списком мороженого
def ice_cream_list(request):
    return HttpResponse('Список мороженого')


# Страница с информацией об одном сорте мороженого;
# view-функция принимает параметр pk из path()
def ice_cream_detail(request, pk):
    return HttpResponse(f'Мороженое номер {pk}')
