# -*- coding: utf-8 -*-

from django.contrib import admin

from Patcher.models import *

class SoftAdmin(admin.ModelAdmin):
    list_display    = ("slug","name")
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Soft,SoftAdmin)

class VersionAdmin(admin.ModelAdmin):
    list_display = ("number","soft","os","bit","created")
    list_filter = ("number","soft","os","bit")
admin.site.register(Version,VersionAdmin)

class FileAdmin(admin.ModelAdmin):
    list_display = ("filename","file","version","created","action")
    list_filter = ("version__soft","version__number","version__os","version__bit","filename","action")
admin.site.register(File,FileAdmin)

