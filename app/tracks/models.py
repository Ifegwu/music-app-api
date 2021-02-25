from django.db import models
# from django.contrib.auth import get_user_model
from app.registration.models import User
from django.core.validators import RegexValidator
URL_VALIDATOR_MESSAGE = 'Not a valid URL.'
URL_VALIDATOR = RegexValidator(regex='/^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/', message=URL_VALIDATOR_MESSAGE)



class Track(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    url = models.URLField(validators=[URL_VALIDATOR])
    avarta = models.URLField(blank=True, default='DEFAULT VALUE', validators=[URL_VALIDATOR])
    created_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(
        # get_user_model(),
        User(),
        null=True,
        on_delete=models.CASCADE
    )


class Like(models.Model):
    user = models.ForeignKey(
        # get_user_model(),
        User(),
        null=True,
        on_delete=models.CASCADE
    )
    track = models.ForeignKey(
        'tracks.Track',
        related_name='likes',
        on_delete=models.CASCADE
    )
