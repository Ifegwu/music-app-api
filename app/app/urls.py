"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from graphql_jwt.decorators import jwt_cookie
from app.registration.views import activate_account #, test_payment, save_stripe_info, confirm_payment_intent, delete_subscription 
from app.registration.thanks import thanks
from app.registration.tryagain import tryagain

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/activate/<token>', activate_account, name='activate'),
    path('graphql/', csrf_exempt(jwt_cookie(GraphQLView.as_view(graphiql=True)))),
    path('api/thanks/', thanks, name='thanks'),
    path('api/tryagain/', tryagain, name='oops!'),
    # path('api/test-payment/', test_payment, name='testpayment'),
    # path('api/save-stripe-info/', save_stripe_info, name='stripeinfo'),
    # path('api/confirm-payment-intent/', confirm_payment_intent, name='paymentintent'),
    # path('api/delete-subscription/', delete_subscription, name='deletesubscription')
]

urlpatterns += staticfiles_urlpatterns()