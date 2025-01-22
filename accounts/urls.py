from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('sign-up/', views.user_signUp, name='sign_up'),
    path('login/', views.user_login, name='login'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

]

