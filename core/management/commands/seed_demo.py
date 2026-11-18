from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.models import Category, Movement, Product, UserProfile
from core.services import register_movement


class Command(BaseCommand):
    help = 'Cria dados fictícios para demonstração local do SocialPet.'

    def handle(self, *args, **options):
        manager, created = User.objects.get_or_create(
            username='carlos', defaults={'first_name': 'Carlos', 'last_name': 'Almeida', 'email': 'carlos@example.test'}
        )
        if created:
            manager.set_password('SocialPet#2026')
            manager.save()
        manager.profile.role = UserProfile.Role.MANAGER
        manager.profile.save()

        catalog = {
            'Alimentação': [('Ração para cães', 'KG', 20), ('Ração para gatos', 'KG', 15)],
            'Medicamentos': [('Vermífugos', 'UN', 10)],
            'Higiene': [('Tapetes higiênicos', 'PCT', 10), ('Shampoo para animais', 'UN', 5)],
            'Limpeza': [('Desinfetantes', 'L', 8)],
            'Acessórios': [('Coleiras', 'UN', 10)],
        }
        for category_name, products in catalog.items():
            category, _ = Category.objects.get_or_create(name=category_name)
            for name, unit, minimum in products:
                product, product_created = Product.objects.get_or_create(
                    name=name, category=category,
                    defaults={'unit': unit, 'minimum_stock': Decimal(minimum)},
                )
                if product_created:
                    register_movement(
                        product=product, user=manager, movement_type=Movement.Type.IN,
                        quantity=Decimal(minimum) * 2, reason=Movement.Reason.DONATION,
                        notes='Carga inicial fictícia para demonstração.',
                    )
        self.stdout.write(self.style.SUCCESS('Dados fictícios criados. Usuário: carlos | Senha: SocialPet#2026'))
