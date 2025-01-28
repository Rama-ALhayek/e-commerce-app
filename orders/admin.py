from django.contrib import admin
from .models import Order,OrderItem
import csv
import datetime 
from django.http import HttpResponse
from django.db.models import Field, OneToOneField, ForeignKey

import csv
import datetime
from django.http import HttpResponse

from django.urls import reverse
from django.utils.safestring import mark_safe


def order_pdf(obj):
   url = reverse('orders:admin_order_pdf', args=[obj.id])
   return mark_safe(f'<a href="{url}" target="_blank">Download PDF</a>')  

order_pdf.short_description = 'Invoice'



def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta  # Get the model's metadata
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)

    # Get all fields that are not relationship fields (many-to-many or one-to-many)
    fields = [field for field in opts.get_fields() if hasattr(field, 'verbose_name') and not (field.many_to_many or field.one_to_many)]

    # Write the header row (field verbose names)
    writer.writerow([field.verbose_name for field in fields])

    # Write the data rows
    for obj in queryset:
        row = []
        for field in fields:
            value = getattr(obj, field.name)

            # If the field is a DateTime field, format the date
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            row.append(value)
        writer.writerow(row)

    return response

export_to_csv.short_description = 'Export to CSV'



class OrderItemInline(admin.TabularInline):
   model =OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
   list_display = ['first_name', 'email', 'paid', 'created_at', order_pdf]
   inlines=[OrderItemInline]
   actions = [export_to_csv]