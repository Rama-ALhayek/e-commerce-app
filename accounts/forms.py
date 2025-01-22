from django import forms
from .models import Account
    
class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'country','phone_number']

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        print(cleaned_data)
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Your passwords don\'t match!')
        print(cleaned_data)
        return cleaned_data
    

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder']= 'Enter First Name'
            
        self.fields['last_name'].widget.attrs['placeholder']= 'Enter Last Name'

        self.fields['phone_number'].widget.attrs['placeholder']= 'Enter Phone Number'
        
        self.fields['email'].widget.attrs['placeholder']= 'Enter Email'


