from django.shortcuts import render, get_object_or_404
from .models import Product,Category
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank
from cart.forms import CartAddProductForm
from django.core.cache import cache
from django.core.paginator import Paginator


def product_list(request, category_slug=None):
    products=Product.objects.filter(status='AV')
    categories = Category.objects.all()
    category = None
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products =  products.filter(category=category)
    paginator = Paginator(products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    context = {
        'products': products,
        'category ': category,
        'categories': categories ,
        'page_obj': page_obj,
    }
    
    return render(request, 'store/product_list.html', context)




def product_details(request, product_slug):
    cache_key = f'product_{product_slug}'
    product=cache.get(cache_key)
    if product is None:
        product = get_object_or_404(Product, slug=product_slug,status='AV' )
        cache.set(cache_key,product,timeout = 60 * 30 )

    cart_product_form= CartAddProductForm()
    context = {'detail': product,
               'cart_product_form':cart_product_form,
               }
    
    return render(request, 'store/product_details.html', context)


def product_search(request):
    query = None
    results = []

    if 'query' in request.GET:
        query = request.GET.get('query')
        search_vector = SearchVector('name', 'description')
        search_query = SearchQuery(query)

        if query:
            results = Product.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=query, status='AV').order_by('-rank')

    context = {
        'query': query,
        'results': results,
    }

    return render(request, 'store/search.html', context)