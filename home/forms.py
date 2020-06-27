from django import forms
from django.forms import ModelForm
from .models import CategoryType, Category, Item


class AddItemForm(ModelForm):

    category_type = forms.ModelChoiceField(
        queryset=CategoryType.objects.all(),
        label="Category Type",
        widget=forms.Select(
            attrs={'class': 'category_type_list form-control form-control-lg'})
    )

    class Meta:
        model = Item
        widgets = {
            'category': forms.Select(attrs={'class': 'category_types form-control form-control-lg'}),
            'date': forms.DateInput(attrs={'class': 'date_field form-control form-control-lg', 'type': 'date'}),
            'value': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'notes': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'style': 'height: 150px;'}),
        }
        fields = ['category_type', 'category', 'date', 'value', 'notes']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        # self.fields['category'].queryset = Category.objects.none()

        # if 'CategoryType' in self.data:
        #     try:
        #         category_type =CategoryType.objects.filter(id=int(self.data.get('CategoryType'))).first()
        #         self.fields['category'].queryset = Category.objects.filter(
        #             category_type=category_type)
        #     except (ValueError, TypeError):
        #         pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['category'].queryset = self.instance.CategoryType

    # category = forms.ModelChoiceField(
    #     queryset=Category.objects.all(),
    #     label="Category"
    # )

    # date = forms.DateField()
    # value = forms.FloatField()
    # notes = forms.CharField(widget=forms.Textarea)
