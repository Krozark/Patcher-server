# -*- coding: utf-8 -*-
#from django.views.generic import TemplateView, FormView, ListView
#from django.views.generic.edit import ProcessFormView, FormMixin
#from django import forms
from django.views.decorators.csrf import csrf_exempt, csrf_protect, requires_csrf_token
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed
#from django.core.context_processors import csrf

#from django.template.context import RequestContext# Context
from django.utils.translation import ugettext_lazy as _
#from django.db.models import Q

from django.http import Http404

from Patcher.models import Soft,Version,File

def get(request,*args,**kwargs):
    k_soft    = kwargs.get('soft')
    k_major   = int(kwargs.get('major'))
    k_minor   = int(kwargs.get('minor'))
    k_patch   = int(kwargs.get('patch'))
    k_os      = kwargs.get('os')
    k_bit     = kwargs.get('bit')
    k_file    = kwargs.get('file')

    soft = Soft.objects.filter(slug=k_soft)[:1]
    if not soft:
        return #TODO
    soft = soft[0]
    number = k_patch + (k_minor + (k_major*100))*100
    version = Version.objects.filter(number=number,soft=soft,os=k_os,bit=k_bit)[:1]

    print soft,number,version
    Version.objects.filter(number__gt=version)

    print "get",args,kwargs
    return HttpResponse('{"get"}',content_type='application/json')

@csrf_exempt
def push(request,*args,**kwargs):
    if request.method != 'POST':
        return HttpResponseNotAllowed('Only POST here')

    k_soft    = request.POST.get('soft')
    k_major   = int(request.POST.get('major'))
    k_minor   = int(request.POST.get('minor'))
    k_patch   = int(request.POST.get('patch'))
    k_os      = request.POST.get('os')
    k_bit     = request.POST.get('bit')
    k_file    = request.FILES.get("file")

    filename  = k_file.name
    return HttpResponse('{"push"}',content_type='application/json')


