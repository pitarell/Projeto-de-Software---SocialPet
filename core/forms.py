from django import forms

from .models import Category, Movement, Product


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


class MovementForm(StyledModelForm):
    class Meta:
        model = Movement
        fields = ('product', 'quantity', 'notes')
        widgets = {'quantity': forms.NumberInput(attrs={'min': '0.01', 'step': '0.01'})}

    def __init__(self, *args, movement_type, **kwargs):
        self.movement_type = movement_type
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')

    def clean_quantity(self):
        value = self.cleaned_data['quantity']
        if value <= 0:
            raise forms.ValidationError('A quantidade deve ser maior que zero.')
        return value
