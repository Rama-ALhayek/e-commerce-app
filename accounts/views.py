from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegisterForm
from .models import Account
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


def user_signUp(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            country = form.cleaned_data['country']
            user_name = email.split("@")[0]
            password = form.cleaned_data['password']
            phone_number= form.cleaned_data['phone_number']

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                country=country,
                username=user_name,
                password=password
            )
            user.phone_number=phone_number
            user.save()
            current_site = get_current_site(request)
            subject= 'Please Activate Your Email'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email=email
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to_email]
            )
            email.send()

            return redirect(reverse('accounts:login') + f'?command=verification&email={to_email}')
    else:
        form = RegisterForm()
    
    context = {'form': form,}

    return render(request, 'accounts/register.html', context)



def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You are logged in.')
        else:
            messages.error(request, 'Invalid login! Email or password is invalid.')
            return redirect('accounts:login')

    return render(request, 'accounts/login.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Invalid activation link or the link has expired.')
        return redirect('accounts:sign_up')