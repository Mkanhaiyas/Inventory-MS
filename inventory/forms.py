from django import forms
from django.core.exceptions import ValidationError
from .models import Product
from .models import StockTransaction, StockDetail


# Product Form Fields
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        prod_name = cleaned_data.get("prod_name")
        category = cleaned_data.get("category")
        unit = cleaned_data.get("unit")

        if Product.objects.filter(
            prod_name=prod_name, category=category, unit=unit
        ).exists():
            raise ValidationError("This product already exists!")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


# Transaction Form Fields
class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = ["trans_type", "trans_date"]
        widgets = {
            "trans_type": forms.Select(attrs={"class": "form-control"}),
            "trans_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }


# Stock Detail Form Fields
class StockDetailForm(forms.ModelForm):
    class Meta:
        model = StockDetail
        fields = ["product", "quantity"]
        widgets = {
            "product": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
        }
