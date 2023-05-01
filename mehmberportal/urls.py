from django.urls import path

from . import views
from .views import payment_history
from .views import unlock

app_name = 'mehmberportal'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('payment-history/', payment_history, name='payment_history'),
    path('unlock/', unlock, name='unlock'),
]
