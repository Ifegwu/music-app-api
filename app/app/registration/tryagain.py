from django.template.loader import render_to_string
import os
from django.shortcuts import render
from django.http import HttpResponse



def tryagain(request):
    msg_html = render_to_string('oops.html')
    return HttpResponse(msg_html)
    
    
