# -*- coding: utf-8 -*-

#from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

from Patcher.views import SoftListAllView, VersionListView


urlpatterns = patterns('',
    url(r'^get/(?P<soft>[\w-]+)/(?P<major>[\d]+).(?P<minor>[\d]+).(?P<patch>[\d]+)/(?P<os>[\w-]+)-x(?P<bit>[\d]+)/(?P<file>[\w.-]+)?',"Patcher.views.get",name="patcher-download" ),
    url(r'^maj/(?P<soft>[\w-]+)/(?P<from_major>[\d]+).(?P<from_minor>[\d]+).(?P<from_patch>[\d]+)/((?P<to_key>last)|(?P<to_major>[\d]+).(?P<to_minor>[\d]+).(?P<to_patch>[\d]+))/(?P<os>[\w-]+)-x(?P<bit>[\d]+).json',"Patcher.views.maj",name="patcher-maj" ),
    url(r'^push/',"Patcher.views.push",name="patcher-push" ),
    url(r"^list/",SoftListAllView.as_view(),name="patcher-soft-list"),
    url(r"^(?P<soft>[\w-]+)/list/",VersionListView.as_view(),name="patcher-version-list"),
)
