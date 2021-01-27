import jwt
from django.shortcuts import redirect, render
from app.registration.thanks import thanks
from app.registration.models import User
import logging
from app.settings import SECRET_KEY, DOMAIN, FRONTEND_DOMAIN, STRIPE_SECRET_KEY
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import stripe  
from django.contrib.auth import login as auth_login
from .models import Subscriptions
from .forms import UserPasswordResetForm, UserPasswordResetConfirmForm

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

def reset_account(request, token):
    username = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])["user"]
    user = User.objects.get(username=username)
    if username and not user.is_verified:
        user.is_verified = True
        # user.save()
        # return redirect(f'{DOMAIN}/api')
        # return thanks
        msg_html = render_to_string('password_reset.html')
        return HttpResponse(msg_html)
    else:
        user.is_verified = False
        # messages.success(request, ('Items has been added to list'))
        # return redirect(f'{DOMAIN}/api')
        msg_html = render_to_string('oops.html')
        return HttpResponse(msg_html)

def password_reset(request):
    user = User.objects.get(email=email)
    if request.method == 'POST':
        form = UserPasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})

def password_reset_confirm(request):
    user = User.objects.get(password=password)
    if request.method == 'POST':
        form = UserPasswordResetConfirmForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('password_reset_complete.html')
    else:
        form = UserPasswordResetConfirmForm()
    return render(request, 'password_reset_confirm.html', {'form': form})