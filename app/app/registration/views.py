import jwt
from django.shortcuts import redirect

from app.registration.models import User
from app.settings import SECRET_KEY, DOMAIN


def activate_account(request, token):
    username = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])["user"]
    user = User.objects.get(username=username)
    if username and not user.is_verified:
        user.is_verified = True
        user.save()
        return redirect(DOMAIN)
    else:
        user.is_verified = False
        # messages.success(request, ('Items has been added to list'))
        return redirect(f'{DOMAIN}/api')
