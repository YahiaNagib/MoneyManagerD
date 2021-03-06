from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Item, Category, CategoryType, Account
from .forms import AddItemForm, UserRegisterForm
from .utils import data_reshaping, get_statistics, account_after_item_delete
from datetime import datetime

def home(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to continue")
        return redirect("login")
    if request.GET.get('m'):
        Month = int(request.GET.get('m'))
    else:
        Month = datetime.now().month
    account = Account.objects.filter(user=request.user, active=True).first()
    items = Item.objects.filter(account=account, date__month=Month).all()
    context = {
        'title': account.user.username,
        'items': data_reshaping(items),
        'account': account
    }
    return render(request, "home/home.html", context)

@login_required
def add_item(request):
    if request.method == "POST":
        form = AddItemForm(request.POST)
        if form.is_valid():
            account = Account.objects.filter(user=request.user, active=True).first()
            form.instance.account = account
            if str(form.cleaned_data["category_type"]) == "Expenses":
                account.total_spendings = account.total_spendings + form.cleaned_data.get("value")
                account.save()
            else:
                account.total_income = account.total_income + form.cleaned_data.get("value")
                account.save()
            form.save()
            messages.success(request, "Item has been added")
            return redirect("home")
    else:
        form = AddItemForm()
    return render(request, 'home/additem.html', {'form': form, 'title': "Add"})

@login_required
def edit_item(request, id):
    if request.method == "POST":
        item = Item.objects.filter(id=id).first()
        old_value = item.value
        old_category_type = item.category.category_type.type_name
        form = AddItemForm(request.POST, instance=item)
        account = Account.objects.filter(user=request.user, active=True).first()
        if form.is_valid():
            if str(form.cleaned_data["category_type"]) != old_category_type:
                if str(form.cleaned_data["category_type"]) == "Expenses":
                    account.total_income = account.total_income - old_value
                    account.total_spendings = account.total_spendings + form.cleaned_data.get("value")
                    account.save()
                else:
                    account.total_spendings = account.total_spendings - old_value
                    account.total_income = account.total_income + form.cleaned_data.get("value")
                    account.save()
            else:
                if str(form.cleaned_data["category_type"]) == "Expenses":
                    account.total_spendings = account.total_spendings - old_value
                    account.total_spendings = account.total_spendings + form.cleaned_data.get("value")
                    account.save()
                else:
                    account.total_income = account.total_income - old_value
                    account.total_income = account.total_income + form.cleaned_data.get("value")
                    account.save()
            form.save()
            messages.success(request, "Item has been updated")
            return redirect("home")
    else:
        item = Item.objects.filter(id=id).first()
        form = AddItemForm(instance=item, initial={'category_type': item.category.category_type})
        return render(request, 'home/edititem.html', {'form': form, 'title': "Edit Item", 'id': id})

@login_required
def delete_item(request, id):
    item = Item.objects.get(pk=id)
    account_after_item_delete(request.user, item)
    item.delete()
    messages.success(request, "Category has been deleted")
    return redirect("home")

@login_required
def categories(request):
    if request.method == "POST":
        if request.POST.get("new_expense"):
            category = Category(category_type_id=1, name=request.POST.get("new_expense"))
        else:
            category = Category(category_type_id=2, name=request.POST.get("new_income"))
        category.save()
        messages.success(request, "Category has been added")
        return redirect("categories")
    else:
        context = {
            'title': "Edit Categories",
            'expense_categories': Category.objects.filter(category_type_id = 1),
            'income_categories': Category.objects.filter(category_type_id = 2)
        }
        return render(request, 'home/categories.html', context)

@login_required
def delete_category(request, id):
    pass
    # category = Category.objects.get(pk=id)
    # account = Account.objects.filter(user=request.user).first()
    # for item in category.items.all():
    #     account_after_item_delete(request.user, item)
    # category.delete()
    # messages.success(request, "Category has been deleted")
    # return redirect("home")

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your account has been created, you are now able to login")
            user = User.objects.filter(username=str(form.cleaned_data["username"])).first()
            account = Account(user=user)
            account.save()
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, 'home/register.html', {'form': form})

@login_required
def accounts(request):
    pass
    # context={
    #     'title': 'Accounts',
    #     'user': request.user,
    #     'accounts': Account.objects.filter(user=request.user).all()
    # }
    # return render(request, 'home/accounts.html', context)

@login_required
def activate_account(request, id):
    pass
#     accounts = Account.objects.filter(user=request.user).all()
#     for account in accounts:
#         if account.id == id:
#             account.active = True
#         else:
#             account.active = False
#         account.save()
#     account = Account.objects.filter(user=request.user, active=True).first()
#     messages.success(request, f"Account {account.name} is activated")
#     return redirect("home")

@login_required
def statistics(request):
    items_expenses = get_statistics(request.user, 1)
    items_income = get_statistics(request.user, 2)
    context={
        'title': 'statistics',
        'items_expenses': items_expenses,
        'items_income': items_income
    }
    if request.method == "POST":
        if int(request.POST.get("CategoryType")) == 1:
            return JsonResponse(items_expenses, safe=False)
        else:
            return JsonResponse(items_income, safe=False)
    return render(request, 'home/statistics.html', context)

@login_required
def category_statisitcs_redirect(request, category_name):
    name = category_name.replace('%', "0")
    name = name.replace('.', "0")
    name = ''.join([i for i in name if not i.isdigit()])
    result = name.rstrip()
    return redirect(f"/statistics/{result}")

@login_required
def category_statistics(request, category_name):
    category = Category.objects.filter(name = category_name).first()
    account = Account.objects.filter(user=request.user, active=True).first()
    context = {
        'title': "Statistics",
        'items': category.items.filter(account=account).order_by("-value")
     }
    return render(request, "home/item_statistics.html", context)

def logout_user(request):
    logout(request)
    return redirect("login")

def load_categories(request):
    category_type =CategoryType.objects.filter(id=request.GET.get('CategoryType')).first()
    categories = Category.objects.filter(category_type=category_type)
    return render(request, 'home/category_dropdown.html', {'categories': categories})

 