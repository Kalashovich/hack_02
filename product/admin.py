from django.contrib import admin

from product.models import Product, Category, Likes, Comment

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Likes)
admin.site.register(Comment)
