# -*- coding: utf-8 -*-

import os
import zipfile
import StringIO

from django.views.decorators.csrf import csrf_exempt, csrf_protect, requires_csrf_token
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from django.views.generic import ListView

from Patcher.models import Soft,Version,File
from Patcher.forms import FileForm
from Patcher.utils import render_to_json


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

    if not version:
        raise Http404
    version = version[0]
    
    
    qs = File.objects.filter(version__soft__name=k_soft,version__number__lte=number,version__os=version.os)
    if k_file:
        qs = qs.filter(filename=k_file)
    files = qs.order_by("filename","-version__number")
    # Files (local path) to put in the .zip
    filenames = []

    for f in files:
        add = True
        for x in filenames:
            if x.filename == f.filename:
                add = False
                break
        if add and f.action != 3:
            filenames.append(f)
    
    # Folder name in ZIP archive which contains the above files
    # E.g [thearchive.zip]/somefiles/file2.txt
    # FIXME: Set this to something better
    zip_subdir = "%s" % version
    if k_file:
        zip_subdir = "%s-%s" % (k_file,zip_subdir)

    zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
    s = StringIO.StringIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    for file in filenames:
        fpath = file.file.path
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, file.filename)

        # Add file, at correct path
        zf.write(fpath, zip_path)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp

@render_to_json()
def maj(request,*args,**kwargs):
    #soft
    k_soft    = kwargs.get('soft')
    #from
    k_from_major   = int(kwargs.get('from_major'))
    k_from_minor   = int(kwargs.get('from_minor'))
    k_from_patch   = int(kwargs.get('from_patch'))
    #to
    k_to_key     = kwargs.get("to_key")
    k_to_major   = int(kwargs.get('to_major') or 0)
    k_to_minor   = int(kwargs.get('to_minor') or 0)
    k_to_patch   = int(kwargs.get('to_patch') or 0)
    #os
    k_os      = kwargs.get('os')
    k_bit     = kwargs.get('bit')

    response = {"message":"all is fine",
           "status" : 0,
           "datas" : {}
          }


    from_number = k_from_patch + (k_from_minor + (k_from_major*100))*100
    to_number = k_to_patch + (k_to_minor + (k_to_major*100))*100
    soft = Soft.objects.filter(slug=k_soft)[:1]
    if not soft:
        response["message"] = "No soft find"
        response["status"] = 1
        return response

    soft = soft[0]
    from_version = Version.objects.filter(number=from_number,soft=soft,os=k_os,bit=k_bit)[:1]

    if not from_version:
        response["message"] = "No source version find"
        response["status"] = 2
        return response
    from_version = from_version[0]

    qs = Version.objects.filter(soft=soft,os=k_os,bit=k_bit)
    if to_number > 0:
        to_version = qs.filter(number=to_number)[:1]
        if not to_version:
            response["message"] = "The destination version does't exist"
            response["status"] = 3
            return response
    else:
        to_version = qs.filter(number__gt=from_number).order_by("-number")[:1]
        if not to_version:
            response["message"] = "Your version is the lastest"
            response["status"] = 4
            return response
    to_version = to_version[0]
    to_number = to_version.number


    files = File.objects.filter(version__soft__name=k_soft,
                                version__os=to_version.os,
                                version__number__lte=to_number,
                                version__number__gt=from_number
                               ).order_by("filename","-version__number")

    fs = []

    for f in files:
        add = True
        for x in fs:
            if x["filename"] == f.filename:
                add = False
                break
        if add:
            datas = {"filename" : f.filename,
                    "action" : f.action,
                    "action_str" : f.get_action_display()
                   }
            if f.file:
                datas.update({"url" : f.file.url})
            fs.append(datas)

    response["datas"] = {"files" : fs}

    return response

@csrf_exempt
def push(request,*args,**kwargs):
    if request.method != 'POST':
        return HttpResponse('Only POST here')

    k_soft      = request.POST.get('soft')
    k_major     = int(request.POST.get('major'))
    k_minor     = int(request.POST.get('minor'))
    k_patch     = int(request.POST.get('patch'))
    k_os        = request.POST.get('os')
    k_bit       = int(request.POST.get('bit'))
    k_file      = request.FILES.get("file")
    k_filename  = request.POST.get('filename')
    k_user      = request.POST.get('user')
    k_pass      = request.POST.get('pass')

    #params
    if None in (k_soft,k_major,k_minor,k_patch,k_os,k_bit,k_filename,k_user,k_pass):
        return HttpResponse('Informations are wrong')

    #user
    user = authenticate(username=k_user, password=k_pass)
    if user is None or not user.is_active:
        return HttpResponse('Wrong user/pass')
    if not user.is_superuser:
        return HttpResponse('Wrong user')

    #soft
    soft = Soft.objects.filter(slug=k_soft)[:1]
    if not soft:
        return HttpResponse('Soft does not exist')
    soft = soft[0]

    #version
    number = Version.version_to_number(k_major,k_minor,k_patch)
    if Version.objects.filter(soft=soft,number__gt=number,os=k_os,bit=k_bit).count() > 0:
        return HttpResponse('A newer version exist of this soft')

    version = Version.objects.filter(soft=soft,number=number,os=k_os,bit=k_bit)[:1]
    if not version:
        version = Version(soft=soft,number=number,os=k_os,bit=k_bit)
        version.save()
    else:
        version = version[0]

    #files
    form = FileForm(request.POST,request.FILES)
    if not form.is_valid():
        return HttpResponse('Wrong file')
    
    files = File.objects.filter(version=version,filename=k_filename)
    if files.count() > 0:
        return HttpResponse('File already exist')

    action = 0
    if not k_file:
        action = 3 #delete
    else:
        files = File.objects.filter(version__soft=version.soft,filename=k_filename)
        if not files:
            action = 1 #new
        else:
            action = 2 #maj
            print k_filename,k_soft
            if not k_filename == k_soft:
                files = File.objects.filter(version__soft=version.soft,filename=k_filename,file__endswith=k_file.name)
                if files:
                    return HttpResponse('File already exist in other version')

    f = File(version=version,filename=k_filename,file=k_file,action=action)
    f.save()
    return HttpResponse('File added')


class SoftListAllView(ListView):
    template_name = "Patcher/Soft/list.html"
    model   = Soft

    def get_template_names(self):
        names = []
        names.append(self.template_name)
        return names
    
class VersionListView(ListView):
    template_name = "Patcher/Version/list.html"
    model   = Version

    def get_template_names(self):
        names = []
        names.append(self.template_name)
        return names

    def get_queryset(self,*args,**kwargs):
        return Version.objects.filter(soft__slug=self.kwargs['soft'])


