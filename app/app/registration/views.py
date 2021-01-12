import jwt
from django.shortcuts import redirect, render
from app.registration.thanks import thanks
from app.registration.models import User
# from django.contrib.auth.models import User
from app.settings import SECRET_KEY, DOMAIN, FRONTEND_DOMAIN, STRIPE_SECRET_KEY
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import stripe  
from .models import Subscriptions
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


stripe.api_key = STRIPE_SECRET_KEY

def activate_account(request, token):
    username = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])["user"]
    user = User.objects.get(username=username)
    if username and not user.is_verified:
        user.is_verified = True
        user.save()
        # return redirect(f'{DOMAIN}/api')
        # return thanks
        msg_html = render_to_string('greetings.html')
        return HttpResponse(msg_html)
    else:
        user.is_verified = False
        # messages.success(request, ('Items has been added to list'))
        # return redirect(f'{DOMAIN}/api')
        msg_html = render_to_string('oops.html')
        return HttpResponse(msg_html)

@api_view(['POST'])
def test_payment(request, user):
    test_payment_intent = stripe.PaymentIntent.create(
        amount=1000, currency='ngn', 
        payment_method_types=['card'],
        receipt_email='test@example.com')
    return Response(status=status.HTTP_200_OK, data=test_payment_intent)

@api_view(['POST'])
def confirm_payment_intent(request):
    data = request.data
    payment_intent_id = data['payment_intent_id']

    stripe.PaymentIntent.confirm(payment_intent_id)

    return Response(status=status.HTTP_200_OK, data={"message": "Success"})

@api_view(['POST'])
def save_stripe_info(request):
    data = request.data
    email = data['email']
    music = data['music']
    payment_method_id = data['payment_method_id']
    extra_msg = '' # add new variable to response message
    # checking if customer with provided email already exists
    customer_data = stripe.Customer.list(email=email).data   
    # print(customer_data)
    
    # if the array is empty it means the email has not been used yet  
    if len(customer_data) == 0:
        # creating customer
        customer = stripe.Customer.create(
            email=email,
            description=music,
            payment_method=payment_method_id,
            invoice_settings={
                'default_payment_method': payment_method_id
            }
        )
    else:
        customer = customer_data[0]
        extra_msg = "Customer already existed."
    # add these lines
    customer_intent = stripe.PaymentIntent.create(
        customer=customer, 
        payment_method=payment_method_id,  
        currency='ngn', # you can provide any currency you want
        amount=500000,  # it equals 5000.00 NGN
        confirm=True
    )  

    customer_intent
    customer_intent.amount   

    stripe.Subscription.create(
        customer=customer,
        items=[
            {'price': 'price_1I6EAkJF4Y1CLG7ZZPtxzRfK'}, #here paste your price id
        ],
    )

    user = User.objects.get()
    if user.is_verified:    
        subscriptions = Subscriptions.objects.create(
            subscriber=user,
            music=music,
            email=email,
            stripe_id=customer.id,
            fee=customer_intent.amount
        )
        subscriptions.subscriber = user.id
        subscriptions.save()
        extra_msg = "You successfully created a subscription"

        return Response(status=status.HTTP_200_OK, 
            data={'message': 'Success', 'data': {
            'customer': customer, 'extra_msg': extra_msg}
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, 
            data={'message': 'You are not authorized to perform this action'})

@api_view(['POST'])
def delete_subscription(request):
    data = request.data
    email = data['email']
    extra_msg = ''
    customer_data = stripe.Customer.list(email=email).data

    customer = customer_data[0]

    if request.user.is_authenticated:
        sub_id = request.user.subscription.id
        print(sub_id)
        try:
            stripe.Subscription.delete(sub_id)
        except Exception as e:
            return JsonResponse({ 'error': (e.args[0])}, status=403)

        extra_msg = "Your subscription is deleted"

    return Response(status=status.HTTP_200_OK, 
        data={'message': 'Success', 'data': {
        'customer': customer, 'extra_msg': extra_msg}
    })