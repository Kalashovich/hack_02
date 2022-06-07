from django.db import models

from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save

from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, primary_key=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Category)
def product_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='images', null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} - {self.price} (category: {self.category})'

#
# User = get_user_model()
#
#
# class Comment(models.Model):
#     owner = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
#     body = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.owner} -> {self.product} -> {self.created_at}'
#
#
# class Likes(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked')
#
#     class Meta:
#         unique_together = ['product', 'user']
#
