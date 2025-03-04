from django import forms
from .models import Order,OrderPay
from django.core.exceptions import ValidationError

class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['first_name', 'last_name','address','postal_code','city','email']

class OrderPayForm(forms.ModelForm):

    class Meta:
        model = OrderPay
        fields = ['pay_phone', 'pay_image']


            
    def clean_pay_phone(self):
        pay_phone = self.cleaned_data.get('pay_phone')
        
        # Check if the phone number contains only digits
        if not pay_phone.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        
        # Optionally, check the length of the phone number (if required)
        if len(pay_phone) != 11:  # Assuming a 10-digit phone number
            raise ValidationError("Phone number must be 11 digits long.")
        
        valid_prefixes = ['010', '011', '012','015']  # List of valid country prefixes (You can extend this list as needed)
    
        if not any(pay_phone.startswith(prefix) for prefix in valid_prefixes):
            raise ValidationError(f"Phone number must start with a valid prefix. Valid prefixes are {', '.join(valid_prefixes)}.")
        
        return pay_phone