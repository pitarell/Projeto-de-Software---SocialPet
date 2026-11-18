from django import forms

from .models import Category, Product


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class CategoryForm(StyledModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description', 'is_active')


class ProductForm(StyledModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'category', 'unit', 'minimum_stock', 'is_active')

    def clean_minimum_stock(self):
        value = self.cleaned_data['minimum_stock']
        if value < 0:
            raise forms.ValidationError('O estoque mínimo não pode ser negativo.')
        return value
