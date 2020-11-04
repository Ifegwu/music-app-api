import jwt
from django.shortcuts import redirect, render
from app.registration.thanks import thanks
from app.registration.models import User
from app.settings import SECRET_KEY, DOMAIN, FRONTEND_DOMAIN
from django.template.loader import render_to_string
from django.http import HttpResponse

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
