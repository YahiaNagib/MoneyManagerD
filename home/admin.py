from django.contrib import admin
from .models import CategoryType, Category, Item, Account
# Register your models here.

admin.site.register(CategoryType)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Account)

