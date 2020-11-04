import jwt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
# from django.shortcuts import response
from django.template.loader import render_to_string
import os
from app.settings import DOMAIN, SENDGRID_API_KEY, SECRET_KEY
# from app.settings import DOMAIN


def send_confirmation(email, username):
    token = jwt.encode({'user': username}, SECRET_KEY,
                       algorithm='HS256').decode('utf-8')
    print(SECRET_KEY)
    context = {
        'small_text_detail': 'Thank you for '
                             'creating an account. '
                             'Please verify your email '
                             'address to set up your account.',
        'email': email,
        'domain': DOMAIN,
        'token': token,
    }
    # locates our email.html in the templates folder
    msg_html = render_to_string('email.html', context)
    message = Mail(
        # the email that sends the confirmation email
        from_email='danielagbanyim@hotmail.com',
        to_emails=[email],  # list of email receivers
        subject='Account activation',  # subject of your email
        html_content=msg_html)
    print(msg_html)
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))
        # print(e.message)
