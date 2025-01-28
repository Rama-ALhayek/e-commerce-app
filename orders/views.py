from django.shortcuts import render,get_object_or_404,redirect

from .models import OrderItem,Order
from .forms import OrderCreateForm,OrderPayForm
from cart.cart import Cart
from django.core.mail import send_mail
from django.conf import settings
from .tasks import send_emails
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint
import os
from .tasks import payment_completed
def order_create(request):
    cart = Cart(request)
    order = None
    success=False
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            order_id =order.order_id
            send_emails.delay(order_id)


            # subject = 'Order Confirm'
            # message = f'Your Order ID : {order.order_id} has been created successfully. \n\nOrder details:\n'
            # for item in cart :
            #     product_name = item['product'].name
            #     message += f'Product: {product_name}, Price: {item['price']}, Quantity:{ item['quantity']}\n'
            # email_from=settings.DEFAULT_FROM_EMAIL
            # recipient_list=[form.cleaned_data['email']]
            # send_mail(subject,message,email_from,recipient_list)
            success=True
            return redirect('orders:pay_order',order_id=order.id)
        return render(request,'orders/created.html',{'order':order,'success': success})
        
    else:
        form = OrderCreateForm()
        
    return render(request,'orders/created.html',{'form':form,'cart':cart})  



def payment_view(request,order_id):
    order=get_object_or_404(Order,id=order_id)
    if request.method == 'POST':
        form = OrderPayForm(request.POST,request.FILES)
        if form.is_valid():
            order_pay =form.save(commit=False)
            order_pay.order = order
            order_pay.paid=True
            order_pay.save()

            order.paid=True
            order.save()
            return redirect('orders:payment_success',order_id=order.id)
    else:
        form =OrderPayForm()

    return render(request, 'orders/pay_form.html', {'form': form,'order':order})
    


def payment_success(request,order_id):
    order=get_object_or_404(Order,id=order_id)
    payment_completed.delay(order.id)
    return render(request, 'orders/payment_success.html', {'order':order})



@staff_member_required
def admin_order_pdf(request,order_id):
    order=get_object_or_404(Order,id=order_id)
    html = render_to_string('orders/pdf.html', {'order':order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.order_id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response)
    return response

