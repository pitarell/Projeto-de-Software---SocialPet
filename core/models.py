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


class Category(models.Model):
    name = models.CharField('nome', max_length=100, unique=True)
    description = models.TextField('descrição', blank=True, max_length=500)
    is_active = models.BooleanField('ativa', default=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.name


class Product(models.Model):
    class Unit(models.TextChoices):
        UNIT = 'UN', 'Unidade'
        KILOGRAM = 'KG', 'Quilograma'
        LITER = 'L', 'Litro'
        PACKAGE = 'PCT', 'Pacote'

    name = models.CharField('nome', max_length=120)
    description = models.TextField('descrição', blank=True, max_length=500)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name='categoria')
    unit = models.CharField('unidade de medida', max_length=3, choices=Unit.choices)
    current_quantity = models.DecimalField('quantidade atual', max_digits=12, decimal_places=2, default=0, editable=False)
    minimum_stock = models.DecimalField('estoque mínimo', max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField('data de cadastro', auto_now_add=True)
    is_active = models.BooleanField('ativo', default=True)

    class Meta:
        ordering = ('name',)
        constraints = [models.UniqueConstraint(fields=('name', 'category'), name='unique_product_per_category')]

    @property
    def needs_restock(self):
        return self.current_quantity <= self.minimum_stock

    def __str__(self):
        return self.name

# Create your models here.
