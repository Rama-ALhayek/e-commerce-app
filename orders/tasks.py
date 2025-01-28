from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import weasyprint
from io import BytesIO

@shared_task
def send_emails(order_id):
    try:
        order = Order.objects.get(order_id=order_id)
        subject = f'Order ID : {order.order_id}'
        message = f'Dear {order.get_full_name()},\n\nYou have successfully placed an order.\nYour Order ID is: {order.order_id}\n'
        from_email = settings.DEFAULT_FROM_EMAIL
        mail_sent = send_mail(subject, message, from_email, [order.email])

        if mail_sent:
            return f"Email sent successfully to {order.email}"
        else:
            return f"Failed to send email to {order.email}"
    except Order.DoesNotExist:
        return f"Order with ID {order_id} not found"
    except Exception as e:
        return f"An error occurred: {str(e)}"
    


@shared_task
def payment_completed(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'My shop - Invoice : {order.order_id}'
    message = f'Hello {order.get_full_name()},\nPlease find attached the invoice for tour recent purchase.'
    from_email = settings.DEFAULT_FROM_EMAIL
    html=render_to_string('orders/pdf.html',{'order':order})
    out =BytesIO()
    weasyprint.HTML(string=html).write_pdf(out)
    email = send_mail(subject, message, from_email, [order.email])
    email.attach(f'order_{order.order_id}.pdf',out.getvalue(),'application/pdf')
  
    email.send()
    return True


