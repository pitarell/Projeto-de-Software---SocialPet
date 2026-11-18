from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    class Role(models.TextChoices):
        MANAGER = 'GESTOR', 'Gestor'
        VOLUNTEER = 'VOLUNTARIO', 'Voluntário'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField('perfil', max_length=12, choices=Role.choices, default=Role.VOLUNTEER)
    created_at = models.DateTimeField('data de cadastro', auto_now_add=True)

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} — {self.get_role_display()}'

# Create your models here.
