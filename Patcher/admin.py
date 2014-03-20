# -*- coding: utf-8 -*-

from django.contrib import admin

from Patcher.models import *

class SoftAdmin(admin.ModelAdmin):
    list_display    = ("slug","name")
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Soft,SoftAdmin)

class VersionAdmin(admin.ModelAdmin):
    list_display = ("number","soft","os","bit")
    list_filter = ("number","soft","os","bit")
admin.site.register(Version,VersionAdmin)

class FileAdmin(admin.ModelAdmin):
    list_display = ("filename","file","version","action")
    list_filter = ("filename","version","action")
admin.site.register(File,FileAdmin)

