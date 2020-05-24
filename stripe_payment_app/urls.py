from django.urls import path
from stripe_payment_app import views

urlpatterns = [
    path('', views.checkout_view, name='checkout'),
    path('webhook', views.webhook_view,name='webhook'),
]
