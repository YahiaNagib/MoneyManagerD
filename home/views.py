from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Item, Category, CategoryType, Account
from .forms import AddItemForm
from .utils import data_reshaping, get_statistics, account_after_item_delete

def home(request):
    items = Item.objects.filter(user=request.user).all()
    account = Account.objects.filter(user=request.user).first()
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
            form.instance.user = request.user
            account = Account.objects.filter(user=request.user).first()
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
        form = AddItemForm(request.POST, instance=item)
        account = Account.objects.filter(user=request.user).first()
        if form.is_valid():
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

def delete_item(request, id):
    item = Item.objects.get(pk=id)
    account_after_item_delete(request.user, item)
    item.delete()
    messages.success(request, "Category has been deleted")
    return redirect("home")

def categories(request):
    if request.method == "POST":
        if request.POST.get("new_expense"):
            category = Category(category_type_id=1, name=request.POST.get("new_expense"))
        else:
            category = Category(category_type_id=2, name=request.POST.get("new_income"))
        category.save()
        messages.success(request, "Category has been added")
        return redirect("home")
    else:
        context = {
            'title': "Edit Categories",
            'expense_categories': Category.objects.filter(category_type_id = 1),
            'income_categories': Category.objects.filter(category_type_id = 2)
        }
        return render(request, 'home/categories.html', context)

def delete_category(request, id):
    category = Category.objects.get(pk=id)
    account = Account.objects.filter(user=request.user).first()
    # for item in category.items.all():
    #     account_after_item_delete(request.user, item)
    # category.delete()
    messages.success(request, "Category has been deleted")
    return redirect("home")

def statistics(request):
    items = get_statistics(request.user)
    if request.method == "POST":
        return JsonResponse(items, safe=False)
    return render(request, 'home/statistics.html', {'title': 'statistics', 'items': items})

def category_statisitcs_redirect(request, category_name):
    name = category_name.replace('%', "0")
    name = name.replace('.', "0")
    name = ''.join([i for i in name if not i.isdigit()])
    result = name.rstrip()
    return redirect(f"/statistics/{result}")

def category_statistics(request, category_name):
    category = Category.objects.filter(name = category_name).first()
    context = {
        'title': "Statistics",
        'items': category.items.all().order_by("-value")
     }
    return render(request, "home/item_statistics.html", context)


def load_categories(request):
    Category_Type =CategoryType.objects.filter(id=request.GET.get('CategoryType')).first()
    categories = Category.objects.filter(category_type=Category_Type)
    return render(request, 'home/category_dropdown.html', {'categories': categories})

