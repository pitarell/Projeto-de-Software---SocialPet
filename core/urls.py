from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views
from .auth import ThrottledLoginView

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('entrar/', ThrottledLoginView.as_view(), name='login'),
    path('sair/', LogoutView.as_view(), name='logout'),
]
