from .models import Category, CategoryType, Item, Account

def data_reshaping(items):
    dates = []
    data = []
    for item in items:
        if item.date.date() not in dates:
            dates.append(item.date.date())
    for date in dates:
        dic = {}
        dic["date"] = date
        dic["items"] = []
        dic["expenses"] = 0
        dic["income"] = 0
        for item in items:
            if item.date.date() == date:
                dic["items"].append(item)
                if item.category.category_type.id == 2:
                    dic["income"] = dic["income"] + float(item.value)
                else:
                    dic["expenses"] = dic["expenses"] + float(item.value)
        data.append(dic)
    return sorted(data, key=lambda i: i['date'], reverse=True)


def get_statistics(user):
    #expenses only for now
    categories = Category.objects.filter(category_type_id = 1)
    arr = []
    sum = 0
    for category in categories:
         dic = {}
         values = 0
         for item in category.items.filter(user=user).all():
             values = values + abs(item.value)
         if values == 0:
             continue
         dic["y"] = values
         dic["indexLabel"] = category.name
         arr.append(dic)
         sum = sum + values
    for dic in arr:
        try:
            percentage = round((dic["y"]/sum)*100, 2)
        except ZeroDivisionError:
            percentage = 0
        dic["indexLabel"] =  dic["indexLabel"] + " " + str(percentage) + "%"
    return arr


def account_after_item_delete(user, item):
    account = Account.objects.filter(user=user).first()
    if item.category.category_type_id == 1:
        account.total_spendings = account.total_spendings - item.value
        account.save()
    elif item.category.category_type_id == 2:
        account.total_income = account.total_income - item.value
        account.save()