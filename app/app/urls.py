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
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from graphql_jwt.decorators import jwt_cookie
from app.registration.views import activate_account, reset_account, password_reset, password_reset_confirm 
from app.registration.thanks import thanks
from app.registration.tryagain import tryagain
# from app.registration.form import UserPasswordResetForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/activate/<token>', activate_account, name='activate'),
    path('api/reset/<token>', reset_account, name='reset'),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('password-reset/', 
            auth_views.PasswordResetView.as_view(
                template_name="password_reset.html"
            ), 
            name="password_reset"),
    path('password-reset/done', 
            auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), 
            name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>', 
            auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), 
            name="password_reset_confirm"),
    path('password-reset-complete', 
            auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), 
            name="password_reset_complete"),
    path('thanks/', thanks, name='thanks'),
    path('tryagain/', tryagain, name='oops!'),
    # path('api/test-payment/', test_payment, name='testpayment'),
    # path('api/save-stripe-info/', save_stripe_info, name='stripeinfo'),
    # path('api/confirm-payment-intent/', confirm_payment_intent, name='paymentintent'),
    # path('api/delete-subscription/', delete_subscription, name='deletesubscription')
]

urlpatterns += staticfiles_urlpatterns()