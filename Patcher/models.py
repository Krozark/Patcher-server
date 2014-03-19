# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Soft(models.Model):
    name    = models.CharField(_("Name"),max_length=255,unique=True)
    slug    = models.SlugField(_("Slug"),max_length=32,unique=True)

    def __unicode__(self):
        return u"%s" % self.name

class Version(models.Model):
    BIT_CHOICE = (32,64)

    soft    = models.ForeignKey(Soft,null=False,blank=False)
    number  = models.IntegerField(_("Number"),help_text=_("Format is xxxxyyzz where xxxx is the Major version, yy the minor and zz the patch"))
    os      = models.CharField(_("os name"),max_length=128)
    bit     = models.IntegerField(_("Bit number"),choices=[(x,x) for x in BIT_CHOICE])


    def get_version(self):
        major = self.version / (100*100)
        minor = self.version / 100 - major*100
        patch = self.version - (minor + major*100)*100
        return (major, minor,patch)

    def __unicode__(self):
        (major,minor,patch) = self.get_version()
        return u"%s-%s-x%d.%d.%d.%d" % (self.soft,self.os,self.bit,major,minor,patch)

class File(models.Model):
    def get_upload_dir(self,filename):
        (major,minor,patch) = self.version.get_version()
        return "%s/%d.%d.%d/%s-x%d/" % (self.soft.slug,major,minor,patch,self.version.os,self.version.bit)

    version = models.ForeignKey(Version)
    file    = models.FileField(_("File"),upload_to=get_upload_dir)
    action  = models.IntegerField(_("Action"),choices=[(1,"New"),(2,"Maj"),(3,"Deleted")])


    def __unicode__(self):
        return u"%s" % self.file

