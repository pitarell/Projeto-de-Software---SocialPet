from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Movement, Product


@transaction.atomic
def register_movement(*, product, user, movement_type, quantity, reason, notes=''):
    quantity = Decimal(quantity)
    if quantity <= 0:
        raise ValidationError('A quantidade deve ser maior que zero.')
    locked_product = Product.objects.select_for_update().get(pk=product.pk)
    if movement_type == Movement.Type.OUT and locked_product.current_quantity < quantity:
        raise ValidationError('Estoque insuficiente para registrar esta saída.')
    delta = quantity if movement_type == Movement.Type.IN else -quantity
    locked_product.current_quantity += delta
    locked_product.save(update_fields=('current_quantity',))
    return Movement.objects.create(
        product=locked_product, user=user, type=movement_type,
        quantity=quantity, reason=reason, notes=notes,
    )
