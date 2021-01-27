from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.conf import settings


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