from django import forms
from django.forms import ModelForm
from .models import CategoryType, Category, Item
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AddItemForm(ModelForm):

    category_type = forms.ModelChoiceField(
        queryset=CategoryType.objects.all(),
        label="Category Type",
        widget=forms.Select(
            attrs={'class': 'category_type_list form-control form-control-lg mb-2'}),
        initial=CategoryType.objects.filter(id=1).first()
    )

    class Meta:
        model = Item
        widgets = {
            'category': forms.Select(attrs={'class': 'category_types form-control form-control-lg mb-2'}),
            'date': forms.DateInput(attrs={'class': 'date_field form-control form-control-lg mb-2', 'type': 'date'}),
            'value': forms.TextInput(attrs={'class': 'form-control form-control-lg mb-2'}),
            'notes': forms.Textarea(attrs={'class': 'form-control form-control-lg mb-2', 'style': 'height: 130px;'}),
        }
        fields = ['category_type', 'category', 'date', 'value', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(
                    category_type=1)

        if 'category_type' in self.data:
            try:
                category_type =CategoryType.objects.filter(id=int(self.data.get('category_type'))).first()
                self.fields['category'].queryset = Category.objects.filter(
                    category_type=category_type)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            # self.fields['category'].queryset = self.instance.CategoryType
            self.fields['category'].queryset = Category.objects.filter(
                    category_type=self.instance.category.category_type)

