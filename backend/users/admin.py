# abstract_user/users/admin.py
"""Admin panel for user models."""
from django.contrib import admin

from .models import User

admin.site.register(User)
