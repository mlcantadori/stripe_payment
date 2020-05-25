from django.shortcuts import render
import stripe
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from decimal import Decimal
from datetime import datetime
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY

def checkout_view(request):
    intent = stripe.PaymentIntent.create(
      amount=1999,
      currency='usd',
      metadata={'integration_check': 'accept_a_payment'},
    )
    amount_displayed = Decimal(str(intent.amount/100)).quantize(Decimal('.01'))
    dict = {'client_secret':intent.client_secret,'amount_displayed':amount_displayed,'publishable_key':settings.STRIPE_PUBLISHABLE_KEY}
    return render(request,'stripe_payment_app/checkout.html',context=dict)

@csrf_exempt
def webhook_view(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  payment_intent = event.data.object # contains a stripe.PaymentIntent

  # Handle the event
  if event.type == 'payment_intent.succeeded':
    print('PaymentIntent was successful!')
    creation_date_unix = payment_intent['created']
    creation_date = datetime.utcfromtimestamp(creation_date_unix).strftime('%Y-%m-%d %H:%M:%S')
    webhook_object = payment_intent['object']
    webhook_status = payment_intent['status']
    currency = payment_intent['currency'].upper()
    amount_charged = Decimal(str(payment_intent['amount']/100)).quantize(Decimal('.01'))
    user_name = payment_intent['charges']['data'][0]['billing_details']['name']
    logger = logging.getLogger('successful_payments')
    logger.info("{} (UTC) - {}.{}: successful transaction of {} {} from {}".format(creation_date,
                                                                            webhook_object,
                                                                            webhook_status,
                                                                            currency,
                                                                            amount_charged,
                                                                            user_name))
  elif event.type == 'payment_intent.created':
    print('PaymentIntent was created')
  elif event.type == 'payment_intent.canceled':
    print('PaymentIntent was canceled')
  elif event.type == 'payment_intent.payment_failed':
    print('PaymentIntent has failed :(')

  return HttpResponse(status=200)
