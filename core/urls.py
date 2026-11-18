from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views
from .auth import ThrottledLoginView

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('entrar/', ThrottledLoginView.as_view(), name='login'),
    path('sair/', LogoutView.as_view(), name='logout'),
    path('categorias/', views.category_list, name='category_list'),
    path('categorias/nova/', views.category_form, name='category_create'),
    path('categorias/<int:pk>/editar/', views.category_form, name='category_edit'),
    path('produtos/', views.product_list, name='product_list'),
    path('produtos/novo/', views.product_form, name='product_create'),
    path('produtos/<int:pk>/editar/', views.product_form, name='product_edit'),
]
