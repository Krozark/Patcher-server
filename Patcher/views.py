# -*- coding: utf-8 -*-

from django.views.decorators.csrf import csrf_exempt, csrf_protect, requires_csrf_token
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed, Http404
from django.utils.translation import ugettext_lazy as _

from Patcher.models import Soft,Version,File
from Patcher.forms import FileForm

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
    k_bit     = int(request.POST.get('bit'))
    k_file    = request.FILES.get("file")

    form = FileForm(request.POST,request.FILES)
    if not form.is_valid() or None in (k_soft,k_major,k_minor,k_patch,k_os,k_bit,k_file):
        return HttpResponseNotAllowed('Informations are wrong')

    filename  = k_file.name

    soft = Soft.objects.filter(slug=k_soft)[:1]
    if not soft:
        return HttpResponseNotAllowed('Informations are wrong')
    soft = soft[0]

    number = Version.version_to_number(k_major,k_minor,k_patch)
    version = Version.objects.filter(soft=soft,
                                     number__gte=number,
                                     os=k_os,
                                     bit=k_bit)[:1]
    if not version:
        version = Version(soft=soft,
                           number=number,
                           os=k_os,
                           bit=k_bit)
        version.save()
    else:
        version = version[0]

    if File.objects.filter(version=version,file=k_file.name).count() > 0:
        return HttpResponseNotAllowed('Informations are wrong')

    f = File(version=version,file=k_file)
    f.save()
    return HttpResponse('{"push"}',content_type='application/json')


