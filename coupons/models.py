from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import MinValueValidator,MaxValueValidator

class Coupon(models.Model):
    code = models.CharField(max_length=8, unique=True)
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)], help_text="Percentage value (0 to 100).")
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField()
   

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = ("Coupon")
        verbose_name_plural = ("Coupons")
