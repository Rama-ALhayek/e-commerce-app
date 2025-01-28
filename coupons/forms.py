from django import forms

from django import forms
from django.core.exceptions import ValidationError
from .models import Coupon

class CouponApplyForm(forms.Form):
    code = forms.CharField()
 