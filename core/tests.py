from decimal import Decimal

from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from .forms import ProductForm
from .models import Category, Movement, Product, UserProfile
from .services import register_movement


class SocialPetTestCase(TestCase):
    def setUp(self):
        cache.clear()
        self.manager = User.objects.create_user('gestor', password='SenhaSegura#123', first_name='Carlos')
        self.manager.profile.role = UserProfile.Role.MANAGER
        self.manager.profile.save()
        self.volunteer = User.objects.create_user('voluntario', password='SenhaSegura#456')
        self.category = Category.objects.create(name='Alimentação')
        self.product = Product.objects.create(
            name='Ração para cães', category=self.category, unit=Product.Unit.KILOGRAM,
            minimum_stock=Decimal('10'),
        )

    def test_valid_and_invalid_authentication(self):
        self.assertTrue(self.client.login(username='gestor', password='SenhaSegura#123'))
        self.client.logout()
        self.assertFalse(self.client.login(username='gestor', password='incorreta'))

    def test_login_is_blocked_after_five_failures(self):
        url = reverse('login')
        for _ in range(5):
            self.client.post(url, {'username': 'gestor', 'password': 'incorreta'})
        response = self.client.post(url, {'username': 'gestor', 'password': 'SenhaSegura#123'})
        self.assertContains(response, 'temporariamente bloqueado')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_manager_can_create_category(self):
        self.client.force_login(self.manager)
        response = self.client.post(reverse('category_create'), {'name': 'Higiene', 'description': '', 'is_active': True})
        self.assertRedirects(response, reverse('category_list'))
        self.assertTrue(Category.objects.filter(name='Higiene').exists())

    def test_volunteer_cannot_manage_categories(self):
        self.client.force_login(self.volunteer)
        response = self.client.get(reverse('category_create'))
        self.assertEqual(response.status_code, 403)

    def test_product_form_rejects_negative_minimum(self):
        form = ProductForm(data={
            'name': 'Coleira', 'category': self.category.pk, 'unit': Product.Unit.UNIT,
            'minimum_stock': '-1', 'is_active': True,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('minimum_stock', form.errors)

    def test_donation_updates_balance_and_history(self):
        movement = register_movement(
            product=self.product, user=self.volunteer, movement_type=Movement.Type.IN,
            quantity='15', reason=Movement.Reason.DONATION,
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.current_quantity, Decimal('15'))
        self.assertEqual(movement.reason, Movement.Reason.DONATION)
        self.assertEqual(self.product.movements.count(), 1)

    def test_withdrawal_updates_balance(self):
        register_movement(product=self.product, user=self.manager, movement_type=Movement.Type.IN, quantity='20', reason=Movement.Reason.DONATION)
        register_movement(product=self.product, user=self.volunteer, movement_type=Movement.Type.OUT, quantity='7.5', reason=Movement.Reason.CONSUMPTION)
        self.product.refresh_from_db()
        self.assertEqual(self.product.current_quantity, Decimal('12.5'))

    def test_negative_stock_is_blocked_without_partial_write(self):
        with self.assertRaises(ValidationError):
            register_movement(product=self.product, user=self.volunteer, movement_type=Movement.Type.OUT, quantity='1', reason=Movement.Reason.CONSUMPTION)
        self.product.refresh_from_db()
        self.assertEqual(self.product.current_quantity, Decimal('0'))
        self.assertEqual(Movement.objects.count(), 0)

    def test_non_positive_movement_is_rejected(self):
        with self.assertRaises(ValidationError):
            register_movement(product=self.product, user=self.volunteer, movement_type=Movement.Type.IN, quantity='0', reason=Movement.Reason.DONATION)

    def test_restock_alert_at_minimum(self):
        self.product.current_quantity = Decimal('10')
        self.assertTrue(self.product.needs_restock)
        self.product.current_quantity = Decimal('10.01')
        self.assertFalse(self.product.needs_restock)

    def test_stock_and_history_require_authentication(self):
        for name in ('stock', 'movement_history'):
            response = self.client.get(reverse(name))
            self.assertRedirects(response, f"{reverse('login')}?next={reverse(name)}")

    def test_linked_category_cannot_be_deleted(self):
        with self.assertRaises(IntegrityError):
            self.category.delete()

# Create your tests here.
