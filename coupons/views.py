from django.shortcuts import render, redirect
from .forms import CouponApplyForm
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Coupon
@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon=Coupon.objects.get(code__iexact=code ,valid_from__lte=now,valid_to__gte=now,is_active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None

       # form.save()
    return redirect('cart:cart_details')  # Redirect to a page listing all coupons
    # else:
    #     form = CouponApplyForm()
    # return render(request, 'coupon_form.html', {'form': form})
