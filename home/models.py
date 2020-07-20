from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class CategoryType(models.Model):
    type_name = models.CharField(max_length=50)
    def __str__(self):
        return self.type_name

class Category(models.Model):
    category_type = models.ForeignKey(CategoryType, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Account(models.Model):
    user = models.ForeignKey(User, related_name="accounts", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="Personal Account")
    total_income = models.FloatField(default=0)
    total_spendings = models.FloatField(default=0)
    active = models.BooleanField(default=True)
    def __str__(self):
        return f"name: {self.name}, user: {self.user.username}, Income: {self.total_income}, Spent: {self.total_spendings}"

class Item(models.Model):
    category= models.ForeignKey(Category, related_name="items", on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    value = models.FloatField()
    notes = models.TextField()
    def __str__(self):
        return f"{self.category.name}, {self.value}"
