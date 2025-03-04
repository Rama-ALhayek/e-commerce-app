from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.name

    def save(self, *args ,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)     
    

class Product(models.Model):
    STATUS = (
        ('DF', 'Draft'),
        ('AV', 'Available'),
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='products/images')
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=6 , decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, max_length=2, default='AV')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes= [models.Index(fields=['id','slug'])]
        verbose_name = "Product"
        verbose_name_plural = "Products"
        

    def __str__(self):
        return self.name

    def save(self, *args ,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)     
    