from django.db import models

from product.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


class Mark():
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5

    marks = (
        (one, 'Плохо'),
        (two, 'Неудовлетворительно'),
        (three, 'Удовлетворительно'),
        (four, 'Хорошо'),
        (five, 'Отлично!')
    )


class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    mark = models.PositiveSmallIntegerField(choices=Mark.marks)

    def __str__(self):
        return f'{self.mark} -> {self.product}'

    class Meta:
        unique_together = ('owner', 'product')
