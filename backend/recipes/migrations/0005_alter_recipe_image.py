# Generated by Django 3.2 on 2023-04-03 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20230403_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(null=True, upload_to='recipes/images/', verbose_name='Фотография рецепта'),
        ),
    ]
