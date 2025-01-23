from django.shortcuts import render, get_object_or_404
from .models import Product,Category




def product_list(request, category_slug=None):
    products=Product.objects.filter(status='AV')
    categories = Category.objects.all()
    category = None
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products =  products.filter(category=category)

    context = {
        'products': products,
        'category ': category ,
        'categories': categories ,
    }
    
    return render(request, 'store/product_list.html', context)




def product_details(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug,status='AV' )
    context = {
        'detail': product,
    }
    
    return render(request, 'store/product_details.html', context)