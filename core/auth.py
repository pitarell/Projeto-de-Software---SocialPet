from functools import wraps

from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.http import HttpResponseForbidden


def manager_required(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden('Autenticação obrigatória.')
        if not request.user.is_superuser and request.user.profile.role != 'GESTOR':
            return HttpResponseForbidden('Operação permitida somente para gestores.')
        return view(request, *args, **kwargs)
    return wrapped


class ThrottledLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def _key(self):
        username = self.request.POST.get('username', '').strip().lower()
        address = self.request.META.get('REMOTE_ADDR', 'unknown')
        return f'login-failures:{address}:{username}'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST' and cache.get(self._key(), 0) >= 5:
            messages.error(request, 'Acesso temporariamente bloqueado. Tente novamente em 15 minutos.')
            return self.render_to_response(self.get_context_data(form=self.get_form()))
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        key = self._key()
        cache.set(key, cache.get(key, 0) + 1, timeout=900)
        return super().form_invalid(form)

    def form_valid(self, form):
        cache.delete(self._key())
        return super().form_valid(form)
