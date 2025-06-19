from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import OrderItem, Sale

@receiver(post_save, sender=OrderItem)
def create_sale_when_completed(sender, instance, created, **kwargs):
    # Only process if the status is 'completed'
    if instance.status != 'completed':
        return

    # Check if a Sale already exists for this specific product, quantity and order
    sale_exists = Sale.objects.filter(
        product=instance.product,
        quantity=instance.quantity,
        total_price=instance.price * instance.quantity,
        buyer=instance.order.name,
        email=instance.order.email,
        phone=instance.order.phone,
    ).exists()

    if not sale_exists:
        # Create the Sale entry
        Sale.objects.create(
            product=instance.product,
            buyer=instance.order.name,
            email=instance.order.email,
            phone=instance.order.phone,
            quantity=instance.quantity,
            total_price=instance.price * instance.quantity,
        )

        # Reduce product quantity if applicable
        if hasattr(instance.product, 'quantity') and instance.product.quantity is not None:
            instance.product.quantity -= instance.quantity
            instance.product.save()
