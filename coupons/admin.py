from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class CoupounAdmin(admin.ModelAdmin):
    list_display = ['code','valid_from','valid_to']
    list_filter = ['is_active','valid_from','valid_to']
    search_fields = ['code']