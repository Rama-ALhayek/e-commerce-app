from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'username',]
    list_display_links = ('email', 'first_name','last_name', 'username')
    readonly_fields = ('date_joined', 'last_login')  
    ordering = ['-date_joined']