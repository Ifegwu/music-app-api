from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.conf import settings
# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)

class Subscriptions(models.Model):
    email = models.CharField(max_length=50)
    fee = models.DecimalField(max_digits=8, decimal_places=2)
    music = models.CharField(max_length=100)
    stripe_id = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    subscriber = models.ForeignKey(User, blank=True, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = 'subscribers'

    def __unicode__(self):
        return u"%s's Subscription Info" % self.user_rec

    # def charge(self, request, email, music):
    #     # Set your secret key: remember to change this to your live secret key
    #     # in production. See your keys here https://manage.stripe.com/account
    #     stripe.api_key = settings.STRIPE_SECRET_KEY

    #     # Get the credit card details submitted by the form
    #     # token = request.POST['token']
    #     email = request.POST['email']
    #     music = request.POST['music']

    #     stripe_customer = stripe.Customer.create(
    #         email=email,
    #         description=music,
    #         payment_method=payment_method_id,
    #         invoice_settings={
    #             'default_payment_method': payment_method_id
    #         }
    #     )


    #     # Save the Stripe ID to the customer's profile
    #     # self.stripe_id = stripe_customer.id
    #     # self.music = stripe_customer.description
    #     # self.email = stripe_customer.email
    #     # self.fee = stripe_customer.fee
    #     # self.subscribed_by  = request.user.id
    #     # self.save()

    #     return stripe_customer