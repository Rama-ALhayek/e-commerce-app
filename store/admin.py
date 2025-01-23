from django.contrib import admin
from .models import Product,Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields=['slug']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields=['slug']


