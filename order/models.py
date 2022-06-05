from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product

from django.dispatch import receiver
from django.db.models.signals import post_save

from account.confirmations_email import send_notification

User = get_user_model()
STATUS_CHOICES = (
    ('open', 'Открыт'),
    ('in_process', 'В процессе'),
    ('closed', 'Закрыт'),
)


class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name='items', on_delete=models.RESTRICT)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return f'{self.product} -> {self.quantity} шт'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='orders')
    product = models.ManyToManyField(Product, through=OrderItem)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)


@receiver(post_save, sender=Order)
def order_post_save(sender, instance, *args, **kwargs):
    send_notification(instance.user, instance.id)
