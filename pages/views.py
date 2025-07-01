from django.shortcuts import render
from django.views.generic import View , TemplateView

# Create your views here.

class index(TemplateView):
    template_name = 'pages/index.html'