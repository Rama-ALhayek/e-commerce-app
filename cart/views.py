from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Product
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id = product_id, status='AV')

    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product , quantity= cd['quantity'] , override_quantity= cd['override'])
        return redirect('cart:cart_details')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product,id=product_id, status='AV')
    cart.delete(product)
    return redirect('cart:cart_details')

def cart_details(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form']=CartAddProductForm(initial={'quantity':item['quantity'],
                                                                 'override':True})
    context = { 'cart':cart}
    return render(request , 'cart/cart_details.html',context)

