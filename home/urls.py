from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add_item, name="add-item"),
    path('edit/<int:id>/', views.edit_item, name="item-edit"),
    path('categories/', views.categories, name="categories"),
    path('accounts/', views.accounts, name="accounts"),
    path('delete/category/<int:id>', views.delete_category, name="delete-category"),
    path('delete/item/<int:id>', views.delete_item, name="delete-item"),
    path('statistics/', views.statistics, name="statistics"),
    path('statisitcs/redirect/<str:category_name>', views.category_statisitcs_redirect, name="statistics-redirect"),
    path('statistics/<str:category_name>', views.category_statistics, name="statistics-category"),
    path('activate/<int:id>', views.activate_account, name="activate"),
    path('login/', auth_views.LoginView.as_view(template_name="home/login.html"), name='login'),
    path('ajax/load-categories/', views.load_categories, name='ajax_load_categories')
]
