from django.shortcuts import render
from django.views.generic import View , TemplateView

# Create your views here.

class accounting(TemplateView):
    template_name = 'accounting/accounting.html'
    
class reports(TemplateView):
    template_name = 'accounting/reports.html'
