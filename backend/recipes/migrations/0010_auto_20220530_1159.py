# Generated by Django 2.2.19 on 2022-05-30 08:59

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_auto_20220530_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient', to='recipes.Recipe'),
        ),
    ]
