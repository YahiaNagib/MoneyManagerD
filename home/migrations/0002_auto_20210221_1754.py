# Generated by Django 3.0.7 on 2021-02-21 15:18

from django.db import migrations
from home.models import CategoryType, Category

def add_category_type_data(apps, schema_editor):
    expenses = CategoryType(id=1, type_name="Expenses")
    expenses.save()
    income = CategoryType(id=2, type_name="Income")
    income.save()


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_category_type_data),
    ]
