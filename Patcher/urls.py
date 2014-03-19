# -*- coding: utf-8 -*-

#from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

#from Patcher.views import *


urlpatterns = patterns('',
    url(r'^get/(?P<soft>[\w-]+)/(?P<major>[\d]+).(?P<minor>[\d]+).(?P<patch>[\d]+)/(?P<os>[\w-]+)-x(?P<bit>[\d]+)/(?P<file>[\w.-]+)?',"Patcher.views.get" ),
    url(r'^push/',"Patcher.views.push" ),
)
