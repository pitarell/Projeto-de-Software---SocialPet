from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .auth import manager_required
from .forms import CategoryForm, ProductForm
from .models import Category, Product


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

# Create your views here.
