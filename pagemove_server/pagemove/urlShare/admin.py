from .models import User, Device, URL

from django.contrib import admin


class DeviceInline(admin.TabularInline):
    model = Device


class URLInline(admin.TabularInline):
    model = URL


class UserAdmin(admin.ModelAdmin):
    inlines = [DeviceInline, URLInline]

admin.site.register(User, UserAdmin)
