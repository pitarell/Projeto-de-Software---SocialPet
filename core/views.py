from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from .auth import manager_required
from .forms import CategoryForm, MovementForm, ProductForm
from .models import Category, Movement, Product
from .services import register_movement


@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')


@login_required
@manager_required
def category_list(request):
    return render(request, 'core/category_list.html', {'categories': Category.objects.all()})


@login_required
@manager_required
def category_form(request, pk=None):
    instance = get_object_or_404(Category, pk=pk) if pk else None
    form = CategoryForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Categoria salva com sucesso.')
        return redirect('category_list')
    return render(request, 'core/form.html', {'form': form, 'title': 'Categoria'})


@login_required
@manager_required
def product_list(request):
    products = Product.objects.select_related('category').all()
    return render(request, 'core/product_list.html', {'products': products})


@login_required
@manager_required
def product_form(request, pk=None):
    instance = get_object_or_404(Product, pk=pk) if pk else None
    form = ProductForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Produto salvo com sucesso.')
        return redirect('product_list')
    return render(request, 'core/form.html', {'form': form, 'title': 'Produto'})


@login_required
def movement_form(request, movement_type):
    if movement_type not in (Movement.Type.IN, Movement.Type.OUT):
        return redirect('dashboard')
    form = MovementForm(request.POST or None, movement_type=movement_type)
    if form.is_valid():
        try:
            register_movement(
                product=form.cleaned_data['product'], user=request.user,
                movement_type=movement_type, quantity=form.cleaned_data['quantity'],
                reason=Movement.Reason.DONATION if movement_type == Movement.Type.IN else Movement.Reason.CONSUMPTION,
                notes=form.cleaned_data['notes'],
            )
        except ValidationError as error:
            form.add_error('quantity', error.message)
        else:
            label = 'Doação' if movement_type == Movement.Type.IN else 'Saída'
            messages.success(request, f'{label} registrada com sucesso.')
            return redirect('stock')
    title = 'Registrar doação' if movement_type == Movement.Type.IN else 'Registrar saída'
    return render(request, 'core/movement_form.html', {'form': form, 'title': title, 'movement_type': movement_type})

# Create your views here.
