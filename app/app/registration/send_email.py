import jwt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
# from django.shortcuts import response
from django.template.loader import render_to_string
import os
from app.settings import DOMAIN, SENDGRID_API_KEY, SECRET_KEY
# from app.settings import DOMAIN
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from app.registration.models import User

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

def contact_form(email, name, body):
    context = {
        'name': name,
        'email': email,
        'small_text_detail': body      
    }
    msg_html = render_to_string('contact_form.html', context)
    from_email = Email("danielagbanyim@hotmail.com")
    to_email = To("agbanyimdaniel29@gmail.com")
    subject = "Sender - {}: A message from Temunah Music contact form".format(name)
    
    mail = Mail(
        from_email, 
        to_email, 
        subject, 
        html_content=msg_html)
    print(msg_html)
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        # response = sg.client.mail.send.post(request_body=mail.get())
        response = sg.send(mail)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))
        # print(e.message)
