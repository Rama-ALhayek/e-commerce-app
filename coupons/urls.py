from . import views
from django.urls import path

app_name = 'coupons'

urlpatterns = [
    path('apply/', views.coupon_apply, name='coupon_apply'),]