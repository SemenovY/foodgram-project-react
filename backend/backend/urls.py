"""Backend URL Configuration."""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'api/docs',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc',
    ),
    # Djoser создаст набор необходимых эндпоинтов.
    # базовые, для управления пользователями в Django:
    #    path('auth/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    # path('auth/', include('djoser.urls.jwt')),
]

# path('api/', include('api.urls')),
# path('api/', include('users.urls')),
